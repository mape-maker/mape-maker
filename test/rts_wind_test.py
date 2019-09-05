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

class TestUM(unittest.TestCase):

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
                    "curvature": None,
                    "time_limit": 3600,
                    "curvature_target": None,
                    "mip_gap": 0.3,
                    "solver": "gurobi",
                    "latex_output": False,
                    "show": True
                    }
        return basedict

    @classmethod
    def setUpClass(self):
        # make a temp dir
        self.temp_dir = tempfile.mkdtemp()
        sys.path.insert(1, self.temp_dir)
        # change to the temp directory
        os.chdir(self.temp_dir)
        self.cwd = os.getcwd()
        print("temporary directory:", self.cwd)
        # path to the RTS wind data

        self.wind_data = file_path + dir_sep + "rts_gmlc" + \
                         dir_sep + "WIND_forecasts_actuals.csv"

    def test_commmand(self):
        """
        here is the command :
        python -m mape_maker "mape_maker/samples/WIND_forecasts_actuals.csv" -st "actuals" -n 5 -bp "ARMA" -o "wind_forecasts_actuals" -s 1234
        :return:
        """
        parm_dict = self._basic_dict()
        parm_dict["input_file"] = self.wind_data
        parm_dict["simulated_timeseries"] = "actuals"
        parm_dict["number_simulations"] = 5
        parm_dict["base-process"] = "ARMA"
        parm_dict["output_dir"] = "wind_forecasts_actuals"
        parm_list = list(parm_dict.values())
        mapemain.main_func(*parm_list)

if __name__ == "__main__":
    unittest.main()