import tempfile
import pyutilib.th as unittest
import sys
import os.path
import os
import datetime
from datetime import datetime
import mape_maker
from mape_maker import __main__ as mapemain

dir_sep = "/"
p = str(mape_maker.__path__)
l = p.find("'")
r = p.find("'", l + 1)
mape_maker_path = p[l + 1:r]
file_path = mape_maker_path + dir_sep + "samples"


class TestUM(unittest.TestCase):

    def _base_dict(self):
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
        # path to Bus_220_Load_zone2
        self.load_data = file_path + dir_sep + "rts_gmlc" + dir_sep + \
                         "Bus_220_Load_zone2_forecasts_actuals.csv"

    def test_one(self):
        print("Running ", str(self.id()).split('.')[2])
        parm_dict = self._base_dict()
        parm_dict["input_file"] = self.load_data
        parm_dict["second_file"] = self.load_data
        parm_dict["simulated_timeseries"] = "actuals"
        parm_dict["number_simulations"] = 1
        parm_dict["base-process"] = "ARMA"
        parm_dict["input_start_dt"] = datetime(year=2020, month=1, day=10, hour=0, minute=0, second=0)
        parm_dict["input_end_dt"] = datetime(year=2020, month=5, day=20, hour=0, minute=0, second=0)
        parm_dict["simulation_start_dt"] = datetime(year=2020, month=6, day=1, hour=0, minute=0, second=0)
        parm_dict["simulation_end_dt"] = datetime(year=2020, month=6, day=30, hour=23, minute=0, second=0)
        parm_list = list(parm_dict.values())
        # run the test
        mapemain.main_func(*parm_list)

    def test_two(self):
        print("Running ", str(self.id()).split('.')[2])
        parm_dict = self._base_dict()
        parm_dict["input_file"] = self.load_data
        parm_dict["simulated_timeseries"] = "forecasts"
        parm_dict["number_simulations"] = 1
        parm_dict["base-process"] = "ARMA"
        parm_dict["input_start_dt"] = datetime(year=2020, month=1, day=10, hour=0, minute=0, second=0)
        parm_dict["input_end_dt"] = datetime(year=2020, month=5, day=20, hour=0, minute=0, second=0)
        parm_dict["simulation_start_dt"] = datetime(year=2020, month=1, day=11, hour=0, minute=0, second=0)
        parm_dict["simulation_end_dt"] = datetime(year=2020, month=4, day=20, hour=23, minute=0, second=0)
        parm_list = list(parm_dict.values())
        # run the test
        mapemain.main_func(*parm_list)

    def test_three(self):
        print("Running ", str(self.id()).split('.')[2])
        parm_dict = self._base_dict()
        parm_dict["input_file"] = self.load_data
        parm_dict["simulated_timeseries"] = "actuals"
        parm_dict["number_simulations"] = 1
        parm_dict["base-process"] = "iid"
        parm_dict["input_start_dt"] = datetime(year=2020, month=3, day=20, hour=0, minute=0, second=0)
        parm_dict["input_end_dt"] = datetime(year=2020, month=7, day=20, hour=0, minute=0, second=0)
        parm_dict["simulation_start_dt"] = datetime(year=2020, month=6, day=1, hour=0, minute=0, second=0)
        parm_dict["simulation_end_dt"] = datetime(year=2020, month=6, day=30, hour=23, minute=0, second=0)
        parm_list = list(parm_dict.values())
        # run the test
        mapemain.main_func(*parm_list)


if __name__ == "__main__":
    unittest.main()
