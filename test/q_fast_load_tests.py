import tempfile
import pyutilib.th as unittest
import sys
import os.path
import os
import datetime
from datetime import datetime
import shutil
import mape_maker
from mape_maker import __main__ as mapemain

dir_sep = "/"
p = str(mape_maker.__path__)
l = p.find("'")
r = p.find("'", l + 1)
mape_maker_path = p[l + 1:r]
file_path = mape_maker_path + dir_sep + "samples"

# whether to skip the last two tests
quick_test = False
# whether to run only one example
skip_all_but_one = False
# whether to skip the test which always fails
test_known_failure = False


class TestUM(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # path to the RTS Load data
        # self.load_data = file_path + dir_sep + "based_rts_gmlc" + dir_sep + "Load_rts_gmlc_based" +\
        #                  dir_sep + "procssed_file.csv"
        self.load_data = mape_maker_path + dir_sep + "samples" + \
                         dir_sep + "based_rts_gmlc" + dir_sep + "Load_rts_gmlc_based" \
                         + dir_sep + "processed_file.csv"
        self.parser = mapemain.make_parser()

    def test_load_actuals_ARMA(self):
        print("Running ", str(self.id()).split('.')[2])
        parm_dict = {"-xf": self.load_data,
                     "-is": str(datetime(year=2020, month=1, day=1, hour=1, minute=0, second=0)),
                     "-ie": str(datetime(year=2020, month=3, day=30, hour=0, minute=0, second=0)),
                     "-ss": str(datetime(year=2020, month=2, day=10, hour=0, minute=0, second=0)),
                     "-se": str(datetime(year=2020, month=2, day=28, hour=23, minute=0, second=0))}
        parm_list = []
        for i, j in parm_dict.items():
            if j is not None:
                parm_list += [i, j]
            else:
                parm_list += [i]
        # run the test
        args = self.parser.parse_args(parm_list)
        mapemain.main(args)

    def test_load_forecasts_ARMA(self):
        print("Running ", str(self.id()).split('.')[2])
        parm_dict = {"-xf": self.load_data, "-f": "forecasts",
                     "-is": str(datetime(year=2020, month=2, day=1, hour=1, minute=0, second=0)),
                     "-ie": str(datetime(year=2020, month=4, day=30, hour=0, minute=0, second=0)),
                     "-ss": str(datetime(year=2020, month=3, day=10, hour=0, minute=0, second=0)),
                     "-se": str(datetime(year=2020, month=3, day=28, hour=23, minute=0, second=0))}
        parm_list = []
        for i, j in parm_dict.items():
            if j is not None:
                parm_list += [i, j]
            else:
                parm_list += [i]
        # run the test
        args = self.parser.parse_args(parm_list)
        mapemain.main(args)

    def test_load_forecasts_iid(self):
        print("Running ", str(self.id()).split('.')[2])
        parm_dict = {"-xf": self.load_data, "-f": "forecasts", "-bp": "iid",
                     "-is": str(datetime(year=2020, month=1, day=1, hour=1, minute=0, second=0)),
                     "-ie": str(datetime(year=2020, month=3, day=30, hour=0, minute=0, second=0)),
                     "-ss": str(datetime(year=2020, month=2, day=10, hour=0, minute=0, second=0)),
                     "-se": str(datetime(year=2020, month=2, day=28, hour=23, minute=0, second=0))}
        parm_list = []
        for i, j in parm_dict.items():
            if j is not None:
                parm_list += [i, j]
            else:
                parm_list += [i]
        # run the test
        args = self.parser.parse_args(parm_list)
        mapemain.main(args)

    def test_load_actuals_iid(self):
        print("Running ", str(self.id()).split('.')[2])
        parm_dict = {"-xf": self.load_data, "-bp": "iid",
                     "-is": str(datetime(year=2020, month=2, day=1, hour=1, minute=0, second=0)),
                     "-ie": str(datetime(year=2020, month=4, day=30, hour=0, minute=0, second=0)),
                     "-ss": str(datetime(year=2020, month=3, day=10, hour=0, minute=0, second=0)),
                     "-se": str(datetime(year=2020, month=3, day=28, hour=23, minute=0, second=0))}
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
