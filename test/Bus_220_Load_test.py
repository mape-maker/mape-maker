import pyutilib.th as unittest
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

    @classmethod
    def setUpClass(self):
        # path to Bus_220_Load_zone2
        self.parser = mapemain.make_parser()
        self.load_data = file_path + dir_sep + "rts_gmlc" + dir_sep + \
                         "Bus_220_Load_zone2_forecasts_actuals.csv"

    def test_Bus_220_Load_actuals_ARMA(self):
        print("Running ", str(self.id()).split('.')[2])
        parm_dict = {"-xf": self.load_data, "-sf": self.load_data,
                     "-is": str(datetime(year=2020, month=1, day=10, hour=0, minute=0, second=0)),
                     "-ie": str(datetime(year=2020, month=5, day=20, hour=0, minute=0, second=0)),
                     "-ss": str(datetime(year=2020, month=6, day=1, hour=0, minute=0, second=0)),
                     "-se": str(datetime(year=2020, month=6, day=30, hour=23, minute=0, second=0))}
        parm_list = []
        for i, j in parm_dict.items():
            if j is not None:
                parm_list += [i, j]
            else:
                parm_list += [i]
            # run the test
        args = self.parser.parse_args(parm_list)
        mapemain.main(args)

    def test_Bus_220_Load_forecasts_ARMA(self):
        print("Running ", str(self.id()).split('.')[2])
        parm_dict = {"-xf": self.load_data, "-f": "forecasts",
                     "-is": str(datetime(year=2020, month=1, day=10, hour=0, minute=0, second=0)),
                     "-ie": str(datetime(year=2020, month=5, day=20, hour=0, minute=0, second=0)),
                     "-ss": str(datetime(year=2020, month=1, day=11, hour=0, minute=0, second=0)),
                     "-se": str(datetime(year=2020, month=4, day=20, hour=23, minute=0, second=0))}
        parm_list = []
        for i, j in parm_dict.items():
            if j is not None:
                parm_list += [i, j]
            else:
                parm_list += [i]
        # run the test
        args = self.parser.parse_args(parm_list)
        mapemain.main(args)

    def test_Bus_220_Load_actuals_iid(self):
        print("Running ", str(self.id()).split('.')[2])
        parm_dict = {"-xf": self.load_data, "-bp": "iid",
                     "-is": str(datetime(year=2020, month=3, day=20, hour=0, minute=0, second=0)),
                     "-ie": str(datetime(year=2020, month=7, day=20, hour=0, minute=0, second=0)),
                     "-ss": str(datetime(year=2020, month=6, day=1, hour=0, minute=0, second=0)),
                     "-se": str(datetime(year=2020, month=6, day=30, hour=23, minute=0, second=0))}
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
