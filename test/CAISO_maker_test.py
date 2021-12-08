from mape_maker import CAISO_maker as CAISOmain
import unittest
import mape_maker
import pandas as pd
import shutil
from datetime import datetime
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
        cls.CAISO_data = mape_maker_path + dir_sep + "samples" + \
            dir_sep + "CAISO_wind_operational_data.csv"
        cls.parser = CAISOmain.make_parser()
        # cls.output_1 = out_path + dir_sep + "test" + \
        #     dir_sep + "test_output"
        # cls.output_2 = out_path + dir_sep + "test" + \
        #     dir_sep + "test_output_another"

    def test_CAISO_maker(self):
        # 1st run
        parm_dict = {'-s': "1234",
                     '-o': "test_output",
                     '-n': "3",
                     '-ss': str(datetime(year=2014, month=7, day=2, hour=0, minute=0, second=0)),
                     '-se': str(datetime(year=2014, month=7, day=31, hour=0, minute=0, second=0))}
        parm_list = []
        for i, j in parm_dict.items():
            if j is not None:
                parm_list += [i, j]
            else:
                parm_list += [i]
        args = self.parser.parse_args(parm_list)
        outputpath = 'test_output/simulations_of_target_mape_9.0.csv'
        CAISOmain.main(args)
        l = pd.read_csv(outputpath)
        test_numbers = l.iloc[:, 1]  # 2nd column
        single_test_number_1 = test_numbers[1]

        # 2nd run
        parm_dict = {'-s': "1234",
                     '-o': "test_output_another",
                     '-n': "3",
                     '-ss': str(datetime(year=2013, month=7, day=1, hour=0, minute=0, second=0)),
                     '-se': str(datetime(year=2014, month=7, day=1, hour=0, minute=0, second=0))}
        parm_list = []
        for i, j in parm_dict.items():
            if j is not None:
                parm_list += [i, j]
            else:
                parm_list += [i]
        args = self.parser.parse_args(parm_list)
        outputpath_2 = 'test_output/simulations_of_target_mape_9.0.csv'
        CAISOmain.main(args)
        l = pd.read_csv(outputpath_2)
        test_numbers = l.iloc[:, 1]
        single_test_number_2 = test_numbers[1]
        self.assertEqual(single_test_number_1, single_test_number_2)

    @classmethod
    def tearDownClass(cls):
        try:
            shutil.rmtree('test_output')
        except:
            pass
        try:
            shutil.rmtree('test_output_another')  # delete the output dir
        except:
            pass


if __name__ == "__main__":
    unittest.main()
