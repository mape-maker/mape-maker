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

        self.wind_data = file_path + dir_sep + "based_rts_gmlc" + \
                         dir_sep + "Wind_rts_gmlc_based" + dir_sep + \
                         "processed_file.csv"

    def test_commmand(self):
        """
        here is the command :
        python -m mape_maker "mape_maker/samples/based_rts_gmlc/Wind_rts_gmlc_based/processed_file.csv" -st "actuals" -s 1234 -n 5 -bp "ARMA" -o "wind_forecasts_actuals" -is "2020-2-1 00:00:00" -ie "2020-5-1 00:00:00" -sd "2020-2-2 00:00:00" -ed "2020-3-2 00:00:00"
        :return:
        """
        print("Running ", str(self.id()).split('.')[2])
        parm_dict = self._basic_dict()
        parm_dict["input_file"] = self.wind_data
        parm_dict["simulated_timeseries"] = "actuals"
        parm_dict["number_simulations"] = 5
        parm_dict["base-process"] = "ARMA"
        parm_dict["output_dir"] = "wind_forecasts_actuals"
        parm_dict["seed"] = 1234
        parm_dict["simulation_start_dt"] = datetime(year=2020, month=2, day=2, hour=0, minute=0, second=0)
        parm_dict["simulation_end_dt"] = datetime(year=2020, month=3, day=2, hour=0, minute=0, second=0)
        parm_dict["input_start_dt"] = datetime(year=2020, month=2, day=1, hour=0, minute=0, second=0)
        parm_dict["input_end_dt"] = datetime(year=2020, month=5, day=1, hour=0, minute=0, second=0)
        parm_list = list(parm_dict.values())
        mapemain.main_func(*parm_list)

if __name__ == "__main__":
    unittest.main()