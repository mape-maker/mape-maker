import pyutilib.th as unittest
import datetime
from datetime import datetime
import mape_maker
dir_sep = '/'
from mape_maker import __main__ as mapemain
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
        self.parser = mapemain.make_parser()

    def test_CAISO_wind_actuals_ARMA_seed_1234(self):
        parm_dict = {'-xf': self.wind_data, '-s': "1234",
                     '-is': str(datetime(year=2014, month=7, day=1, hour=0, minute=0, second=0)),
                     '-ie': str(datetime(year=2014, month=8, day=1, hour=0, minute=0, second=0)),
                     '-ss': str(datetime(year=2014, month=7, day=2, hour=0, minute=0, second=0)),
                     '-se': str(datetime(year=2014, month=7, day=31, hour=0, minute=0, second=0))}
        parm_list = []
        for i, j in parm_dict.items():
            if j is not None:
                parm_list += [i, j]
            else:
                parm_list += [i]
        # run the test
        args = self.parser.parse_args(parm_list)
        mapemain.main(args)

    def test_CAISO_wind_forecasts_iid_seed_1134(self):
        parm_dict = {"-xf": self.wind_data, "-s": "1134", "-bp": "iid", "-f": "forecasts",
                     "-is": str(datetime(year=2014, month=1, day=1, hour=0, minute=0, second=0)),
                     "-ie": str(datetime(year=2014, month=10, day=1, hour=0, minute=0, second=0)),
                     "-ss": str(datetime(year=2014, month=1, day=2, hour=0, minute=0, second=0)),
                     "-se": str(datetime(year=2014, month=9, day=30, hour=0, minute=0, second=0))}
        parm_list = []
        for i, j in parm_dict.items():
            if j is not None:
                parm_list += [i, j]
            else:
                parm_list += [i]
        # run the test
        args = self.parser.parse_args(parm_list)
        mapemain.main(args)

    def test_CAISO_wind_actuals_iid_seed_1134(self):
        parm_dict = {"-xf": self.wind_data, "-bp": "iid", "-s": "1134",
                     "-is": str(datetime(year=2014, month=1, day=1, hour=0, minute=0, second=0)),
                     "-ie": str(datetime(year=2014, month=10, day=1, hour=0, minute=0, second=0)),
                     "-ss": str(datetime(year=2014, month=1, day=2, hour=0, minute=0, second=0)),
                     "-se": str(datetime(year=2014, month=9, day=30, hour=0, minute=0, second=0))}
        parm_list = []
        for i, j in parm_dict.items():
            if j is not None:
                parm_list += [i, j]
            else:
                parm_list += [i]
        # run the test
        args = self.parser.parse_args(parm_list)
        mapemain.main(args)

    def test_CAISO_wind_forecasts_ARMA_seed_1234(self):
        parm_dict = {"-xf": self.wind_data, "-f": "forecasts", "-s": "1134",
                     "-is": str(datetime(year=2014, month=7, day=1, hour=0, minute=0, second=0)),
                     "-ie": str(datetime(year=2014, month=8, day=1, hour=0, minute=0, second=0)),
                     "-ss": str(datetime(year=2014, month=7, day=2, hour=0, minute=0, second=0)),
                     "-se": str(datetime(year=2014, month=7, day=31, hour=0, minute=0, second=0))}
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
