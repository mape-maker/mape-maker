import os
from mape_maker import __main__ as mapemain
import unittest
import datetime
from datetime import datetime
import mape_maker
import pandas as pd
import shutil
dir_sep = '/'


class TestUM(unittest.TestCase):
    @classmethod
    def setUp(cls):
        p = str(mape_maker.__path__)
        l = p.find("'")
        r = p.find("'", l + 1)
        o = p.rfind('mape_maker')
        mape_maker_path = p[l + 1:r]
        out_path = p[2:o-1]
        cls.wind_data = mape_maker_path + dir_sep + "samples" + \
            dir_sep + "wind_total_forecast_actual_070113_063015.csv"
        cls.parser = mapemain.make_parser()
        # cls.output_1 = out_path + dir_sep + "test" + \
        #     dir_sep + "test_output"
        # cls.output_2 = out_path + dir_sep + "test" + \
        #     dir_sep + "test_output_another"

    def test_CAISO_wind_actuals_cap_scale(self):
        # 1st run, use -ts scale to 100
        parm_dict = {'-xf': self.wind_data, '-s': "1234",
                     '-is': str(datetime(year=2014, month=7, day=1, hour=0, minute=0, second=0)),
                     '-ie': str(datetime(year=2014, month=8, day=1, hour=0, minute=0, second=0)),
                     '-ss': str(datetime(year=2014, month=7, day=2, hour=0, minute=0, second=0)),
                     '-se': str(datetime(year=2014, month=7, day=31, hour=0, minute=0, second=0)),
                     '-v': "0",
                     '-sb': "0",
                     '-ts': "100",
                     '-o': "test_output"}  # output dir
        parm_list = []
        for i, j in parm_dict.items():
            if j is not None:
                parm_list += [i, j]
            else:
                parm_list += [i]
        args = self.parser.parse_args(parm_list)
        outputpath = 'test_output/simulations_of_target_mape_9.2.csv'
        mapemain.main(args)
        l = pd.read_csv(outputpath)
        test_numbers = l.iloc[:, 1]  # 2nd column
        single_test_number_1 = test_numbers[1]

        # 2nd run, same as 1st run
        parm_dict = {'-xf': self.wind_data, '-s': "1234",
                     '-is': str(datetime(year=2014, month=7, day=1, hour=0, minute=0, second=0)),
                     '-ie': str(datetime(year=2014, month=8, day=1, hour=0, minute=0, second=0)),
                     '-ss': str(datetime(year=2014, month=7, day=2, hour=0, minute=0, second=0)),
                     '-se': str(datetime(year=2014, month=7, day=31, hour=0, minute=0, second=0)),
                     '-v': "0",
                     '-sb': "0",
                     '-ts': "100",
                     '-o': "test_output_2"}
        parm_list = []
        for i, j in parm_dict.items():
            if j is not None:
                parm_list += [i, j]
            else:
                parm_list += [i]
        args = self.parser.parse_args(parm_list)
        outputpath_2 = 'test_output_2/simulations_of_target_mape_9.2.csv'
        mapemain.main(args)
        l = pd.read_csv(outputpath_2)
        test_numbers = l.iloc[:, 1]
        single_test_number_2 = test_numbers[1]
        self.assertEqual(single_test_number_1, single_test_number_2)

        df = pd.read_csv(self.wind_data, index_col=0)
        df.index = pd.to_datetime(df.index)
        start = pd.to_datetime('20140701000000')
        end = pd.to_datetime('20140801000000')
        df = df[(df.index >= start) & (df.index <= end)]
        actual = df.iloc[:, 0]
        actual[0]
        cap = actual.max()
        scale = 100/cap
        # 3rd run, manually scale unscaled output
        parm_dict = {'-xf': self.wind_data, '-s': "1234",
                     '-is': str(datetime(year=2014, month=7, day=1, hour=0, minute=0, second=0)),
                     '-ie': str(datetime(year=2014, month=8, day=1, hour=0, minute=0, second=0)),
                     '-ss': str(datetime(year=2014, month=7, day=2, hour=0, minute=0, second=0)),
                     '-se': str(datetime(year=2014, month=7, day=31, hour=0, minute=0, second=0)),
                     '-v': "0",
                     '-sb': "0",
                     '-o': "test_output_3"}
        parm_list = []
        for i, j in parm_dict.items():
            if j is not None:
                parm_list += [i, j]
            else:
                parm_list += [i]
        args = self.parser.parse_args(parm_list)
        outputpath_2 = 'test_output_3/simulations_of_target_mape_9.2.csv'
        mapemain.main(args)
        l = pd.read_csv(outputpath_2)
        test_numbers = l.iloc[:, 1]
        single_test_number_3 = test_numbers[1]*scale
        self.assertAlmostEqual(single_test_number_1, single_test_number_3, 2)

    @classmethod
    def tearDownClass(cls):
        # delete the output dir
        try:
            shutil.rmtree('test_output')
        except:
            pass
        try:
            shutil.rmtree('test_output_2')
        except:
            pass
        try:
            shutil.rmtree('test_output_3')
        except:
            pass


if __name__ == "__main__":
    unittest.main()
