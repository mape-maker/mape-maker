import pyutilib.th as unittest
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
test_with_error = True
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

    def test_first(self):
        """
        here is the command : python -m mape_maker "mape_maker/samples/CAISO_wind_operational_data.csv" -s 1234 -n 1
        -bp "ARMA" -is "2013-7-1 00:00:00" -ie "2013-12-30 23:00:00" -sd "2015-6-29 23:00:00" -ed
        "2015-6-30 23:00:00" :return:
        """
        print("Running ", str(self.id()).split('.')[2])
        parm_dict = self._basic_dict()
        parm_dict["input_file"] = file_path + dir_sep + "CAISO_wind_operational_data.csv"
        parm_dict["simulated_timeseries"] = "actuals"
        parm_dict["number_simulations"] = 1
        parm_dict["seed"] = 1234
        parm_dict["input_start_dt"] = datetime(year=2013, month=7, day=1, hour=0, minute=0, second=0)
        parm_dict["input_end_dt"] = datetime(year=2013, month=12, day=30, hour=23, minute=0, second=0)
        parm_dict["simulation_start_dt"] = datetime(year=2015, month=6, day=29, hour=23, minute=0, second=0)
        parm_dict["simulation_end_dt"] = datetime(year=2015, month=6, day=30, hour=23, minute=0, second=0)
        parm_list = list(parm_dict.values())
        mapemain.main_func(*parm_list)

    def test_second(self):
        """
        here is the command : python -m mape_maker "mape_maker/samples/CAISO_wind_operational_data.csv" -s 1234 -n 1
        -bp "iid" -is "2013-7-1 00:00:00" -ie "2013-12-30 23:00:00" -sd "2015-6-29 23:00:00" -ed
        "2015-6-30 23:00:00" :return:
        """
        print("Running ", str(self.id()).split('.')[2])
        parm_dict = self._basic_dict()
        parm_dict["input_file"] = file_path + dir_sep + "CAISO_wind_operational_data.csv"
        parm_dict["simulated_timeseries"] = "actuals"
        parm_dict["base-process"] = "iid"
        parm_dict["number_simulations"] = 1
        parm_dict["seed"] = 1234
        parm_dict["input_start_dt"] = datetime(year=2013, month=7, day=1, hour=0, minute=0, second=0)
        parm_dict["input_end_dt"] = datetime(year=2013, month=12, day=30, hour=23, minute=0, second=0)
        parm_dict["simulation_start_dt"] = datetime(year=2015, month=6, day=29, hour=23, minute=0, second=0)
        parm_dict["simulation_end_dt"] = datetime(year=2015, month=6, day=30, hour=23, minute=0, second=0)
        parm_list = list(parm_dict.values())
        mapemain.main_func(*parm_list)

    def test_third(self):
        """
        here is the command : python -m mape_maker "mape_maker/samples/rts_gmlc/WIND_forecasts_actuals.csv" -s 1234
        -n 1 -bp "ARMA" -is "2020-2-1 00:00:00" -ie "2020-10-31 23:00:00" -sd "2020-11-1 0:00:00"
        -ed "2020-11-7 00:00:00" :return:
        """
        print("Running ", str(self.id()).split('.')[2])
        parm_dict = self._basic_dict()
        parm_dict["input_file"] = file_path + dir_sep + "rts_gmlc" + dir_sep + "WIND_forecasts_actuals.csv"
        parm_dict["simulated_timeseries"] = "actuals"
        parm_dict["number_simulations"] = 1
        parm_dict["seed"] = 1234
        parm_dict["input_start_dt"] = datetime(year=2020, month=2, day=1, hour=0, minute=0, second=0)
        parm_dict["input_end_dt"] = datetime(year=2020, month=10, day=31, hour=23, minute=0, second=0)
        parm_dict["simulation_start_dt"] = datetime(year=2020, month=11, day=1, hour=0, minute=0, second=0)
        parm_dict["simulation_end_dt"] = datetime(year=2020, month=11, day=7, hour=0, minute=0, second=0)
        parm_list = list(parm_dict.values())
        with self.assertRaises(RuntimeError) as context:
            mapemain.main_func(*parm_list)
        self.assertTrue('< 1, there is a prevalence of high power input in the SID' in str(context.exception))

    def test_fourth(self):
        """
        here is the command : python -m mape_maker "mape_maker/samples/rts_gmlc/WIND_forecasts_actuals.csv" -s 1234
        -n 1 -bp "ARMA" -st "forecasts" -is "2020-2-1 00:00:00" -ie "2020-8-31 23:00:00" -sd "2020-11-1 0:00:00"
        -ed "2020-11-7 00:00:00" :return:
        """
        print("Running ", str(self.id()).split('.')[2])
        parm_dict = self._basic_dict()
        parm_dict["input_file"] = file_path + dir_sep + "rts_gmlc" + dir_sep + "WIND_forecasts_actuals.csv"
        parm_dict["simulated_timeseries"] = "forecasts"
        parm_dict["number_simulations"] = 1
        parm_dict["seed"] = 1234
        parm_dict["input_start_dt"] = datetime(year=2020, month=2, day=1, hour=0, minute=0, second=0)
        parm_dict["input_end_dt"] = datetime(year=2020, month=8, day=31, hour=23, minute=0, second=0)
        parm_dict["simulation_start_dt"] = datetime(year=2020, month=11, day=1, hour=0, minute=0, second=0)
        parm_dict["simulation_end_dt"] = datetime(year=2020, month=11, day=7, hour=0, minute=0, second=0)
        parm_list = list(parm_dict.values())
        with self.assertRaises(RuntimeError) as context:
            mapemain.main_func(*parm_list)
        self.assertTrue('< 1, there is a prevalence of high power input in the SID' in str(context.exception))

if __name__ == "__main__":
    unittest.main()