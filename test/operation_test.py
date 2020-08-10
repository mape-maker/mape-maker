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
test_with_error = True


class TestUM(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.parser = mapemain.make_parser()

    # def test_CAISO_actuals_ARMA_seed_1234(self):
    #     print("Running ", str(self.id()).split('.')[2])
    #     parm_dict = {"-xf": file_path + dir_sep + "CAISO_wind_operational_data.csv",
    #                  "-s": "1234",
    #                  "-is": str(datetime(year=2013, month=7, day=1, hour=0, minute=0, second=0)),
    #                  "-ie": str(datetime(year=2013, month=12, day=30, hour=23, minute=0, second=0)),
    #                  "-ss": str(datetime(year=2015, month=6, day=29, hour=23, minute=0, second=0)),
    #                  "-se": str(datetime(year=2015, month=6, day=30, hour=23, minute=0, second=0))}
    #     parm_list = []
    #     for i, j in parm_dict.items():
    #         if j is not None:
    #             parm_list += [i, j]
    #         else:
    #             parm_list += [i]
    #     # run the test
    #     args = self.parser.parse_args(parm_list)
    #     mapemain.main(args)
    #
    # def test_CAISO_actuals_iid_seed_1234(self):
    #     print("Running ", str(self.id()).split('.')[2])
    #     parm_dict = {"-xf": file_path + dir_sep + "CAISO_wind_operational_data.csv",
    #                  "-bp": "iid", "-s": "1234",
    #                  "-is": str(datetime(year=2013, month=7, day=1, hour=0, minute=0, second=0)),
    #                  "-ie": str(datetime(year=2013, month=12, day=30, hour=23, minute=0, second=0)),
    #                  "-ss": str(datetime(year=2015, month=6, day=29, hour=23, minute=0, second=0)),
    #                  "-se": str(datetime(year=2015, month=6, day=30, hour=23, minute=0, second=0))}
    #     parm_list = []
    #     for i, j in parm_dict.items():
    #         if j is not None:
    #             parm_list += [i, j]
    #         else:
    #             parm_list += [i]
    #     # run the test
    #     args = self.parser.parse_args(parm_list)
    #     mapemain.main(args)
    #
    # def test_wind_actuals_ARMA_seed_1234(self):
    #     print("Running ", str(self.id()).split('.')[2])
    #     parm_dict = {"-xf": file_path + dir_sep + "rts_gmlc" + dir_sep + "WIND_forecasts_actuals.csv",
    #                  "-s": "1234",
    #                  "-is": str(datetime(year=2020, month=2, day=1, hour=0, minute=0, second=0)),
    #                  "-ie": str(datetime(year=2020, month=10, day=31, hour=23, minute=0, second=0)),
    #                  "-ss": str(datetime(year=2020, month=11, day=1, hour=0, minute=0, second=0)),
    #                  "-se": str(datetime(year=2020, month=11, day=7, hour=0, minute=0, second=0))}
    #     parm_list = []
    #     for i, j in parm_dict.items():
    #         if j is not None:
    #             parm_list += [i, j]
    #         else:
    #             parm_list += [i]
    #     # run the test
    #     args = self.parser.parse_args(parm_list)
    #     with self.assertRaises(RuntimeError) as context:
    #         mapemain.main(args)
    #     self.assertTrue('< 1, there is a prevalence of high power input in the SID' in str(context.exception))

    def test_wind_forecasts_ARMA_seed_1234(self):
        print("Running ", str(self.id()).split('.')[2])
        parm_dict = {"-xf": file_path + dir_sep + "rts_gmlc" + dir_sep + "WIND_forecasts_actuals.csv",
                     "-sf": file_path + dir_sep + "rts_gmlc" + dir_sep + "WIND_forecasts_actuals.csv",
                     "-f": "forecasts", "-s": "1234",
                     "-is": str(datetime(year=2020, month=2, day=1, hour=0, minute=0, second=0)),
                     "-ie": str(datetime(year=2020, month=8, day=31, hour=23, minute=0, second=0)),
                     "-ss": str(datetime(year=2020, month=11, day=1, hour=0, minute=0, second=0)),
                     "-se": str(datetime(year=2020, month=11, day=7, hour=0, minute=0, second=0))}
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