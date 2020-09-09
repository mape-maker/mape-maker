from mape_maker import __main__ as mapemain
import pyutilib.th as unittest
import datetime
from datetime import datetime
import mape_maker
dir_sep = '/'


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

    def test_CAISO_wind_actuals_ARMA_n_200(self):
        parm_dict = {'-xf': self.wind_data, '-s': "1234", '-n': "200", '-o': "wind_actuals_ARMA",
                     '-ss': str(datetime(year=2014, month=7, day=12, hour=0, minute=0, second=0)),
                     '-se': str(datetime(year=2014, month=7, day=13, hour=0, minute=0, second=0))}
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
