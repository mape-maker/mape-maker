from mape_maker.solar import solar_mape_maker as solar_main
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
        cls.solar_data = mape_maker_path + dir_sep + "solar" + \
            dir_sep + "NREL_solar_data.csv"
        cls.parser = solar_main.make_parser()

    def test_solar_mape_maker(self):
        # 1st run
        parm_dict = {'-s': "1234",
                     '-isf': self.solar_data,
                     '-so': "test_output",
                     '-n': "3",
                     '-bp': "iid",
                     '-lc': "37 -103 31 -94 26 -98 32 -107",
                     '-is': str(datetime(year=2018, month=7, day=1, hour=0, minute=0, second=0)),
                     '-ie': str(datetime(year=2018, month=12, day=1, hour=0, minute=0, second=0)),
                     '-ss': str(datetime(year=2018, month=7, day=1, hour=0, minute=0, second=0)),
                     '-se': str(datetime(year=2018, month=7, day=7, hour=0, minute=0, second=0))}
        parm_list = []
        for i, j in parm_dict.items():
            if j is not None:
                parm_list += [i, j]
            else:
                parm_list += [i]
        args = self.parser.parse_args(parm_list)
        outputpath = 'test_output/simulations.csv'
        solar_main.main(args)
        l = pd.read_csv(outputpath)
        test_numbers = l.iloc[:, 1]  # 2nd column
        single_test_number_1 = test_numbers[1]

        # 2nd run
        parm_dict = {'-s': "1234",
                     '-isf': self.solar_data,
                     '-so': "test_output_another",
                     '-n': "3",
                     '-bp': "iid",
                     '-lc': "37 -103 31 -94 26 -98 32 -107",
                     '-is': str(datetime(year=2018, month=7, day=1, hour=0, minute=0, second=0)),
                     '-ie': str(datetime(year=2018, month=12, day=1, hour=0, minute=0, second=0)),
                     '-ss': str(datetime(year=2018, month=7, day=1, hour=0, minute=0, second=0)),
                     '-se': str(datetime(year=2018, month=7, day=7, hour=0, minute=0, second=0))}
        parm_list = []
        for i, j in parm_dict.items():
            if j is not None:
                parm_list += [i, j]
            else:
                parm_list += [i]
        args = self.parser.parse_args(parm_list)
        outputpath_2 = 'test_output/simulations.csv'
        solar_main.main(args)
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
