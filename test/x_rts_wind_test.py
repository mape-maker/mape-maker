import pyutilib.th as unittest
import datetime
from datetime import datetime
import mape_maker
dir_sep = '/'
from mape_maker import __main__ as mapemain
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

    @classmethod
    def setUpClass(self):
        # path to the RTS wind data
        self.wind_data = file_path + dir_sep + "rts_gmlc" + dir_sep + "WIND_forecasts_actuals.csv"
        self.parser = mapemain.make_parser()

    def test_wind_actuals_ARMA_seed_1234(self):
        print("Running ", str(self.id()).split('.')[2])
        parm_dict = {"-xf": self.wind_data, "-s": "1234",
                     "-ss": str(datetime(year=2020, month=2, day=2, hour=0, minute=0, second=0)),
                     "-se": str(datetime(year=2020, month=3, day=2, hour=0, minute=0, second=0)),
                     "-is": str(datetime(year=2020, month=2, day=1, hour=0, minute=0, second=0)),
                     "-ie": str(datetime(year=2020, month=5, day=1, hour=0, minute=0, second=0))}
        parm_list = []
        for i, j in parm_dict.items():
            if j is not None:
                parm_list += [i, j]
            else:
                parm_list += [i]
        # run the test
        args = self.parser.parse_args(parm_list)
        mapemain.main(args)

    def test_wind_forecasts_ARMA_seed_1234(self):
        print("Running ", str(self.id()).split('.')[2])
        parm_dict = {"-xf": self.wind_data, "-f": "forecasts", "-s": "1234",
                     "-ss": str(datetime(year=2020, month=2, day=2, hour=0, minute=0, second=0)),
                     "-se": str(datetime(year=2020, month=3, day=2, hour=0, minute=0, second=0)),
                     "-is": str(datetime(year=2020, month=2, day=1, hour=0, minute=0, second=0)),
                     "-ie": str(datetime(year=2020, month=5, day=1, hour=0, minute=0, second=0))}
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
        print("Running ", str(self.id()).split('.')[2])
        parm_dict = {"-xf": self.wind_data, "-bp": "iid", "-s": "1234",
                     "-ss": str(datetime(year=2020, month=3, day=2, hour=0, minute=0, second=0)),
                     "-se": str(datetime(year=2020, month=4, day=2, hour=0, minute=0, second=0)),
                     "-is": str(datetime(year=2020, month=3, day=1, hour=0, minute=0, second=0)),
                     "-ie": str(datetime(year=2020, month=6, day=1, hour=0, minute=0, second=0))}
        parm_list = []
        for i, j in parm_dict.items():
            if j is not None:
                parm_list += [i, j]
            else:
                parm_list += [i]
        # run the test
        args = self.parser.parse_args(parm_list)
        mapemain.main(args)

    def test_wind_forecasts_iid_seed_1234(self):
        print("Running ", str(self.id()).split('.')[2])
        parm_dict = {"-xf": self.wind_data, "-f": "forecasts", "-bp": "iid", "-s": "1234",
                     "-ss": str(datetime(year=2020, month=3, day=2, hour=0, minute=0, second=0)),
                     "-se": str(datetime(year=2020, month=4, day=2, hour=0, minute=0, second=0)),
                     "-is": str(datetime(year=2020, month=3, day=1, hour=0, minute=0, second=0)),
                     "-ie": str(datetime(year=2020, month=6, day=1, hour=0, minute=0, second=0))}
        parm_list = []
        for i, j in parm_dict.items():
            if j is not None:
                parm_list += [i, j]
            else:
                parm_list += [i]
        # run the test
        args = self.parser.parse_args(parm_list)
        with self.assertRaises(RuntimeError) as context:
            mapemain.main(args)
        self.assertTrue('< 1, there is a prevalence of high power input in the SID' in str(context.exception))


if __name__ == "__main__":
    unittest.main()
