import pandas as pd
import numpy as np
from typing import List, Dict
from logging import Logger
from mape_maker.datasets.SID import SID
from mape_maker.datasets.XYID import XYID
from mape_maker.utilities.SimParams import SimParams


class MapeMaker:
    """A package to simulate actuals or forecasts scenarios for a given mean absolute percent error

    Attributes:
        xyid (:obj:`XYID`): the input dataset with values of actuals and forecasts for specified datetime.
        logger (:obj:`Logger`): the logger to use to display messages to the user during the process
        sid (:obj:`SID`): the simulation input dataset initiated in the function simulate, formatted xyid with the
            exception that one column can be missing for operational purpose.

    """
    __version__ = "2.1"

    def __init__(self, logger: Logger, xyid_path: str, ending_feature: str = "actuals", xyid_load_pickle: bool = False,
                 input_start_dt: str = None, input_end_dt: str = None, a: float = 4, base_process="ARMA", scale_by_capacity: float = None) -> None:
        """Init statement of MapeMaker class

        Args:
            logger (Logger): the type of logger you want to use for all the process of MapeMaker.
            xyid_path (str): the filepath to the input data csv.
            ending_feature (str, optional): the feature you wish to simulate (either "actuals" or "forecasts"). Defaults
                to "actuals".
            xyid_load_pickle (bool): if you want to load the pickle file storing the estimated coefficients estimated
                in a previous run. Defaults to False.
            input_start_dt (str): start date of the input data if you want to select a subset of the csv file. Defaults
                to None.
            input_end_dt (str): end date of the input data if you want to select a subset of the csv file. Defaults
                to None.
            a (float): percent of the input dataset to use on the right and left of the conditional distribution
                coefficient estimation.
            scale_by_capacity (float): if you want MAPE to be with respect to the capacity, enter the capacity; if you want
                the capacity to be the max of actuals(x), enter 0. Defaults to None, meaning the MAPE is with respect to actuals

        """
        self.logger = logger
        self.ending_feature = ending_feature
        self.xyid: XYID = XYID(a, base_process=base_process, csv_filepath=xyid_path, start_date=input_start_dt,
                               end_date=input_end_dt,  ending_feature=ending_feature, xyid_load_pickle=xyid_load_pickle,
                               logger=logger, scale_by_capacity=scale_by_capacity)  #: step 1: load the XYID, estimate distrib and ARMA
        #: step 2: create an object SID. Will be initiated for simulation
        self.sid: SID = type('SID', (), {})()

    def simulate(self, sid_file_path: str = None, simulation_start_dt: str = None, simulation_end_dt: str = None,
                 output_dir: str = None, list_of_date_ranges: List[str] = None, seed: int = None, **kwargs) -> pd.DataFrame:
        """simulate scenarios

        Args:
            sid_file_path (str): the filepath to the simulation input data csv. Defaults to None. In that case, the sid
                will be a subset of the xyid.
            simulation_start_dt: start date of the scenarios. Defaults to None. In that case, the start_date is the
                first date of the sid.
            simulation_end_dt: end date of the scenarios. Defaults to None. In that case the end_date is the last
                date of the sid.
            output_dir: the path where to store the results csv. Defaults to None. In that case, no output is
                produced.
            list_of_date_ranges : list of [start_date, end_date] over which to simulate
            seed : random seed
            **kwargs: Simulation parameters. They will be given in input of the Simulation Parameters.

        Returns:
            results (pd.DataFrame): a dataframe with the simulations as columns and sid datetime index as index

        """
        np.random.seed(seed=seed)
        # TODO create multiple SID for corresponding start and end date in list of date_ranges
        if list_of_date_ranges is None:
            self.sid = SID(logger=self.logger, csv_filepath=sid_file_path, dataset=self.xyid, start_date=simulation_start_dt,
                           end_date=simulation_end_dt, ending_feature=self.ending_feature)  #: initiate the SID from a new csv or from xyid
            #: create a SimParams object and adjust distributions
            self.create_save_simparams(**kwargs)
            results = self.sid.simulate_multiple_scenarios(
                output_dir, **kwargs)  #: simulate and store the scenarios

        return results

    def create_save_simparams(self, **kwargs: object) -> None:
        """constructs a SimParams object and save it to the sid

        Args:
            **kwargs: simulation parameters. They will pass to the constructor of SimParams.

        """
        sim_params = SimParams(self.xyid, self.sid, self.logger, **kwargs)
        self.sid.set_sim_params(sim_params)

    def get_results(self) -> List[pd.DataFrame]:
        """returns the list of the different simulations of scenarios

        Returns:

        """
        return self.sid.simulations


if __name__ == "__main__":
    import logging
    from datetime import datetime
    from mape_maker.utilities.Scenarios import Scenarios
    logger = logging.getLogger('make-maker')
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    mare_embedder = MapeMaker(logger=logger, ending_feature="forecasts", xyid_path="samples/rts_gmlc/wind_operations_example.csv",
                              input_start_dt=str(
                                  datetime(year=2020, month=2, day=1, hour=0, minute=0, second=0)),
                              input_end_dt=str(
                                  datetime(year=2020, month=8, day=31, hour=23, minute=0, second=0)),
                              xyid_load_pickle=True)
    curvature_parameters = [{
        "MIP": 0.05,
        "time_limit": 15,
        "curvature_target": None,
        "solver": "gurobi",
    }, None]
    results = mare_embedder.simulate(n=1,
                                     simulation_start_dt=str(
                                         datetime(year=2020, month=11, day=1, hour=0, minute=0, second=0)),
                                     simulation_end_dt=str(datetime(year=2020, month=11, day=7, hour=0, minute=0, second=0)))
    from mape_maker.utilities.Scenarios import Scenarios
    Scenarios(logger=logger, X=mare_embedder.sid.x_t,
              Y=mare_embedder.sid.y_t,
              results=results,
              target_mare=mare_embedder.sid.SimParams.r_tilde,
              f_mare=mare_embedder.xyid.dataset_info.get("r_m_hat"))
