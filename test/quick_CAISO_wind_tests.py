import tempfile
import pyutilib.th as unittest
import sys
import os.path
import os
import glob
import pandas as pd
import shutil
import datetime
from datetime import datetime
import shutil
import mape_maker
dir_sep = '/'
from mape_maker import __main__ as mapemain
from collections.abc import Iterable
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

    def _basic_dict(self):
        basedict = {"input_file": "",
                    "target_mape": None,
                    "simulated_timeseries": "forecasts",
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
                    "curvature": False,
                    "time_limit": 3600,
                    "curvature_target": None,
                    "mip_gap": 0.3,
                    "solver": "gurobi",
                    "latex_output": False,
                    "show": True
                    }
        return basedict

    def create_temp_dir(self):
        """
        create a sub temporary directory inside the main temporary directory
        to save the output file
        :return: sub_directory
        """
        sub_directory = tempfile.mkdtemp(dir=self.temp_dir)
        print("sub temporary directory:", sub_directory)
        return sub_directory

    def test_with_known_error(self):
        """
        This test will fail because the simulation date range is too small
        :return:
        """
        print("Running ", str(self.id()).split('.')[2])
        # here is the command :
        # python -m mape_maker "mape_maker/samples/wind_total_forecast_actual_070113_063015.csv" -st "actuals" -n 2 -bp "ARMA" -o "wind_actuals_ARMA_1" -is "2014-6-1 00:00:00" -ie "2014-6-30 00:00:00" -sd "2014-6-27 01:00:00" -ed "2014-6-29 00:00:00" -s 1234
        parm_dict = self._basic_dict()
        parm_dict["input_file"] = self.wind_data
        parm_dict["simulated_timeseries"] = "actuals"
        parm_dict["number_simulations"] = 2
        parm_dict["base-process"] = "ARMA"
        parm_dict["output_dir"] = "wind_actuals_ARMA_1"
        parm_dict["simulation_start_dt"] = datetime(year=2014, month=6, day=27, hour=1, minute=0, second=0)
        parm_dict["simulation_end_dt"] = datetime(year=2014, month=6, day=29, hour=0, minute=0, second=0)
        parm_dict["input_start_dt"] = datetime(year=2014, month=6, day=1, hour=0, minute=0, second=0)
        parm_dict["input_end_dt"] = datetime(year=2014, month=6, day=30, hour=0, minute=0, second=0)
        parm_dict["seed"] = 1234
        parm_list = list(parm_dict.values())
        # the function should get an error message
        with self.assertRaises(TypeError) as context:
            mapemain.main_func(*parm_list)
            self.assertTrue(isinstance(context, Iterable))
            self.assertTrue('cannot unpack non-iterable NoneType object' in context)

    def test_wind_actuals_iid_with_dates(self):
        print("Running ", str(self.id()).split('.')[2])
        # here is the command :
        # python -m mape_maker "mape_maker/samples/wind_total_forecast_actual_070113_063015.csv" -st "actuals" -n 2 -bp "iid" -o "wind_actuals_iid" -is "2014-7-1 00:00:00" -ie "2014-8-1 00:00:00" -sd "2014-7-2 00:00:00" -ed "2014-7-31 00:00:00" -s 1234
        parm_dict = self._basic_dict()
        parm_dict["input_file"] = self.wind_data
        parm_dict["simulated_timeseries"] = "actuals"
        parm_dict["number_simulations"] = 2
        parm_dict["base-process"] = "iid"
        parm_dict["input_start_dt"] = datetime(year=2014, month=7, day=1, hour=0, minute=0, second=0)
        parm_dict["input_end_dt"] = datetime(year=2014, month=8, day=1, hour=0, minute=0, second=0)
        parm_dict["simulation_start_dt"] = datetime(year=2014, month=7, day=2, hour=0, minute=0, second=0)
        parm_dict["simulation_end_dt"] = datetime(year=2014, month=7, day=31, hour=0, minute=0, second=0)
        parm_dict["output_dir"] = "wind_actuals_iid"
        parm_dict["seed"] = 1234
        parm_list = list(parm_dict.values())
        mapemain.main_func(*parm_list)
        # save the output dir to the sub temporary directory
        output_plot_path = self.temp_dir + dir_sep + "mmFinalFig.png"
        output_dir_path = self.temp_dir + dir_sep + parm_dict["output_dir"]
        sub_temp_dir = self.create_temp_dir()
        shutil.move(output_plot_path, sub_temp_dir)
        shutil.move(output_dir_path, sub_temp_dir)

    @unittest.skipIf(quick_test or skip_all_but_one,
                     "skipping the third tests")
    def test_wind_actuals_ARMA(self):
        print("Running ", str(self.id()).split('.')[2])
        # here is the command :
        # python -m mape_maker "mape_maker/samples/wind_total_forecast_actual_070113_063015.csv" -st "actuals" -n 2 -bp "ARMA" -o "wind_actuals_ARMA_2" -s 1234
        parm_dict = self._basic_dict()
        parm_dict["input_file"] = self.wind_data
        parm_dict["simulated_timeseries"] = "actuals"
        parm_dict["number_simulations"] = 2
        parm_dict["base-process"] = "ARMA"
        parm_dict["output_dir"] = "wind_actuals_ARMA"
        parm_list = list(parm_dict.values())
        mapemain.main_func(*parm_list)
        # save the output dir to the sub temporary directory
        output_plot_path = self.temp_dir + dir_sep + "mmFinalFig.png"
        output_dir_path = self.temp_dir + dir_sep + parm_dict["output_dir"]
        sub_temp_dir = self.create_temp_dir()
        shutil.move(output_plot_path, sub_temp_dir)
        shutil.move(output_dir_path, sub_temp_dir)

    @unittest.skipIf(quick_test or skip_all_but_one,
                     "skipping the fourth tests")
    def test_wind_forecasts_iid_with_dates(self):
        print("Running ", str(self.id()).split('.')[2])
        # here is the command :
        # python -m mape_maker "mape_maker/samples/wind_total_forecast_actual_070113_063015.csv" -st "forecasts" -n 2 -bp "iid" --output_dir "wind_forecasts_iid" -is "2014-6-1 00:00:00" -ie "2014-6-30 00:00:00" -sd "2014-6-2 01:00:00" -ed "2014-6-30 00:00:00" --target_mape 30 -s 1234
        parm_dict = self._basic_dict()
        parm_dict["input_file"] = self.wind_data
        parm_dict["simulated_timeseries"] = "forecasts"
        parm_dict["number_simulations"] = 2
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
        # save the output dir to the sub temporary directory
        output_plot_path = self.temp_dir + dir_sep + "mmFinalFig.png"
        output_dir_path = self.temp_dir + dir_sep + parm_dict["output_dir"]
        sub_temp_dir = self.create_temp_dir()
        shutil.move(output_plot_path, sub_temp_dir)
        shutil.move(output_dir_path, sub_temp_dir)

    @unittest.skipIf(quick_test or skip_all_but_one,
                     "skipping the fifth tests")
    def test_wind_forecasts_ARMA_with_dates(self):
        """
        This test will fail because the simulation date range is too small
        :return:
        """
        print("Running ", str(self.id()).split('.')[2])
        # here is the command :
        # python -m mape_maker "mape_maker/samples/wind_total_forecast_actual_070113_063015.csv" -st "forecasts" -n 2 -bp "ARMA" -o "wind_forecasts_ARMA" -is "2014-6-1 00:00:00" -ie "2014-6-30 00:00:00" -sd "2014-6-2 01:00:00" -ed "2014-6-29 00:00:00" -t 30 -s 1234
        parm_dict = self._basic_dict()
        parm_dict["input_file"] = self.wind_data
        parm_dict["simulated_timeseries"] = "forecasts"
        parm_dict["number_simulations"] = 2
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
        # save the output dir to the sub temporary directory
        output_plot_path = self.temp_dir + dir_sep + "mmFinalFig.png"
        output_dir_path = self.temp_dir + dir_sep + parm_dict["output_dir"]
        sub_temp_dir = self.create_temp_dir()
        shutil.move(output_plot_path, sub_temp_dir)
        shutil.move(output_dir_path, sub_temp_dir)

    def get_the_first_and_last_num(self, output_dir_path):
        """
        this function will convert the output dir into dataframe
        and return the first and last numbers
        :param output_dir: the path to the output directory
               simulation_num: the number of simulation that the user set
        :return: the first and last number
        """
        csv_path = output_dir_path + dir_sep + "*.csv"
        output_file = glob.glob(csv_path)[0]
        df = pd.read_csv(output_file, index_col=0)
        # get the last simulation columns
        last_num = df.iloc[len(df.index) - 1, len(df.columns) - 1]
        print("last number : ", last_num)
        return last_num

    def test_output_dirs_with_seed(self):
        """
        In this test, we are going to compare the first and the
        last number in the output files to see whether it gives
        the same results with the given seed.
        :return: boolean
        """
        print("Running ", str(self.id()).split('.')[2])
        # initialize the parameters
        parm_dict = self._basic_dict()
        parm_dict["seed"] = 1234
        parm_dict["input_file"] = self.wind_data
        parm_dict["number_simulations"] = 2
        parm_dict["output_dir"] = "first_testing_folder_with_seed"
        parm_list = list(parm_dict.values())
        mapemain.main_func(*parm_list)
        output_plot_path1 = self.temp_dir + dir_sep + "mmFinalFig.png"
        output_dir_path1 = self.temp_dir + dir_sep + parm_dict["output_dir"]
        # get the first and last number
        l1 = self.get_the_first_and_last_num(output_dir_path1)
        sub_temp_dir1 = self.create_temp_dir()
        shutil.move(output_plot_path1, sub_temp_dir1)
        shutil.move(output_dir_path1, sub_temp_dir1)
        # run the test again to get the second output directory
        parm_dict["output_dir"] = "second_testing_folder_with_seed"
        parm_list = list(parm_dict.values())
        mapemain.main_func(*parm_list)
        output_plot_path2 = self.temp_dir + dir_sep + "mmFinalFig.png"
        output_dir_path2 = self.temp_dir + dir_sep + parm_dict["output_dir"]
        # get the first and last number
        l2 = self.get_the_first_and_last_num(output_dir_path2)
        sub_temp_dir2 = self.create_temp_dir()
        shutil.move(output_plot_path2, sub_temp_dir2)
        shutil.move(output_dir_path2, sub_temp_dir2)
        # check the first and last numbers
        if l1 != l2:
            print("If you set the seed, when you run the tests twice,"
                  " the numbers should be the same")
            sys.exit(1)

    def test_output_dirs_without_seed(self):
        """
        In this test, we are going to compare the first and the
        last number in the output files to see whether it gives
        the same results with the given seed.
        :return: boolean
        """
        print("Running ", str(self.id()).split('.')[2])
        # initialize the parameters
        parm_dict = self._basic_dict()
        parm_dict["input_file"] = self.wind_data
        parm_dict["number_simulations"] = 2
        parm_dict["output_dir"] = "first_testing_folder_without_seed"
        parm_list = list(parm_dict.values())
        mapemain.main_func(*parm_list)
        output_plot_path1 = self.temp_dir + dir_sep + "mmFinalFig.png"
        output_dir_path1 = self.temp_dir + dir_sep + parm_dict["output_dir"]
        # get the first and last number
        l1 = self.get_the_first_and_last_num(output_dir_path1)
        sub_temp_dir1 = self.create_temp_dir()
        shutil.move(output_plot_path1, sub_temp_dir1)
        shutil.move(output_dir_path1, sub_temp_dir1)
        # run the test again to get the second output directory
        parm_dict["output_dir"] = "second_testing_folder_without_seed"
        parm_list = list(parm_dict.values())
        mapemain.main_func(*parm_list)
        output_plot_path2 = self.temp_dir + dir_sep + "mmFinalFig.png"
        output_dir_path2 = self.temp_dir + dir_sep + parm_dict["output_dir"]
        # get the first and last number
        l2 = self.get_the_first_and_last_num(output_dir_path2)
        sub_temp_dir2 = self.create_temp_dir()
        shutil.move(output_plot_path2, sub_temp_dir2)
        shutil.move(output_dir_path2, sub_temp_dir2)
        # check the first and last numbers
        if l1 == l2:
            print("If you don't set the seed, when you run the tests twice,"
                  " the numbers shouldn't be the same")
            sys.exit(1)

    def test_simulation_and_input_dates(self):
        """
        python -m mape_maker "mape_maker/samples/wind_total_forecast_actual_070113_063015.csv" -is "2014-6-2 00:00:00" -ie "2014-6-30 00:00:00" -sd "2014-6-1 01:00:00" -ed "2014-6-30 00:00:00"
        This test is used to make sure if the simulation start date is earlier
        than the input start dates, then the code will throw some error messages.
        :return:
        """
        print("Running ", str(self.id()).split('.')[2])
        # initialize the parameters
        parm_dict = self._basic_dict()
        parm_dict["input_file"] = self.wind_data
        parm_dict["simulation_start_dt"] = datetime(year=2014, month=6, day=1, hour=1, minute=0, second=0)
        parm_dict["simulation_end_dt"] = datetime(year=2014, month=6, day=30, hour=0, minute=0, second=0)
        parm_dict["input_start_dt"] = datetime(year=2014, month=6, day=2, hour=0, minute=0, second=0)
        parm_dict["input_end_dt"] = datetime(year=2014, month=6, day=30, hour=0, minute=0, second=0)
        parm_list = list(parm_dict.values())
        # the function should get an error message
        with self.assertRaises(RuntimeError) as context:
            mapemain.main_func(*parm_list)
            self.assertTrue(isinstance(context, Iterable))
            self.assertTrue("Simulation must start after input start" in context)


if __name__ == "__main__":
    unittest.main()
