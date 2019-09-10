import datetime
from mape_maker.utilities import simulation, fitting_distribution, ARMA_fit
from mape_maker.utilities.df_utilities import pre_treat, find_longest_index_sequence, plot_from_date
import numpy as np
import os.path
#from latex_outputer import to_latex
import pickle

file_path = os.path.abspath(os.path.dirname(__file__))
loading_bar = "-"*60


class MapeMaker:
    __version__ = "0.9"
    path_to_test = {
        "BPA": "samples/2012-2013_BPA_forecasts_actuals.csv",
        "CAISO": "samples/wind_total_forecast_actual_070113_063015.csv",
    }

    """
    Class embeding the mare_embedder_frame, the results and the main function needed to create scenarios based on a
    specific mare
    """

    def __init__(self, path="", name="", ending_feature="actuals", load_pickle=False, seed=None, a=4,
                 input_start_dt=None, input_end_dt=None):
        """

        :param path: path to the csv containing datetime - actuals - forecasts
        :param name: csv examples
            - "BPA",
            - "CAISO"
        :param ending_feature: the target of the simulation
            - "actuals",
            - "forecasts"
        :param load: if True and if parameters already computed, will load the vectors giving the estimated parameters
        :param seed: seed used for simulation if none will be random
        :param a: percent/2 of data used for the estimation sample
        """
        if path == "":
            path = os.path.join(file_path, MapeMaker.path_to_test[name])
        self.y = "actuals" if ending_feature == "actuals" else "forecasts"
        self.x = "forecasts" if ending_feature == "actuals" else "actuals"
        """
        Saved preference
        """
        self.name = name if path == "" else path.split("/")[-1]
        self.name = self.name.split(".")[0] + "_to{}".format(self.y)
        if seed is not None:
            self.seed = int(seed)
        else:
            self.seed = seed
        # set the seed here just to make sure it gets done
        np.random.seed(self.seed)
        self.outfile_estimation_parameters = os.path.join(file_path,
                                                          "utilities/stored_vectors/{}_parameters.pkl".format(
                                                              self.name))
        """
        Creations of errors, relative errors columns,
        Zero_df Vs all_df
        """
        full_df = pre_treat(path=path, type_of_simulation=ending_feature)
        self.operations = False
        if len(full_df[full_df[self.y].isna()]) > 0:
            print("-"*60 + "\n\n There are some missing {} => OPERATION MODE\n".format(self.y))
            index_not_na = full_df[~full_df[self.y].isna()].index
            df = full_df.loc[index_not_na]
            self.operations = True
        else:
            df = full_df
        if input_start_dt is not None and input_end_dt is not None:
            df = df.loc[input_start_dt:input_end_dt]
        self.full_df = full_df
        self.x_timeseries, self.errors, self.y_timeseries = df[self.x], df["errors"], df[self.y]
        self.d = self.compute_second_dif()
        ares = abs(self.errors)/self.x_timeseries
        self.mare = np.mean(ares)
        self.cap = max(self.x_timeseries)
        """
        Estimation of parameters
        """
        self.datasetx = fitting_distribution.make_datasetx(self.x_timeseries)
        if load_pickle:
            try:
                self.pload()
                print(loading_bar + "\nEstimation parameters for xbar have been loaded")
            except Exception as e:
                print(e)
                print(loading_bar + "\nCouldn't load - Estimation parameters for xbar are being computed")
                self.s_x_a = fitting_distribution.get_s_hat_datasetx_a(self.x_timeseries, self.datasetx, self.errors,
                                                                       self.cap, a=a)
                print("We save those parameters")
                self.save()
        else:
            print(loading_bar + "\nEstimation parameters for xbar are being computed")
            self.s_x_a = fitting_distribution.get_s_hat_datasetx_a(self.x_timeseries,
                                                                   self.datasetx, self.errors, self.cap, a=a)
            print("We save those parameters")
            self.save()
        print(loading_bar + "\nEstimation parameters for x in datasetx are being infered")
        self.s_x = fitting_distribution.get_s_x(self.s_x_a, self.datasetx)
        self.first_estimated_x = list(self.s_x_a.keys())[0]
        p = np.where(np.array(self.datasetx) > self.first_estimated_x)[0][0]/len(self.datasetx)
        print("The first parameters have been estimated at {}, thus {}% of the low power data have "
              "the same conditional distribution".format(self.first_estimated_x, '%.1f' % (100*p)))
        """
        Estimation of the weight function
        """
        print(loading_bar + "\nEstimation of the target function m_hat and of the maximum target function m_max")
        # we could think of storing m_max which requires a time of computation
        self.m_hat, self.m_max = fitting_distribution.get_maes_from_parameters(self.s_x, self.cap)
        self.r_m_hat = fitting_distribution.get_r_from_m_hat(self.m_hat)
        self.r_m_max = fitting_distribution.get_r_from_m_hat(self.m_max)
        print(loading_bar + "\nMax attainable for full dataset {}%".format("%2.f" % (100*self.r_m_max)))
        print(loading_bar + "\nEstimation of the weight function om_X")
        self.om_x = fitting_distribution.create_weight_function(self.m_hat, self.r_m_hat)

        """
        Estimating the Base Process then ARMA process
        """
        self.Z_hat = None
        self.solver_arma = None

        """
        Getting the simulation functions
        """
        print(loading_bar + "\nInitializing the simulation functions with the estimations")
        self.datasetsid = self.datasetx
        self.x_timeseries_sid = self.full_df[self.x]
        self.m_tilde = self.m_hat
        self.r_tilde_max = self.r_m_max
        self.e_score = 1
        self.om_tilde = self.om_x
        self.s_x_tilde = self.s_x
        self.r_tilde = self.r_m_hat
        self.start_date, self.end_date = self.x_timeseries.index[0], self.x_timeseries.index[-1]
        print("\n"+"*"*30 + " PREPROCESSING DONE - READY TO SIMULATE " + "*"*30 + "\n")

        """
        Curvature parameters
        """
        self.curvature_parameters = {}

        """
        Results
        """
        self.results, self.simulated_errors, self.saved_scores = {}, {}, {}

    def create_arma_process(self):
        """
        estimate the base process and create a solver object to find the ARMA coefficients
        :return:
        """
        print(loading_bar + "\nEstimation of the base process")
        self.Z_hat = ARMA_fit.estimate_base_process(self.x_timeseries, self.errors, self.s_x)
        print(loading_bar)
        self.solver_arma = ARMA_fit.SolverARMA(self.Z_hat, self.name)

    def save(self):
        with open(self.outfile_estimation_parameters, 'wb') as f:
            pickle.dump(self.s_x_a, f, pickle.HIGHEST_PROTOCOL)
        return True

    def pload(self):
        with open(self.outfile_estimation_parameters, 'rb') as f:
            self.s_x_a = pickle.load(f)
        return True

    def compute_second_dif(self):
        """
        Compute the mean of the absolute of the second differences of the output of the simulation
        :return:
        """
        y = self.y_timeseries.diff(1).diff(1).dropna()
        self.d = np.mean(abs(y))
        return self.d

    def has_results(self):
        return len(self.results) != 0

    def scrap_results(self):
        self.results = []

    def has_artafit(self):
        return self.solver_arma is not None

    def get_simulation_parameters(self, r_tilde, x_timeseries_sid):
        """
        from the target mare and the dataset_SID :
            * find the target MAE to get from each of the conditional distributions
            * compute the parameters of the beta distributions to obtain the target MAEs
        :param r_tilde:
        :param x_timeseries_sid:
        :return: s_x_tilde
        """
        print(loading_bar + "\nDetermination of the weight function om_tilde")
        self.om_tilde, self.e_score = fitting_distribution.create_sid_weight_function(self.om_x, x_timeseries_sid)
        print(loading_bar + "\nDetermination of the maximum of mare attainable")
        self.r_tilde_max = fitting_distribution.infer_r_tilde_max(self.m_max, self.om_tilde)
        print(loading_bar + "\nDetermination of the Plausability score and the r_tilde_max")
        flag_error = False
        if abs(self.e_score - 1) < 0.1:
            s = " == 1, the SID is balanced like the datasetx"
        elif self.e_score > 1:
            s = " > 1, there is a prevalence of low power input in the SID"
        else:
            s = " < 1, there is a prevalence of high power input in the SID"
            inequality = " < " if r_tilde > self.r_tilde_max else " > "
            s += "\nMaximum of mare attainable with this score is {}".format("%.2f" % self.r_tilde_max) + \
                       inequality + "target {}".format("%.2f" % r_tilde)
            if r_tilde > self.r_tilde_max:
                flag_error = True
                s += "\nWARNING YOU ASKED FOR A TOO STRONG R TILDE"
                s += "\n     => Either change your r_tilde"
                s += "\n     => Either change your SID so the e_score increases"
        print("Plausibility score = {} ".format('%.3f' % self.e_score) + s)
        if flag_error:
            return None
        print(loading_bar + "\nDetermination of the target function m_tilde")
        self.m_tilde = fitting_distribution.get_maes_from_weight_target(self.om_tilde, r_tilde, self.m_max)
        print(loading_bar + "\nComputation of the new simulation parameters")
        self.s_x_tilde, nb_errors = fitting_distribution.get_s_tilde_sid(self.s_x, self.m_tilde, self.m_hat, self.m_max,
                                                                         self.cap)
        print(loading_bar + "\n{} simulation distributions did not suceed, the plausibility score "
              "is : {}".format(nb_errors, '%.3f' % self.e_score))
        closest_zero = list(self.s_x_tilde.keys())[1]
        print(loading_bar + "\nApplying continuity to the parameters on 0, with closest x value = {}".format(
            "%.2f" % closest_zero))
        self.s_x_tilde[0] = self.s_x_tilde[closest_zero]
        print(loading_bar)
        return self.s_x_tilde, nb_errors

    def simulate(self, target_mare=None, base_process=None, n=1, full_dataset=False, output_dir=None, seed=None,
                 list_of_date_ranges=(datetime.datetime(2013, 8, 1), datetime.datetime(2014, 1, 1),),
                 curvature_parameters=None, latex=False):
        """
        Compute and stores simulation results in self.results
        :param target_mare: requested mare by the user
        :param base_process: underlying process that produces autocorrelation
            - "iid" : simulation of a vector of independent and identically distributed random variable in [0,1]
            - "ARMA" : simulation of a vector with an ARMA process fitted on training data
        :param n: number of simulations to compute
        :param full_dataset: if True will compute simulation over all the dataset, x_sid = x
        :param list_of_date_ranges: otherwise need a list of date ranges on which to compute the simulations,
                                    example [[datetime.datetime(2018,1,1), datetime.datetime(2018,2,1)]]
        :param curvature_parameters: if none, no correction for curvature is added, otherwise the dict will be
                                    used to perform the optimization. The dict contains :
                - "MIP" : default 0.05,
                - "time_limit" : default 120 s,
                - "curvature_target: if None, will take the curvature of the dataset as target
                - "solver" : default "gurobi"
        :param seed: random seed
        :param output_dir: will save the csv in "output_dir" if output_dir is not None (dlw TBD)
        :param latex: create a tex document with table of scores
        :return:
        """
        if target_mare is None:
            tg = " of the empirical dataset"
            # We take the last target used to prevent from recomputing all the weights
            target_mare = self.r_tilde
        else:
            tg = "{}%".format('%.1f' % (100*target_mare))
        name_simul = "target mape {}, base_process {} ".format(tg, base_process)
        if curvature_parameters is not None:
            name_simul += "+ curvature"
        if seed is None:
            seed = self.seed
        if full_dataset:
            list_of_date_ranges = [[self.x_timeseries.index[0], self.x_timeseries.index[-1]]]
        else:
            if list_of_date_ranges is None:
                list_of_date_ranges = [[self.x_timeseries.index[0], self.x_timeseries.index[-1]]]
            elif len(np.array(list_of_date_ranges).shape) == 1:
                list_of_date_ranges = [list_of_date_ranges]
            elif len(np.array(list_of_date_ranges).shape) == 2 and list_of_date_ranges[0][0] is None:
                start_ind = find_longest_index_sequence(self.x_timeseries.index, 150 * 24)
                start_date, end_date = self.x_timeseries.index[start_ind], self.x_timeseries.index[start_ind + 150*24]
                list_of_date_ranges = [[start_date, end_date]]

        s_ = "*" * 30 + "*" * len(" PREPROCESSING DONE - READY TO SIMULATE ") + "*" * 30
        n_s = len(s_)
        print(s_)
        s = "Simulating from {} to {}".format(list_of_date_ranges[0][0], list_of_date_ranges[0][1])
        s = "*" + " " * ((n_s - 2 - len(s)) // 2) + s + " " * ((n_s - 2 - len(s)) // 2) + "*"
        print(s)
        print(s_ + "\n")

        if self.seed is not None:
            seeds = [self.seed+i for i in range(n)]
            name_simul += " seed:{}".format(self.seed)
        else:
            seeds = [None]*n
        if base_process == "ARMA":
            if self.solver_arma is None:
                self.create_arma_process()
            base_process = self.solver_arma
        else :
            base_process = None
        for l in list_of_date_ranges:
            start_date, end_date = l
            # DLW: try to get the efficiency back (this could be skipped for all data)
            ###if target_mare != self.r_tilde or (start_date != self.start_date) or (end_date != self.end_date):
            self.start_date, self.end_date = start_date, end_date
            self.r_tilde = target_mare
            self.x_timeseries_sid = self.full_df[self.x][self.start_date:self.end_date]
            self.datasetsid = fitting_distribution.make_datasetx(self.x_timeseries_sid)
            self.s_x_tilde, nb_errors = self.get_simulation_parameters(target_mare, self.datasetsid)
            if self.s_x_tilde is None:
                return False, None
            ### end if
            if curvature_parameters is not None:
                curvature_parameters["Y"] = self.full_df[self.y][self.start_date:self.end_date]
                curvature_parameters["x"] = self.x_timeseries_sid
                curvature_parameters["name"] = self.name
                if "curvature_target" not in curvature_parameters or curvature_parameters["curvature_target"] is None:
                    self.compute_second_dif()
                    curvature_parameters["curvature_target"] = self.d
                self.curvature_parameters = curvature_parameters
            results, errors = simulation.simulate_multiple_scenarios(self.x_timeseries_sid,
                                                                     self.s_x_tilde, cap=self.cap, n=n,
                                                                     base_process=base_process, seeds=seeds,
                                                                     curvature_parameters=curvature_parameters)
            params_simul = self.create_parameters_simulation(n, base_process, curvature_parameters, output_dir)
            self.results[name_simul] = results
            self.simulated_errors[name_simul] = errors
            if self.operations is False:
                self.saved_scores[name_simul] = simulation.score_simulations_from_measures(
                                                            self.measures_simulations(results, params_simul))
            if latex:
                print("Latex output not supported for now")
                # to_latex.generate_unique(self.saved_scores, results, 0.01)

        return self.saved_scores, nb_errors

    def create_parameters_simulation(self, n, base_process, curvature_parameters, output_dir):
        """
        Create a dict of the parameters used for the simulation. Used for the latex output.
        :param n:
        :param base_process:
        :param curvature_parameters:
        :param output_dir:
        :return:
        """
        params_simulation = {
            "x": self.x, "y": self.y,
            "input_file": self.name,
            "target_mare": self.r_tilde,
            "date_range": [self.start_date, self.end_date],
            "seed": self.seed,
            "number_of_simulations": n,
            "base_process": base_process,
            "curvature_parameters": curvature_parameters,
            "output_dir": output_dir,
        }

        return params_simulation

    def save_output(self, name_simul, output_file):
        """
        Save the name_simul in output_file (CSV)
        :param name_simul:
        :param output_file:
        :return:
        """
        if output_file is not None:
            print("-" * 30 + "storing the output for {} in {}".\
                  format(name_simul, output_file) + "-" * 30)
            # delete this line file_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
            # delete this line path = os.path.join(file_path, "output/" + output_file)
            self.results[name_simul].to_csv(output_file)
        return True

    def save_all_outputs(self, output_dir):
        """
        Make a new output dir and put a csv file for each result in it
        :param output_dir:
        :return:
        """
        if output_dir is None:
            return
        try:
            os.mkdir(output_dir)
        except FileExistsError:
            raise RuntimeError("Directory {} already exists".format(output_dir))
        for name_simul in self.results:
            basename = name_simul.replace(',', '-')
            basename = basename.replace(':', '-')
            basename = basename.replace(' ', '_')
            outfile = output_dir + os.sep + basename + ".csv"
            self.save_output(name_simul, outfile)

    def measures_simulations(self, results, params_simul):
        """
        Compute the measures over the simulation and the SID :
            * MARE
            * Auto-correlation
            * Second-difference
        :param results:
        :param params_simul:
        :return:
        """
        result_mares, observed_mare = simulation.check_simulation_mare(self.x_timeseries, self.y_timeseries,
                                                                       results, self.r_tilde)
        auto_cor_simul, auto_cor_real = simulation.check_simulation_auto_correlation(self.x_timeseries, self.errors,
                                                                                     results)
        d_simuls, observed_second_differences = simulation.check_simulation_curvature(self.y_timeseries, results)
        raw_measures = {
            "params_simulation": params_simul,
            "mares": {
                "target": self.r_tilde,
                "simulated": result_mares,
                "observed": observed_mare,
            },
            "auto-correlation": {
                "target": auto_cor_real,
                "simulated": auto_cor_simul
            },
            "second-differences": {
                "target": self.d,
                "simulated": d_simuls,
                "observed": observed_second_differences,
            },
            "Plausability_score": self.e_score
        }
        return raw_measures

    def plot_example(self, screen=0, title=None):
        if self.has_results():
            if self.operations:
                y = None
            else:
                y = self.y_timeseries
            plot_from_date(self.x_timeseries_sid, y, screen,
                           results=self.results, title=title,
                           target_mare=self.r_tilde, ending_features=self.y,
                           x_legend=self.x)
            return True
        else:
            print(loading_bar + "\nno results to plot\n" + loading_bar)
            return False


if __name__ == "__main__":
    print("main")

    """
    Showing all the options for the creation of the object
    """
    paths = ["samples/wind_total_forecast_actual_070113_063015.csv", "samples/2012-2013_BPA_forecasts_actuals.csv",
             "samples/operations_example.csv"]
    ending_features = ["actuals", "forecasts"]
    mare_embedder = MapeMaker(path=paths[2], ending_feature=ending_features[0], load_pickle=False, seed=None)

    """
    Showing all the options for the simulation
    """
    curvature_parameters = [{
        "MIP": 0.05,
        "time_limit": 15,
        "curvature_target": None,
        "solver": "gurobi",
    }, None]
    base_processes = ["iid", "ARMA"]
    list_of_date_ranges = [[datetime.datetime(2014, 2, 16), datetime.datetime(2014, 2, 17)]]
    output_dir = "output"
    target_mares = {
        "actuals": [None, 0.2],
        "forecasts": [None, 2],
    }

    scores,nb_errors = mare_embedder.simulate(target_mare=target_mares[mare_embedder.y][0], base_process=base_processes[1], n=10,
                                    full_dataset=False, output_dir=None, seed=None,
                                    list_of_date_ranges=list_of_date_ranges,
                                    curvature_parameters=curvature_parameters[1],
                                    latex=False)
    if nb_errors > 0:
        print ("WARNING:")
        print ("   {} errors computing simulating distribution parameters".format(nb_errors))
        print ("   so the simulated MAPE may not match the target.")

    mare_embedder.plot_example()

