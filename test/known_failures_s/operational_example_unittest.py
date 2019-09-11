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
import mape_maker
from mape_maker import __main__ as mapemain
dir_sep = "/"
p = str(mape_maker.__path__)
l = p.find("'")
r = p.find("'", l+1)
mape_maker_path = p[l+1:r]
file_path = mape_maker_path + dir_sep + "samples"

class TestUM(unittest.TestCase):


    def _base_dict(self):
        basedict = {"input_file"            : "",
                    "target_mape"           : None,
                    "simulated_timeseries"  : "",
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
                    "curvature"             : None,
                    "time_limit"            : 1,
                    "curvature_target"      : None,
                    "mip"                   : None,
                    "solver"                : None,
                    "full_dataset"          : True,
                    "latex_output"          : False,
                    "show"                  : False
                    }

        return basedict

    @classmethod
    def setUpClass(self):
        # make a temp dir; to print temp_dir path use print(self.temp_dir)
        self.temp_dir = tempfile.mkdtemp()
        sys.path.insert(1, self.temp_dir)
        # change to the temp directory
        os.chdir(self.temp_dir)
        self.cwd = os.getcwd()
        print("the output dir will be saved to:", self.cwd)
        # path to Bus_220_Load_zone2
        self.load_rts_data = file_path + dir_sep + "rts_gmlc" + dir_sep + \
                         "load_operations_example.csv"
        self.wind_rts_data = file_path + dir_sep + "rts_gmlc" + dir_sep + \
                         "wind_operations_example.csv"

    def create_temp_dir(self):
        """
        create a sub temporary directory inside the main temporary directory
        to save the output file
        :return: sub_directory
        """
        sub_directory = tempfile.mkdtemp(dir=self.temp_dir)
        print("sub temporary directory:", sub_directory)
        return sub_directory




    def test_load_operations_example(self):
        print("Running ", str(self.id()).split('.')[2])
        # python -m mape_maker "mape_maker/samples/rts_gmlc/load_operations_example.csv" -st "actuals" -n 5 -bp "ARMA" -is "2020-1-1 01:00:00" -ie "2020-12-29 23:00:00" -sd "2020-12-30 00:00:00" -ed "2020-12-31 23:00:00" -o "load_operations_example" -s 1234
        parm_dict                           = self._base_dict()
        parm_dict["input_file"]             = self.load_rts_data
        parm_dict["simulated_timeseries"]   = "actuals"
        parm_dict["number_simulations"]     = 5
        parm_dict["base-process"]           = "ARMA"
        parm_dict["input_start_dt"]         = datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0)
        parm_dict["input_end_dt"]           = datetime(year=2020, month=12, day=29, hour=23, minute=0, second=0)
        parm_dict["simulation_start_dt"]    = datetime(year=2020, month=12, day=30, hour=0, minute=0, second=0)
        parm_dict["simulation_end_dt"]      = datetime(year=2020, month=12, day=31, hour=23, minute=0, second=0)
        parm_dict["output_dir"]             = "load_operations_example"
        parm_list = list(parm_dict.values())
        # run the test
        mapemain.main_func(*parm_list)

        # save the output dir to the sub temporary directory
        output_dir_path = self.temp_dir + dir_sep + parm_dict["output_dir"]
        print("output_dir_path = ", output_dir_path)
        print("parm_dict[output_dir]", parm_dict["output_dir"])
        temp_sub_dir = self.create_temp_dir()
        print("Created temp_sub_dir = ", temp_sub_dir)
        shutil.move(output_dir_path, temp_sub_dir)

    def test_wind_operations_example(self):
        print("Running ", str(self.id()).split('.')[2])
        # python -m mape_maker "mape_maker/samples/rts_gmlc/wind_operations_example.csv" -st "actuals" -n 5 -bp "ARMA" -is "2020-1-1 01:00:00" -ie "2020-12-29 23:00:00" -sd "2020-12-30 00:00:00" -ed "2020-12-31 23:00:00" -o "wind_operations_example" -s 1234
        parm_dict                           = self._base_dict()
        parm_dict["input_file"]             = self.wind_rts_data
        parm_dict["simulated_timeseries"]   = "actuals"
        parm_dict["number_simulations"]     = 5
        parm_dict["base-process"]           = "ARMA"
        parm_dict["input_start_dt"]         = datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0)
        parm_dict["input_end_dt"]           = datetime(year=2020, month=12, day=29, hour=23, minute=0, second=0)
        parm_dict["simulation_start_dt"]    = datetime(year=2020, month=12, day=30, hour=0, minute=0, second=0)
        parm_dict["simulation_end_dt"]      = datetime(year=2020, month=12, day=31, hour=23, minute=0, second=0)
        parm_dict["output_dir"]             = "wind_operations_example"
        parm_list = list(parm_dict.values())
        # run the test
        mapemain.main_func(*parm_list)

        # save the output dir to the sub temporary directory
        output_dir_path = self.temp_dir + dir_sep + parm_dict["output_dir"]
        print("output_dir_path = ", output_dir_path)
        print("parm_dict[output_dir]", parm_dict["output_dir"])
        temp_sub_dir = self.create_temp_dir()
        print("Created temp_sub_dir = ", temp_sub_dir)
        shutil.move(output_dir_path, temp_sub_dir)

if __name__ == "__main__":
    unittest.main()
