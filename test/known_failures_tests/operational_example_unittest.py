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
                    "load_pickle"           : False,
                    "curvature"             : False,
                    "time_limit"            : 1,
                    "curvature_target"      : None,
                    "mip_gap"               : None,
                    "solver"                : "gurobi",
                    "latex_output"          : False,
                    "show"                  : True
                    }

        return basedict

    @classmethod
    def setUpClass(self):
        self.cwd = os.getcwd()
        # path to Bus_220_Load_zone2
        self.load_rts_data = file_path + dir_sep + "rts_gmlc" + dir_sep + \
                         "load_operations_example.csv"
        self.wind_rts_data = file_path + dir_sep + "rts_gmlc" + dir_sep + \
                         "wind_operations_example.csv"

    '''
    basic command line run for load_ops and wind_ops
    '''

    def test_load_operations_example(self):
        print("Running ", str(self.id()).split('.')[2])
        # python -m mape_maker "mape_maker/samples/rts_gmlc/load_operations_example.csv" -st "actuals" -n 2 -bp "ARMA" -is "2020-1-1 01:00:00" -ie "2020-12-29 23:00:00" -sd "2020-12-30 00:00:00" -ed "2020-12-31 23:00:00" -o "load_operations_example" -s 1234
        parm_dict                           = self._base_dict()
        parm_dict["input_file"]             = self.load_rts_data
        parm_dict["simulated_timeseries"]   = "actuals"
        parm_dict["number_simulations"]     = 2
        parm_dict["base-process"]           = "ARMA"
        parm_dict["input_start_dt"]         = datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0)
        parm_dict["input_end_dt"]           = datetime(year=2020, month=12, day=29, hour=23, minute=0, second=0)
        parm_dict["simulation_start_dt"]    = datetime(year=2020, month=12, day=30, hour=0, minute=0, second=0)
        parm_dict["simulation_end_dt"]      = datetime(year=2020, month=12, day=31, hour=23, minute=0, second=0)
        parm_dict["output_dir"]             = "load_ops_example"
        parm_list = list(parm_dict.values())
        # run the test
        mapemain.main_func(*parm_list)

        # save the output dir to the sub temporary directory
        output_dir_path = parm_dict["output_dir"]
        shutil.move(output_dir_path, self.cwd)

        plot1 = "mmFinalFig.png"
        shutil.move(plot1, self.saving + dir_sep + parm_dict["output_dir"] )

    def test_wind_operations_example(self):
        print("Running ", str(self.id()).split('.')[2])
        # python -m mape_maker "mape_maker/samples/rts_gmlc/wind_operations_example.csv" -st "actuals" -n 2 -bp "ARMA" -is "2020-1-1 01:00:00" -ie "2020-12-29 23:00:00" -sd "2020-12-30 00:00:00" -ed "2020-12-31 23:00:00" -o "wind_operations_example" -s 1234
        parm_dict                           = self._base_dict()
        parm_dict["input_file"]             = self.wind_rts_data
        parm_dict["simulated_timeseries"]   = "actuals"
        parm_dict["number_simulations"]     = 2
        parm_dict["base-process"]           = "ARMA"
        parm_dict["input_start_dt"]         = datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0)
        parm_dict["input_end_dt"]           = datetime(year=2020, month=12, day=29, hour=23, minute=0, second=0)
        parm_dict["simulation_start_dt"]    = datetime(year=2020, month=12, day=30, hour=0, minute=0, second=0)
        parm_dict["simulation_end_dt"]      = datetime(year=2020, month=12, day=31, hour=23, minute=0, second=0)
        parm_dict["output_dir"]             = "wind_ops_example"
        parm_list = list(parm_dict.values())
        # run the test
        mapemain.main_func(*parm_list)

        # save the output dir to the sub temporary directory
        output_dir_path = parm_dict["output_dir"]
        shutil.move(output_dir_path, self.cwd)

        plot1 = "mmFinalFig.png"
        shutil.move(plot1, self.saving + dir_sep + parm_dict["output_dir"] )
if __name__ == "__main__":
    unittest.main()
