import tempfile
import pyutilib.th as unittest
import sys
import os.path
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import shutil
import datetime
from datetime import datetime
import shutil
import mape_maker
dir_sep = '/'
from mape_maker import __main__ as mapemain
# whether to skip the last two tests
quick_test = False
# whether to run only one example
skip_all_but_one = False

class TestUM(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # find the path to mape_maker
        p = str(mape_maker.__path__)
        l = p.find("'")
        r = p.find("'", l + 1)
        mape_maker_path = p[l + 1:r]
        # make a temp dir
        self.temp_dir = tempfile.mkdtemp()
        sys.path.insert(1, self.temp_dir)
        # change to the temp directory
        os.chdir(self.temp_dir)
        self.cwd = os.getcwd()
        print("temporary directory:", self.cwd)
        # path to the CAISO wind data
        self.wind_data = mape_maker_path + dir_sep + "samples" + \
                         dir_sep + "wind_total_forecast_actual_070113_063015.csv"

    def create_temp_dir(self):
        """
        create a sub temporary directory inside the main temporary directory
        to save the output file
        :return: sub_directory
        """
        sub_directory = tempfile.mkdtemp(dir=self.temp_dir)
        print("sub temporary directory:", sub_directory)
        return sub_directory

    def _basic_dict(self):
        basedict = {"input_file": "",
                    "second_file": None,
                    "target_mape": None,
                    "simulated_timeseries": "actuals",
                    "base-process": "ARMA",
                    "a": 4,
                    "output_dir": None,
                    "number_simulations": 1,
                    "input_start_dt": None,
                    "input_end_dt": None,
                    "simulation_start_dt": None,
                    "simulation_end_dt": None,
                    "title": None,
                    "seed": None,
                    "load_pickle": False,
                    "curvature": None,
                    "time_limit": 3600,
                    "curvature_target": None,
                    "mip_gap": 0.3,
                    "solver": "gurobi",
                    "latex_output": False,
                    "show": True,
                    "verbosity": 2,
                    "verbosity_output": None
                    }
        return basedict

    def test_wind_actuals_iid_with_dates(self):
        print("Running ", str(self.id()).split('.')[2])
        # here is the command :
        # python -m mape_maker "mape_maker/samples/wind_total_forecast_actual_070113_063015.csv" -st "actuals" -n 3 -bp "iid" -o "wind_actuals_iid" -is "2014-7-1 00:00:00" -ie "2014-8-1 00:00:00" -sd "2014-7-2 00:00:00" -ed "2014-7-31 00:00:00" -s 1234
        parm_dict = self._basic_dict()
        parm_dict["input_file"] = self.wind_data
        parm_dict["simulated_timeseries"] = "actuals"
        parm_dict["number_simulations"] = 3
        parm_dict["base-process"] = "iid"
        parm_dict["input_start_dt"] = datetime(year=2014, month=7, day=1, hour=0, minute=0, second=0)
        parm_dict["input_end_dt"] = datetime(year=2014, month=8, day=1, hour=0, minute=0, second=0)
        parm_dict["simulation_start_dt"] = datetime(year=2014, month=7, day=2, hour=0, minute=0, second=0)
        parm_dict["simulation_end_dt"] = datetime(year=2014, month=7, day=31, hour=0, minute=0, second=0)
        parm_dict["output_dir"] = "wind_actuals_iid"
        parm_dict["seed"] = 1234
        parm_list = list(parm_dict.values())
        mapemain.main_func(*parm_list)
        # add a new column to compare two simulations
        # step 1 : read the output file
        # step 2 : convert the output file into dataframe
        # step 3 : add a new column called "simulation_1_minus_2"
        # step 4 : save the new output file and create a graph to show the differences
        csv_path = self.temp_dir + dir_sep + parm_dict["output_dir"] + dir_sep + "*.csv"
        output_file = glob.glob(csv_path)
        df = pd.read_csv(output_file[0], index_col=0)
        df["simulation_1_minus_2"] = df["simulation_n_1"] - df["simulation_n_2"]
        df.index.name = 'dates'
        new_output_file_path = self.temp_dir + dir_sep + parm_dict["output_dir"] \
                               + dir_sep + "simulation_comparison.csv"
        plt.figure(1)
        plt.scatter(df.index, df["simulation_1_minus_2"], s=2)
        plt.xlabel("dates")
        plt.ylabel("simulation differences")
        plot_path = self.temp_dir + dir_sep + parm_dict["output_dir"] \
                    + dir_sep + "plot"
        plt.savefig(plot_path)
        df.to_csv(new_output_file_path)
        # save the output dir to the sub temporary directory
        output_dir_path = self.temp_dir + dir_sep + parm_dict["output_dir"]
        shutil.move(output_dir_path, self.create_temp_dir())

    @unittest.skipIf(skip_all_but_one,
                     "skipping the second tests")
    def test_wind_actuals_ARMA(self):
        print("Running ", str(self.id()).split('.')[2])
        # here is the command :
        # python -m mape_maker "mape_maker/samples/wind_total_forecast_actual_070113_063015.csv" -st "actuals" -n 3 -bp "ARMA" -o "wind_actuals_ARMA_2" -s 1234
        parm_dict = self._basic_dict()
        parm_dict["input_file"] = self.wind_data
        parm_dict["simulated_timeseries"] = "actuals"
        parm_dict["number_simulations"] = 3
        parm_dict["base-process"] = "ARMA"
        parm_dict["output_dir"] = "wind_actuals_ARMA"
        parm_list = list(parm_dict.values())
        mapemain.main_func(*parm_list)
        # add a new column to compare two simulations
        # step 1 : read the output file
        # step 2 : convert the output file into dataframe
        # step 3 : add a new column called "simulation_1_minus_2"
        # step 4 : save the new output file and create a graph to show the differences
        csv_path = self.temp_dir + dir_sep + parm_dict["output_dir"] + dir_sep + "*.csv"
        output_file = glob.glob(csv_path)
        df = pd.read_csv(output_file[0], index_col=0)
        df["simulation_1_minus_2"] = df["simulation_n_1"] - df["simulation_n_2"]
        df.index.name = 'dates'
        new_output_file_path = self.temp_dir + dir_sep + parm_dict["output_dir"] \
                               + dir_sep + "simulation_comparison.csv"
        plt.figure(2)
        plt.scatter(df.index, df["simulation_1_minus_2"], s=2)
        plt.xlabel("dates")
        plt.ylabel("simulation differences")
        plot_path = self.temp_dir + dir_sep + parm_dict["output_dir"] \
                    + dir_sep + "plot"
        plt.savefig(plot_path)
        df.to_csv(new_output_file_path)
        # save the output dir to the sub temporary directory
        output_dir_path = self.temp_dir + dir_sep + parm_dict["output_dir"]
        shutil.move(output_dir_path, self.create_temp_dir())

    @unittest.skipIf(quick_test or skip_all_but_one,
                     "skipping the third tests")
    def test_wind_forecasts_iid_with_dates(self):
        print("Running ", str(self.id()).split('.')[2])
        # here is the command :
        # python -m mape_maker "mape_maker/samples/wind_total_forecast_actual_070113_063015.csv" -st "forecasts" -n 5 -bp "iid" --output_dir "wind_forecasts_iid" -is "2014-6-1 00:00:00" -ie "2014-6-30 00:00:00" -sd "2014-6-2 01:00:00" -ed "2014-6-30 00:00:00" --target_mape 30 -s 1234
        parm_dict = self._basic_dict()
        parm_dict["input_file"] = self.wind_data
        parm_dict["simulated_timeseries"] = "forecasts"
        parm_dict["number_simulations"] = 5
        parm_dict["base-process"] = "iid"
        parm_dict["output_dir"] = "wind_forecasts_iid"
        parm_dict["simulation_start_dt"] = datetime(year=2014, month=6, day=2, hour=1, minute=0, second=0)
        parm_dict["simulation_end_dt"] = datetime(year=2014, month=6, day=30, hour=0, minute=0, second=0)
        parm_dict["input_start_dt"] = datetime(year=2014, month=6, day=1, hour=0, minute=0, second=0)
        parm_dict["input_end_dt"] = datetime(year=2014, month=6, day=30, hour=0, minute=0, second=0)
        parm_dict["target_mape"] = 30
        parm_dict["seed"] = 1234
        parm_list = list(parm_dict.values())
        mapemain.main_func(*parm_list)
        # add a new column to compare two simulations
        # step 1 : read the output file
        # step 2 : convert the output file into dataframe
        # step 3 : add a new column called "simulation_1_minus_2"
        # step 4 : save the new output file and create a graph to show the differences
        csv_path = self.temp_dir + dir_sep + parm_dict["output_dir"] + dir_sep + "*.csv"
        output_file = glob.glob(csv_path)
        df = pd.read_csv(output_file[0], index_col=0)
        df["simulation_1_minus_2"] = df["simulation_n_1"] - df["simulation_n_2"]
        df.index.name = 'dates'
        new_output_file_path = self.temp_dir + dir_sep + parm_dict["output_dir"] \
                               + dir_sep + "simulation_comparison.csv"
        plt.figure(3)
        plt.scatter(df.index, df["simulation_1_minus_2"], s=2)
        plt.xlabel("dates")
        plt.ylabel("simulation differences")
        plot_path = self.temp_dir + dir_sep + parm_dict["output_dir"] \
                    + dir_sep + "plot"
        plt.savefig(plot_path)
        df.to_csv(new_output_file_path)
        # save the output dir to the sub temporary directory
        output_dir_path = self.temp_dir + dir_sep + parm_dict["output_dir"]
        shutil.move(output_dir_path, self.create_temp_dir())

    @unittest.skipIf(quick_test or skip_all_but_one,
                     "skipping the fourth tests")
    def test_wind_forecasts_ARMA_with_dates(self):
        """
        This test will fail because the simulation date range is too small
        :return:
        """
        print("Running ", str(self.id()).split('.')[2])
        # here is the command :
        # python -m mape_maker "mape_maker/samples/wind_total_forecast_actual_070113_063015.csv" -st "forecasts" -n 5 -bp "ARMA" -o "wind_forecasts_ARMA" -is "2014-6-1 00:00:00" -ie "2014-6-30 00:00:00" -sd "2014-6-2 01:00:00" -ed "2014-6-29 00:00:00" -t 30 -s 1234
        parm_dict = self._basic_dict()
        parm_dict["input_file"] = self.wind_data
        parm_dict["simulated_timeseries"] = "forecasts"
        parm_dict["number_simulations"] = 5
        parm_dict["base-process"] = "ARMA"
        parm_dict["output_dir"] = "wind_forecasts_ARMA"
        parm_dict["simulation_start_dt"] = datetime(year=2014, month=6, day=2, hour=1, minute=0, second=0)
        parm_dict["simulation_end_dt"] = datetime(year=2014, month=6, day=29, hour=0, minute=0, second=0)
        parm_dict["input_start_dt"] = datetime(year=2014, month=6, day=1, hour=0, minute=0, second=0)
        parm_dict["input_end_dt"] = datetime(year=2014, month=6, day=30, hour=0, minute=0, second=0)
        parm_dict["target_mape"] = 30
        parm_dict["seed"] = 1234
        parm_list = list(parm_dict.values())
        mapemain.main_func(*parm_list)
        # add a new column to compare two simulations
        # step 1 : read the output file
        # step 2 : convert the output file into dataframe
        # step 3 : add a new column called "simulation_1_minus_2"
        # step 4 : save the new output file and create a graph to show the differences
        csv_path = self.temp_dir + dir_sep + parm_dict["output_dir"] + dir_sep + "*.csv"
        output_file = glob.glob(csv_path)
        df = pd.read_csv(output_file[0], index_col=0)
        df["simulation_1_minus_2"] = df["simulation_n_1"] - df["simulation_n_2"]
        df.index.name = 'dates'
        new_output_file_path = self.temp_dir + dir_sep + parm_dict["output_dir"] \
                               + dir_sep + "simulation_comparison.csv"
        plt.figure(4)
        plt.scatter(df.index, df["simulation_1_minus_2"], s=2)
        plt.xlabel("dates")
        plt.ylabel("simulation differences")
        plot_path = self.temp_dir + dir_sep + parm_dict["output_dir"] \
                    + dir_sep + "plot"
        plt.savefig(plot_path)
        df.to_csv(new_output_file_path)
        # save the output dir to the sub temporary directory
        output_dir_path = self.temp_dir + dir_sep + parm_dict["output_dir"]
        shutil.move(output_dir_path, self.create_temp_dir())

if __name__ == "__main__":
    unittest.main()