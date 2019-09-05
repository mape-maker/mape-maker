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
        self.load_data = file_path + dir_sep + "rts_gmlc" + dir_sep + \
                         "Bus_220_Load_zone2_forecasts_actuals.csv"

    def test_Bus_220_load(self):
        print("Running ", str(self.id()).split('.')[2])
        # python -m mape_maker "test/rts_data/prescient_rts_gmlc/timeseries_data_files_noerror/Bus_220_Load_zone2_forecasts_actuals.csv" -st "actuals" -n 5 -bp "ARMA" -is "2020-1-10 0:0:0" -ie "2020-7-20 0:0:0" -sd "2020-6-1 0:0:0" -ed "2020-6-30 23:0:0" -o "Bus_220_load" -s 1234
        parm_dict                           = self._base_dict()
        parm_dict["input_file"]             = self.load_data
        parm_dict["simulated_timeseries"]   = "actuals"
        parm_dict["number_simulations"]     = 5
        parm_dict["base-process"]           = "ARMA"
        parm_dict["input_start_dt"]         = datetime(year=2020, month=1, day=10, hour=0, minute=0, second=0)
        parm_dict["input_end_dt"]           = datetime(year=2020, month=7, day=20, hour=0, minute=0, second=0)
        parm_dict["simulation_start_dt"]    = datetime(year=2020, month=6, day=1, hour=0, minute=0, second=0)
        parm_dict["simulation_end_dt"]      = datetime(year=2020, month=6, day=30, hour=23, minute=0, second=0)
        parm_dict["output_dir"]             = "Bus_220_load"
        parm_dict["full_dataset"]           = True
        parm_list = list(parm_dict.values())
        # run the test
        mapemain.main_func(*parm_list)

if __name__ == "__main__":
    unittest.main()
