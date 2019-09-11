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
                    "show": True
                    }
        return basedict


    def test_for_single_date_ranges(self):
        """
        The user needs to set the input dates, otherwise the test will
        ends with errors
        :return:
        """
        print("Running ", str(self.id()).split('.')[2])
        parm_dict = self._basic_dict()
        parm_dict["input_file"] = self.wind_data
        parm_dict["simulated_timeseries"] = "actuals"
        parm_dict["base-process"] = "ARMA"
        parm_dict["simulation_start_dt"] = datetime(year=2014, month=6, day=1, hour=0, minute=0, second=0)
        parm_dict["simulation_end_dt"] = datetime(year=2014, month=6, day=30, hour=0, minute=0, second=0)
        parm_list = list(parm_dict.values())
        # the function should get an error message
        with self.assertRaises(TypeError) as context:
            mapemain.main_func(*parm_list)
            self.assertTrue(isinstance(context, Iterable))
            self.assertTrue("'<' not supported between instances of"
                            " 'datetime.datetime' and 'NoneType'" in context)


if __name__ == "__main__":
    unittest.main()
