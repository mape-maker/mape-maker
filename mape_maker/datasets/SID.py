from mape_maker.datasets.Dataset import Dataset
import mape_maker.utilities.curvature_correction as curvature_correction
import numpy as np
import pandas as pd
from scipy.stats import beta


class SID(Dataset):
    """Simulation Input dataset, extends Dataset and implements specific methods to simulate the scenarios

    Attributes:
        extends Dataset
        SimParams (Dict[datasetx, float]): dictionary of maximum attainable mean absolute error for each x

    """
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.SimParams = None
        self.simulations = []
        self.seed = None
        self.number_of_simulations = 0
        self.curvature_parameters = None

    def simulate_multiple_scenarios(self, output_dir: str, **kwargs):
        """simulate multiple scenarios and store them in output dir

        Notes:
            All the inputs relative to the simulations are stored and accessible in self.SimParams

        Args:
            output_dir (str): path to the stored csv. If None, then no output will be saved.
            **kwargs:

        Returns:

        """
        simulations = pd.DataFrame()
        for i in range(self.number_of_simulations):
            simulation = self.simulate_one_scenario()
            simulation.name = simulation.name + "_n_{}".format(i)
            simulations = pd.concat([simulations, simulation], axis=1)
        return simulations

    def simulate_one_scenario(self):
        simulation = pd.DataFrame(index=self.x_t.index)
        simulation.loc[self.x_t.index, "x"] = self.x_t
        simulation["base_process"] = self.arma_process.simulate_base_process(self.x_t)
        simulation["error"] = simulation.apply(self.from_bp_to_errors, axis=1)
        simulation[self.y_name] = simulation.apply(self.from_errors_to_simulated, axis=1, **{"cap": self.dataset_info['cap']})
        simulation = self.adjust_curvature(simulation)
        return simulation

    def adjust_curvature(self, simulation):
        try:
            if self.curvature_parameters is not None:
                model = curvature_correction.model_first_second_dif(self.name + "_curvature_correction",
                                                                    self.curvature_parameters["curvature_target"], self.x_t,
                                                                    simulation["error"], cap=self.dataset_info["cap"])
                simulation = curvature_correction.solve(model, simulation.index, solver=self.curvature_parameters["solver"],
                                                        time_limit=self.curvature_parameters["time_limit"],
                                                        mip_gap=self.curvature_parameters["MIP"], show=self.show)
                simulation.name = "{}_curvature".format(self.y_name)
            else:
                simulation = simulation[self.y_name]
        except Exception as e:
            print(e)
        return simulation

    def from_bp_to_errors(self, row):
        x = row["x"]  # row has three rows : error, x, bp, and set datetime as columns
        bp = row["base_process"]
        a, b, loc, scale = self.s_x[x]
        simulated_error = beta.ppf(bp, a, b, loc=loc, scale=scale)  # scale = 0 cause NAN
        return simulated_error

    def from_errors_to_simulated(self, row, floored=True, simulators=(), floor=0, cap=4500, show_errors=False):
        """
        function returning the simulation x in function of the simulated error
        :param row: one line of a dataframe
        :param floored: apply the floor and cap or not
        :param simulators: function used to recompute a random variable if row is outside of the bounds [floor, cap]
        :param floor: min of the value that your simulation can take
        :param cap: max of the value that your simulation can take
        :return: simulation
        """
        actual = row["x"]
        y = actual + row["error"]
        if floored:
            if y < floor or y > cap:
                if show_errors is True:
                    self.logger.error("Error : y = {} max is {}, \n   {}".format(y, cap, row))
                if len(simulators) == 2:
                    while y < floor:
                        y = simulators[0](np.random.uniform(0, 1, 1))[0]
                    while y > cap:
                        y = simulators[1](np.random.uniform(0, 1, 1))[0]
                else:
                    y = floor if y < floor else cap
        return y

    def set_sim_params(self, sim_params, **kwargs):
        self.SimParams = sim_params
        self.seed = sim_params.seed
        self.number_of_simulations = sim_params.n
        self.s_x = sim_params.s_x_tilde
        self.dataset_info["cap"] = sim_params.cap
        self.arma_process = sim_params.base_process
        self.curvature_parameters = sim_params.curvature_parameters
        self.floored = sim_params.floored
        self.show = sim_params.show

    def add_statistics(self):
        """

        Notes: add :
            - "e_score" : maximum attainable mare with the conditional distribution

        Returns:

        """
        pass