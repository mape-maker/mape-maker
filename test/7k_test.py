from mape_maker.Texas_7k import Texas_7k_maker as T7k_main
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
        cls.parser = T7k_main.make_parser()

    def test_solar_mape_maker(self):
        # 1st run, for sum
        parm_dict = {'-ds': "Princeton_test",
                     '-gs': "sum",
                     '-n': "3",
                     '-o': "test_output"}
        parm_list = []
        for i, j in parm_dict.items():
            if j is not None:
                parm_list += [i, j]
            else:
                parm_list += [i]
        args = self.parser.parse_args(parm_list)
        outputpath = 'test_output/simulations_of_target_mape_26.4.csv'
        T7k_main.main(args)
        l = pd.read_csv(outputpath)
        test_numbers = l.iloc[:, 1]  # 2nd column
        single_test_number_1 = test_numbers[1]

        # 2nd run, for sum
        parm_dict = {'-ds': "Princeton_test",
                     '-gs': "sum",
                     '-n': "3",
                     '-o': "test_output_another"}
        parm_list = []
        for i, j in parm_dict.items():
            if j is not None:
                parm_list += [i, j]
            else:
                parm_list += [i]
        args = self.parser.parse_args(parm_list)
        outputpath_2 = 'test_output_another/simulations_of_target_mape_26.4.csv'
        T7k_main.main(args)
        l = pd.read_csv(outputpath_2)
        test_numbers = l.iloc[:, 1]
        single_test_number_2 = test_numbers[1]
        self.assertEqual(single_test_number_1, single_test_number_2)

        # 3rd run, for individual
        parm_dict = {'-ds': "Princeton_test",
                     '-gs': "individual",
                     '-n': "3"}
        parm_list = []
        for i, j in parm_dict.items():
            if j is not None:
                parm_list += [i, j]
            else:
                parm_list += [i]
        args = self.parser.parse_args(parm_list)
        T7k_main.main(args)

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
        try:
            shutil.rmtree('120493_1_Wind')
            shutil.rmtree('150496_1_Wind')
            shutil.rmtree('160281_1_Wind')
            shutil.rmtree('190193_1_Wind')
            shutil.rmtree('220136_1_Wind')
            shutil.rmtree('220216_1_Wind')
        except:
            pass


if __name__ == "__main__":
    unittest.main()
