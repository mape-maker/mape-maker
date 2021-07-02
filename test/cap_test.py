# based on q_fast_CAISO_wind_test, uses the wind_total_forecast_actual_070113_063015.csv file

from mape_maker import __main__ as mapemain
import unittest
import datetime
from datetime import datetime
import mape_maker
import pandas as pd
dir_sep = '/'


class TestUM(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        p = str(mape_maker.__path__)
        l = p.find("'")
        r = p.find("'", l + 1)
        mape_maker_path = p[l + 1:r]
        self.wind_data = mape_maker_path + dir_sep + "samples" + \
            dir_sep + "wind_total_forecast_actual_070113_063015.csv"
        self.parser = mapemain.make_parser()

    def test_CAISO_wind_actuals_cap_maxx(self):
        # 1st run
        parm_dict = {'-xf': self.wind_data, '-s': "1234",
                     '-is': str(datetime(year=2014, month=7, day=1, hour=0, minute=0, second=0)),
                     '-ie': str(datetime(year=2014, month=8, day=1, hour=0, minute=0, second=0)),
                     '-ss': str(datetime(year=2014, month=7, day=2, hour=0, minute=0, second=0)),
                     '-se': str(datetime(year=2014, month=7, day=31, hour=0, minute=0, second=0)),
                     '-sb': "10",
                     '-o': "test_output"}  # output dir
        parm_list = []
        for i, j in parm_dict.items():
            if j is not None:
                parm_list += [i, j]
            else:
                parm_list += [i]
        args = self.parser.parse_args(parm_list)
        mapemain.main(args)
        l = pd.read_csv(
            r'/home/naijing/Desktop/work/mape-maker-Naijing/test/test_output/simulations_of_target_mape_9.2.csv')
        test_numbers = l.iloc[:, 1]  # 2nd column
        single_test_number_1 = test_numbers[1]

        # 2nd run
        parm_dict = {'-xf': self.wind_data, '-s': "1234",
                     '-is': str(datetime(year=2014, month=7, day=1, hour=0, minute=0, second=0)),
                     '-ie': str(datetime(year=2014, month=8, day=1, hour=0, minute=0, second=0)),
                     '-ss': str(datetime(year=2014, month=7, day=2, hour=0, minute=0, second=0)),
                     '-se': str(datetime(year=2014, month=7, day=31, hour=0, minute=0, second=0)),
                     '-sb': float(0),
                     '-o': "test_output_another"}
        parm_list = []
        for i, j in parm_dict.items():
            if j is not None:
                parm_list += [i, j]
            else:
                parm_list += [i]
        args = self.parser.parse_args(parm_list)
        mapemain.main(args)
        l = pd.read_csv(
            r'/home/naijing/Desktop/work/mape-maker-Naijing/test/test_output_another/simulations_of_target_mape_9.2.csv')
        test_numbers = l.iloc[:, 1]
        single_test_number_2 = test_numbers[1]
        self.assertEqual(single_test_number_1, single_test_number_2)


if __name__ == "__main__":
    unittest.main()
