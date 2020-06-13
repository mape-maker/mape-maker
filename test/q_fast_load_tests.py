import tempfile
import pyutilib.th as unittest
import sys
import os.path
import os
import datetime
from datetime import datetime
import shutil
import mape_maker
from mape_maker import __main__ as mapemain

dir_sep = "/"
p = str(mape_maker.__path__)
l = p.find("'")
r = p.find("'", l + 1)
mape_maker_path = p[l + 1:r]
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
        # path to the RTS Load data
        # self.load_data = file_path + dir_sep + "based_rts_gmlc" + dir_sep + "Load_rts_gmlc_based" +\
        #                  dir_sep + "procssed_file.csv"
        self.load_data = mape_maker_path + dir_sep + "samples" + \
                         dir_sep + "based_rts_gmlc" + dir_sep + "Load_rts_gmlc_based" \
                         + dir_sep + "processed_file.csv"

    def _base_dict(self):
        """
        initialize the parameters
        :return: basedict
        """
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

    def test_one(self):
        print("Running ", str(self.id()).split('.')[2])
        # python -m mape_maker "mape_maker/samples/based_rts_gmlc/Load_rts_gmlc_based/processed_file.csv" -st "actuals" -n 1 -bp "ARMA" -is "2020-1-1 1:0:0" -ie "2020-3-30 0:0:0" -sd "2020-2-1 0:0:0" -ed "2020-2-30 23:0:0" -s 1234
        parm_dict = self._base_dict()
        parm_dict["input_file"] = self.load_data
        parm_dict["simulated_timeseries"] = "actuals"
        parm_dict["number_simulations"] = 1
        parm_dict["base-process"] = "ARMA"
        parm_dict["input_start_dt"] = datetime(year=2020, month=1, day=1, hour=1, minute=0, second=0)
        parm_dict["input_end_dt"] = datetime(year=2020, month=3, day=30, hour=0, minute=0, second=0)
        parm_dict["simulation_start_dt"] = datetime(year=2020, month=2, day=10, hour=0, minute=0, second=0)
        parm_dict["simulation_end_dt"] = datetime(year=2020, month=2, day=28, hour=23, minute=0, second=0)
        parm_list = list(parm_dict.values())
        mapemain.main_func(*parm_list)

    def test_two(self):
        print("Running ", str(self.id()).split('.')[2])
        # python -m mape_maker "mape_maker/samples/rbased_rts_gmlc/Load_rts_gmlc_based/processed_file.csv" -st "forecasts" -n 1 -bp "ARMA" -s 1234
        parm_dict = self._base_dict()
        parm_dict["input_file"] = self.load_data
        parm_dict["simulated_timeseries"] = "forecasts"
        parm_dict["number_simulations"] = 1
        parm_dict["base-process"] = "ARMA"
        parm_list = list(parm_dict.values())
        mapemain.main_func(*parm_list)

    def test_three(self):
        print("Running ", str(self.id()).split('.')[2])
        # python -m mape_maker "mape_maker/samples/based_rts_gmlc/Load_rts_gmlc_based/processed_file.csv" -st "forecasts" -n 1 -bp "iid" -is "2020-1-1 1:0:0" -ie "2020-3-30 0:0:0" -sd "2020-2-1 0:0:0" -ed "2020-2-30 23:0:0" -s 1234
        parm_dict = self._base_dict()
        parm_dict["input_file"] = self.load_data
        parm_dict["simulated_timeseries"] = "forecasts"
        parm_dict["number_simulations"] = 1
        parm_dict["base-process"] = "iid"
        parm_dict["input_start_dt"] = datetime(year=2020, month=1, day=1, hour=1, minute=0, second=0)
        parm_dict["input_end_dt"] = datetime(year=2020, month=3, day=30, hour=0, minute=0, second=0)
        parm_dict["simulation_start_dt"] = datetime(year=2020, month=2, day=10, hour=0, minute=0, second=0)
        parm_dict["simulation_end_dt"] = datetime(year=2020, month=2, day=28, hour=23, minute=0, second=0)
        parm_list = list(parm_dict.values())
        mapemain.main_func(*parm_list)

    def test_four(self):
        print("Running ", str(self.id()).split('.')[2])
        # python -m mape_maker "mape_maker/samples/rbased_rts_gmlc/Load_rts_gmlc_based/processed_file.csv" -st "actuals" -n 1 -bp "iid" -s 1234
        parm_dict = self._base_dict()
        parm_dict["input_file"] = self.load_data
        parm_dict["simulated_timeseries"] = "actuals"
        parm_dict["number_simulations"] = 1
        parm_dict["base-process"] = "iid"
        parm_list = list(parm_dict.values())
        mapemain.main_func(*parm_list)

if __name__ == "__main__":
    unittest.main()
