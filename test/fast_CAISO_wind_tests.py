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

    def test_wind_actuals_ARMA_with_dates(self):
        # here is the command :
        # python -m mape_maker "mape_maker/samples/wind_total_forecast_actual_070113_063015.csv" -st "actuals" -n 1 -bp "iid" -o "wind_actuals_iid" -is "2014-7-1 00:00:00" -ie "2014-8-1 00:00:00" -sd "2014-7-2 00:00:00" -ed "2014-7-31 00:00:00" -s 1234
        parm_dict = self._basic_dict()
        parm_dict["input_file"] = self.wind_data
        parm_dict["simulated_timeseries"] = "actuals"
        parm_dict["base-process"] = "ARMA"
        parm_dict["input_start_dt"] = datetime(year=2014, month=7, day=1, hour=0, minute=0, second=0)
        parm_dict["input_end_dt"] = datetime(year=2014, month=8, day=1, hour=0, minute=0, second=0)
        parm_dict["simulation_start_dt"] = datetime(year=2014, month=7, day=2, hour=0, minute=0, second=0)
        parm_dict["simulation_end_dt"] = datetime(year=2014, month=7, day=31, hour=0, minute=0, second=0)
        parm_dict["seed"] = 1134
        parm_list = list(parm_dict.values())
        mapemain.main_func(*parm_list)

if __name__ == "__main__":
    unittest.main()