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
from mape_maker import __main__ as mapemain
from collections.abc import Iterable
dir_sep = "/"
p = str(mape_maker.__path__)
l = p.find("'")
r = p.find("'", l+1)
mape_maker_path = p[l+1:r]
file_path = mape_maker_path + dir_sep + "samples"

# whether to skip the last two tests
quick_test = False
# whether to run only one example
skip_all_but_one = False
# whether to skip the test which always fails
test_known_failure = False


class TestUM(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # make a temp dir
        self.temp_dir = tempfile.mkdtemp()
        sys.path.insert(1, self.temp_dir)
        # change to the temp directory
        os.chdir(self.temp_dir)
        self.cwd = os.getcwd()
        print("temporary directory:", self.cwd)
        # path to the RTS Load data
        self.load_data = file_path + dir_sep + ".." + dir_sep + ".." + dir_sep + "mape_maker" + dir_sep + \
                         "samples" + dir_sep + "rts_gmlc" + dir_sep + "Load_forecasts_actuals.csv"

    def _base_dict(self):
        """
        initialize the parameters
        :return: basedict
        """
        basedict = {"input_file"            : "",
                    "target_mape"           : None,
                    "simulated_timeseries"  : "",
                    "base-process"          : "",
                    "a"                     : None,
                    "output_dir"            : "result",
                    "number_simulations"    : 3,
                    "input_start_dt"        : None,
                    "input_end_dt"          : None,
                    "simulation_start_dt"   : None,
                    "simulation_end_dt"     : None,
                    "title"                 : "",
                    "seed"                  : 1234,
                    "load_pickle"           : False,
                    "curvature"             : None,
                    "time_limit"            : 1,
                    "curvature_target"      : None,
                    "mip_gap"               : None,
                    "solver"                : "gurobi",
                    "latex_output"          : False,
                    "show"                  : True
                    }

        return basedict

    def create_temp_dir(self):
        """
        create a sub temporary directory inside the main temporary directory
        to save the output file
        """
        sub_directory = tempfile.mkdtemp(dir=self.temp_dir)
        print("sub temporary directory:", sub_directory)
        return sub_directory

    def test_load_first_command(self):
        print("Running ", str(self.id()).split('.')[2])
        # python -m mape_maker "mape_maker/samples/rts_gmlc/Load_forecasts_actuals.csv" -st "actuals" -n 3 -bp "ARMA" -o "load_actuals_iid" -s 1234
        parm_dict                           = self._base_dict()
        parm_dict["input_file"]             = self.load_data
        parm_dict["simulated_timeseries"]   = "actuals"
        parm_dict["number_simulations"]     = 1
        parm_dict["base-process"]           = "ARMA"
        parm_dict["output_dir"]             = "load_actuals_iid"
        parm_list                           = list(parm_dict.values())
        # run the test
        mapemain.main_func(*parm_list)
        # save the output dir to the sub temporary directory
        output_dir_path = self.temp_dir + dir_sep + parm_dict["output_dir"]
        print("output_dir_path = ", output_dir_path)
        print("parm_dict[output_dir]", parm_dict["output_dir"])
        temp_sub_dir = self.create_temp_dir()
        print("Created temp_sub_dir = ", temp_sub_dir)
        shutil.move(output_dir_path, temp_sub_dir)
        output_file_path = temp_sub_dir + dir_sep + output_dir_path
        print("output_file_path = ", output_file_path)
        #output_file_path = pd.read_csv(file_path1[0], index_col=0)
        print("read output file path")
        #print(output_file_path)

    @unittest.skipIf(skip_all_but_one,
                     "skipping the second test")
    def test_load_second_command(self):
        print("Running ", str(self.id()).split('.')[2])
        # python -m mape_maker "mape_maker/samples/rts_gmlc/Load_forecasts_actuals.csv" -st "actuals" -n 3 -bp "ARMA" -is "2020-5-1 1:0:0" -ie "2020-7-30 0:0:0" -sd "2020-6-1 0:0:0" -ed "2020-6-30 23:0:0" -o "load_actuals_ARMA" -s 1234
        parm_dict                           = self._base_dict()
        parm_dict["input_file"]             = self.load_data
        parm_dict["simulated_timeseries"]   = "actuals"
        parm_dict["number_simulations"]     = 3
        parm_dict["base-process"]           = "iid"
        parm_dict["input_start_dt"]         = datetime(year=2020, month=5, day=1,   hour=1,   minute=0, second=0)
        parm_dict["input_end_dt"]           = datetime(year=2020, month=7, day=30,  hour=0,   minute=0, second=0)
        parm_dict["simulation_start_dt"]    = datetime(year=2020, month=6, day=10,   hour=0,   minute=0, second=0)
        parm_dict["simulation_end_dt"]      = datetime(year=2020, month=6, day=30,  hour=23,  minute=0, second=0)
        parm_dict["output_dir"]             = "load_actuals_ARMA"
        parm_list                           = list(parm_dict.values())
        # run the test
        mapemain.main_func(*parm_list)
        # save the output dir to the sub temporary directory
        output_dir_path = self.temp_dir + dir_sep + parm_dict["output_dir"]
        shutil.move(output_dir_path, self.create_temp_dir())

    @unittest.skipIf(skip_all_but_one or test_known_failure or quick_test,
                     "skipping the third test")
    def test_load_third_command(self):
        print("Running ", str(self.id()).split('.')[2])
        # python -m mape_maker "mape_maker/samples/rts_gmlc/Load_forecasts_actuals.csv" -st "forecasts" -n 3 -bp "ARMA" -o "load_actuals_ARMA" -s 1234
        parm_dict                           = self._base_dict()
        parm_dict["input_file"]             = self.load_data
        parm_dict["simulated_timeseries"]   = "forecasts"
        parm_dict["number_simulations"]     = 3
        parm_dict["base-process"]           = "ARMA"
        parm_dict["output_dir"]             = "load_actuals_ARMA"
        parm_list                           = list(parm_dict.values())

        # run the test
        mapemain.main_func(*parm_list)
        # save the output dir to the sub temporary directory

        output_dir_path = self.temp_dir + dir_sep + parm_dict["output_dir"]
        shutil.move(output_dir_path, self.create_temp_dir())

    @unittest.skipIf(skip_all_but_one or test_known_failure or quick_test,
                     "skipping the fourth test")
    def test_load_fourth_command(self):
        print("Running ", str(self.id()).split('.')[2])
        # python -m mape_maker "mape_maker/samples/rts_gmlc/Load_forecasts_actuals.csv" -st "forecasts" -n 3 -bp "iid" -is "2020-5-1 1:0:0" -ie "2020-7-30 0:0:0" -sd "2020-6-1 0:0:0" -ed "2020-6-30 23:0:0" -o "load_forecasts_iid" -s 1234
        parm_dict                           = self._base_dict()
        parm_dict["input_file"]             = self.load_data
        parm_dict["simulated_timeseries"]   = "forecasts"
        parm_dict["number_simulations"]     = 3
        parm_dict["base-process"]           = "iid"
        parm_dict["input_start_dt"]         = datetime(year=2020, month=5, day=1,   hour=1,   minute=0, second=0)
        parm_dict["input_end_dt"]           = datetime(year=2020, month=7, day=30,  hour=0,   minute=0, second=0)
        parm_dict["simulation_start_dt"]    = datetime(year=2020, month=6, day=1,   hour=0,   minute=0, second=0)
        parm_dict["simulation_end_dt"]      = datetime(year=2020, month=6, day=30,  hour=23,  minute=0, second=0)
        parm_dict["output_dir"]             = "load_forecasts_iid"
        parm_list                           = list(parm_dict.values())

        # run the test
        mapemain.main_func(*parm_list)

        # save the output dir to the sub temporary directory
        output_dir_path = self.temp_dir + dir_sep + parm_dict["output_dir"]
        shutil.move(output_dir_path, self.create_temp_dir())

    def get_the_first_and_last_num(self, output_dir_path):
        """
        this function will convert the output dir into dataframe
        and return the first and last numbers
        :param output_dir: the path to the output directory
               simulation_num: the number of simulation that the user set
        :return: the first and last number
        """
        csv_path        = output_dir_path + dir_sep + "*.csv"
        output_file     = glob.glob(csv_path)[0]
        df              = pd.read_csv(output_file, index_col=0)

        # get the first and last simulation columns
        first_num       = df.iloc[0, 0]
        last_num        = df.iloc[len(df.index) - 1, len(df.columns) - 1]
        print("first number : ", first_num, "last number : ", last_num)
        return first_num, last_num

    @unittest.skipIf(skip_all_but_one,
                     "skipping compare output dir with seed test")
    def compare_output_dirs_with_seed(self):
        """
        In this test, we are going to compare the first and the
        last number in the output files to see whether it gives
        the same results with the given seed.
        :return: boolean
        """
        print("Running ", str(self.id()).split('.')[2])
        # initialize the parameters
        parm_dict                   = self._base_dict()
        parm_dict["input_file"]     = self.load_data
        parm_dict["output_dir"]     = "first_testing_folder"
        parm_list                   = list(parm_dict.values())
        mapemain.main_func(*parm_list)
        output_dir_path1            = self.temp_dir + dir_sep + parm_dict["output_dir"]

        # get the first and last number
        f1, l1                      = self.get_the_first_and_last_num(output_dir_path1)
        shutil.move(output_dir_path1, self.create_temp_dir())

        # run the test again to get the second output directory
        parm_dict["output_dir"]     = "second_testing_folder"
        parm_list                   = list(parm_dict.values())
        mapemain.main_func(*parm_list)

        output_dir_path2            = self.temp_dir + dir_sep + parm_dict["output_dir"]
        # get the first and last number
        f2, l2  = self.get_the_first_and_last_num(output_dir_path2)
        shutil.move(output_dir_path2, self.create_temp_dir())

        # check the first and last numbers
        if f1 != f2 or l1 != l2:
            print("Error: If you set the seed, when you run the tests twice,"
                  " the numbers should be the same.")
            sys.exit(1)

    @unittest.skipIf(skip_all_but_one,
                     "skipping compare output dir without seed test")
    def compare_output_dirs_without_seed(self):
        """
        In this test, we are going to compare the first and the
        last number in the output files to see whether it gives
        the same results without the given seed.
        :return: boolean
        """
        print("Running ", str(self.id()).split('.')[2])
        # initialize the parameters
        parm_dict                   = self._base_dict()
        parm_dict["input_file"]     = self.load_data
        parm_dict["seed"]           = None
        parm_dict["output_dir"]     = "first_testing_folder"
        parm_list                   = list(parm_dict.values())
        mapemain.main_func(*parm_list)
        output_dir_path1            = self.temp_dir + dir_sep + parm_dict["output_dir"]

        # get the first and last number
        f1, l1                      = self.get_the_first_and_last_num(output_dir_path1)
        shutil.move(output_dir_path1, self.create_temp_dir())

        # run the test again to get the second output directory
        parm_dict["output_dir"]     = "second_testing_folder"
        parm_list                   = list(parm_dict.values())
        mapemain.main_func(*parm_list)

        output_dir_path2            = self.temp_dir + dir_sep + parm_dict["output_dir"]
        # get the first and last number
        f2, l2                      = self.get_the_first_and_last_num(output_dir_path2)
        shutil.move(output_dir_path2, self.create_temp_dir())

        # check the first and last numbers
        if f1 == f2 and l1 == l2:
            print("Error: If you don't set the seed, when you run the tests twice,"
                  " the numbers should be different")
            sys.exit(1)

    @unittest.skipIf(skip_all_but_one,
                     "skipping check input and simulation dates test")
    def test_simulation_and_input_dates(self):
        """
        python -m mape_maker "mape_maker/samples/rts_gmlc/Load_forecasts_actuals.csv" -st "forecasts" -n 3 -bp "iid" -is "2020-5-1 1:0:0" -ie "2020-7-30 0:0:0" -sd "2020-4-22 0:0:0" -ed "2020-6-29 23:0:0" -s 1234
        This test is used to make sure if the simulation start date is earlier
        than the input start dates, then the code will throw some error messages.
        :return:
        """
        print("Running ", str(self.id()).split('.')[2])
        # initialize the parameters
        parm_dict                           = self._base_dict()
        parm_dict["input_file"]             = self.load_data
        parm_dict["input_start_dt"]         = datetime(year=2020, month=5, day=1,   hour=1,   minute=0, second=0)
        parm_dict["input_end_dt"]           = datetime(year=2020, month=7, day=30,  hour=0,   minute=0, second=0)
        parm_dict["simulation_start_dt"]    = datetime(year=2020, month=4, day=22,   hour=0,   minute=0, second=0)
        parm_dict["simulation_end_dt"]      = datetime(year=2020, month=6, day=29,  hour=23,  minute=0, second=0)
        parm_list                           = list(parm_dict.values())
        with self.assertRaises(RuntimeError) as context:
            mapemain.main_func(*parm_list)
            self.assertTrue(isinstance(context, Iterable))
            self.assertTrue('Simulation must start after input start' in context)

if __name__ == "__main__":
    unittest.main()
