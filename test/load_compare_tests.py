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
        # self.load_data = file_path + dir_sep + ".." + dir_sep + ".." + dir_sep + "mape_maker" + dir_sep + \
        #                  "samples" + dir_sep + "based_rts_gmlc" + dir_sep + "Load_rts_gmlc"+ dir_sep + \
        #                  "processed_file.csv"
        self.load_data = mape_maker_path + dir_sep + "samples" + \
                         dir_sep + "based_rts_gmlc" + dir_sep + "Load_rts_gmlc_based" \
                         + dir_sep + "processed_file.csv"

    def _base_dict(self):
        """
        initialize the parameters
        :return: basedict
        """
        basedict = {"input_file"            : "",
                    "target_mape"           : None,
                    "simulated_timeseries"  : "actuals",
                    "base-process"          : "",
                    "a"                     : None,
                    "output_dir"            : "result",
                    "number_simulations"    : 2,
                    "input_start_dt"        : None,
                    "input_end_dt"          : None,
                    "simulation_start_dt"   : None,
                    "simulation_end_dt"     : None,
                    "title"                 : "",
                    "seed"                  : 1234,
                    "load_pickle"           : False,
                    "curvature"             : False,
                    "time_limit"            : 1,
                    "curvature_target"      : None,
                    "mip_gap"               : None,
                    "solver"                : "gurobi",
                    "latex_output"          : False,
                    "show"                  : True,
                    "verbosity"             : 2,
                    "verbosity_output"      : None
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




    def get_the_first_and_last_num(self, output_dir_path):
        """
        this function will convert the output dir into dataframe
        and return the first number in the first col, and the last number in the last col.
        :param output_dir: the path to the output directory
               simulation_num: the number of simulation that the user set
        :return: the first and last number
        """
        csv_path = output_dir_path + dir_sep + "*.csv"
        output_file = glob.glob(csv_path)[0]
        df = pd.read_csv(output_file, index_col=0)

        # get the first and last simulation columns
        first_num = df.iloc[0, 0]
        last_num = df.iloc[len(df.index) - 1, len(df.columns) - 1]
        print("first number : ", first_num, "last number : ", last_num)
        return first_num, last_num


    @unittest.skipIf(skip_all_but_one,
                     "skipping compare output dirs with seed test")
    def test_compare_output_dirs_with_seed(self):
        """
        In this test, we are going to compare the first and the
        last number in the output files to see whether it gives
        the same results with the given seed.

        If the first number and the last number in the two files are same,
        then this test will pass.
        """
        print("Running ", str(self.id()).split('.')[2])
        # initialize the parameters
        parm_dict = self._base_dict()
        parm_dict["input_file"] = self.load_data
        parm_dict["output_dir"] = "first_testing_folder"
        parm_list = list(parm_dict.values())
        mapemain.main_func(*parm_list)
        output_dir_path1 = self.temp_dir + dir_sep + parm_dict["output_dir"]

        # get the first and last number
        f1, l1 = self.get_the_first_and_last_num(output_dir_path1)
        shutil.move(output_dir_path1, self.create_temp_dir())

        # run the test again to get the second output directory
        parm_dict["output_dir"] = "second_testing_folder"
        parm_list = list(parm_dict.values())
        mapemain.main_func(*parm_list)

        output_dir_path2 = self.temp_dir + dir_sep + parm_dict["output_dir"]
        # get the first and last number
        f2, l2 = self.get_the_first_and_last_num(output_dir_path2)
        shutil.move(output_dir_path2, self.create_temp_dir())

        # check the first and last numbers
        if f1 != f2 or l1 != l2:
            print("Error: If you set the seed, when you run the tests twice,"
                  " the numbers should be the same.")
            sys.exit(1)
        else:
            print("compare output dirs with seed test passed.")


    @unittest.skipIf(skip_all_but_one,
                     "skipping compare output dirs without seed test")
    def test_compare_output_dirs_without_seed(self):
        """
        In this test, we are going to compare the first and the
        last number in the output files to see whether it gives
        the same results without the given seed.

        If the first number and the last number in the two files are different,
        then this test will pass.
        """
        print("Running ", str(self.id()).split('.')[2])
        # initialize the parameters
        parm_dict = self._base_dict()
        parm_dict["input_file"] = self.load_data
        parm_dict["seed"] = None
        parm_dict["output_dir"] = "first_testing_folder"
        parm_list = list(parm_dict.values())
        mapemain.main_func(*parm_list)
        output_dir_path1 = self.temp_dir + dir_sep + parm_dict["output_dir"]

        # get the first and last number
        f1, l1 = self.get_the_first_and_last_num(output_dir_path1)
        shutil.move(output_dir_path1, self.create_temp_dir())

        # run the test again to get the second output directory
        parm_dict["output_dir"] = "second_testing_folder"
        parm_list = list(parm_dict.values())
        mapemain.main_func(*parm_list)

        output_dir_path2 = self.temp_dir + dir_sep + parm_dict["output_dir"]
        # get the first and last number
        f2, l2 = self.get_the_first_and_last_num(output_dir_path2)
        shutil.move(output_dir_path2, self.create_temp_dir())

        # check the first and last numbers
        if f1 == f2 and l1 == l2:
            print("Error: If you don't set the seed, when you run the tests twice,"
                  " the numbers should be different")
            sys.exit(1)
        else:
            print("compare output dirs without seed test passed.")


    @unittest.skipIf(skip_all_but_one,
                     "skipping input and simulation dates test")
    def test_input_and_simulation_dates(self):
        """
        python -m mape_maker "mape_maker/samples/based_rts_gmlc/Load_rts_gmlc_based/processed_file.csv" -st "forecasts" -n 3 -is "2020-5-1 1:0:0" -ie "2020-7-30 0:0:0" -sd "2020-4-22 0:0:0" -ed "2020-6-29 23:0:0" -s 1234

        This test is used to make sure if the simulation start date is earlier
        than the input start dates, then the code will throw some error messages.
        If MapeMaker raises an error, then this test will pass.
        """
        print("Running ", str(self.id()).split('.')[2])
        # initialize the parameters
        parm_dict = self._base_dict()
        parm_dict["input_file"] = self.load_data
        parm_dict["input_start_dt"] = datetime(year=2020, month=5, day=1, hour=1, minute=0, second=0)
        parm_dict["input_end_dt"] = datetime(year=2020, month=7, day=30, hour=0, minute=0, second=0)
        parm_dict["simulation_start_dt"] = datetime(year=2020, month=4, day=22, hour=0, minute=0, second=0)
        parm_dict["simulation_end_dt"] = datetime(year=2020, month=6, day=29, hour=23, minute=0, second=0)
        parm_list = list(parm_dict.values())
        with self.assertRaises(RuntimeError) as context:
            mapemain.main_func(*parm_list)
            self.assertTrue(isinstance(context, Iterable))
            self.assertTrue('Simulation must start after input start' in context)



if __name__ == "__main__":
    unittest.main()