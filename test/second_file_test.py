import pyutilib.th as unittest
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

    @classmethod
    def setUpClass(self):
        self.parser = mapemain.make_parser()

    def test_bpa_2012_to_2014_actuals_iid_seed_1234(self):
        parm_dict = {"-xf": file_path + dir_sep + "2012-2013_BPA_forecasts_actuals.csv",
                     "-sf": file_path + dir_sep + "wind_total_forecast_actual_070113_063015.csv",
                     "-bp": "iid", "-s": "1234",
                     "-is": str(datetime(year=2012, month=6, day=3, hour=0, minute=0, second=0)),
                     "-ie": str(datetime(year=2014, month=1, day=1, hour=0, minute=0, second=0)),
                     "-ss": str(datetime(year=2015, month=6, day=29, hour=0, minute=0, second=0)),
                     "-se": str(datetime(year=2015, month=6, day=30, hour=0, minute=0, second=0))}
        parm_list = []
        for i, j in parm_dict.items():
            if j is not None:
                parm_list += [i, j]
            else:
                parm_list += [i]
        # run the test
        args = self.parser.parse_args(parm_list)
        mapemain.main(args)

    def test_bpa_2012_to_2013_actuals_iid_seed_1234(self):
        parm_dict = {"-xf": file_path + dir_sep + "2012-2013_BPA_forecasts_actuals.csv",
                     "-sf": file_path + dir_sep + "wind_total_forecast_actual_070113_063015.csv",
                     "-bp": "iid", "-s": "1234",
                     "-is": str(datetime(year=2012, month=6, day=3, hour=0, minute=0, second=0)),
                     "-ie": str(datetime(year=2013, month=8, day=3, hour=0, minute=0, second=0)),
                     "-ss": str(datetime(year=2015, month=6, day=23, hour=0, minute=0, second=0)),
                     "-se": str(datetime(year=2015, month=6, day=30, hour=0, minute=0, second=0))}
        parm_list = []
        for i, j in parm_dict.items():
            if j is not None:
                parm_list += [i, j]
            else:
                parm_list += [i]
        # run the test
        args = self.parser.parse_args(parm_list)
        mapemain.main(args)

    def test_bpa_2012_to_2013_actuals_ARMA_seed_1234(self):
        parm_dict = {"-xf": file_path + dir_sep + "2012-2013_BPA_forecasts_actuals.csv",
                     "-sf": file_path + dir_sep + "wind_total_forecast_actual_070113_063015.csv",
                     "-s": "1234",
                     "-is": str(datetime(year=2012, month=8, day=1, hour=0, minute=0, second=0)),
                     "-ie": str(datetime(year=2013, month=6, day=30, hour=0, minute=0, second=0)),
                     "-ss": str(datetime(year=2013, month=8, day=1, hour=0, minute=0, second=0)),
                     "-se": str(datetime(year=2014, month=6, day=30, hour=0, minute=0, second=0))}
        parm_list = []
        for i, j in parm_dict.items():
            if j is not None:
                parm_list += [i, j]
            else:
                parm_list += [i]
        # run the test
        args = self.parser.parse_args(parm_list)
        mapemain.main(args)

    def test_wind_actuals_ARMA_seed_1234(self):
        parm_dict = {"-xf": file_path + dir_sep + "wind_total_forecast_actual_070113_063015.csv",
                     "-sf": file_path + dir_sep + "rts_gmlc" + dir_sep + "WIND_forecasts_actuals.csv",
                     "-s": "1234",
                     "-is": str(datetime(year=2013, month=8, day=1, hour=0, minute=0, second=0)),
                     "-ie": str(datetime(year=2014, month=6, day=30, hour=23, minute=0, second=0)),
                     "-ss": str(datetime(year=2020, month=2, day=1, hour=0, minute=0, second=0)),
                     "-se": str(datetime(year=2020, month=12, day=31, hour=0, minute=0, second=0))}
        parm_list = []
        for i, j in parm_dict.items():
            if j is not None:
                parm_list += [i, j]
            else:
                parm_list += [i]
        # run the test
        args = self.parser.parse_args(parm_list)
        mapemain.main(args)

    def test_wind_actuals_iid_seed_1234(self):
        parm_dict = {"-xf": file_path + dir_sep + "wind_total_forecast_actual_070113_063015.csv",
                     "-sf": file_path + dir_sep + "rts_gmlc" + dir_sep + "WIND_forecasts_actuals.csv",
                     "-s": "1234", "-bp": "iid",
                     "-is": str(datetime(year=2013, month=8, day=1, hour=0, minute=0, second=0)),
                     "-ie": str(datetime(year=2014, month=6, day=30, hour=23, minute=0, second=0)),
                     "-ss": str(datetime(year=2020, month=4, day=1, hour=0, minute=0, second=0)),
                     "-se": str(datetime(year=2020, month=4, day=8, hour=0, minute=0, second=0))}
        parm_list = []
        for i, j in parm_dict.items():
            if j is not None:
                parm_list += [i, j]
            else:
                parm_list += [i]
        # run the test
        args = self.parser.parse_args(parm_list)
        mapemain.main(args)

    def test_bpa_actuals_iid_seed_1234(self):
        parm_dict = {"-xf": file_path + dir_sep + "2012-2013_BPA_forecasts_actuals.csv",
                     "-sf": file_path + dir_sep + "wind_total_forecast_actual_070113_063015.csv",
                     "-bp": "iid", "-s": "1234",
                     "-is": str(datetime(year=2012, month=8, day=1, hour=0, minute=0, second=0)),
                     "-ie": str(datetime(year=2013, month=6, day=30, hour=0, minute=0, second=0)),
                     "-ss": str(datetime(year=2013, month=8, day=1, hour=0, minute=0, second=0)),
                     "-se": str(datetime(year=2014, month=6, day=30, hour=0, minute=0, second=0))}
        parm_list = []
        for i, j in parm_dict.items():
            if j is not None:
                parm_list += [i, j]
            else:
                parm_list += [i]
        # run the test
        args = self.parser.parse_args(parm_list)
        mapemain.main(args)


if __name__ == "__main__":
    unittest.main()
