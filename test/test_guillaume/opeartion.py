import datetime
from datetime import datetime
import mape_maker
from mape_maker import __main__ as mapemain
from mape_maker import main2debug as mapemain2
dir_sep = "/"
p = str(mape_maker.__path__)
l = p.find("'")
r = p.find("'", l+1)
mape_maker_path = p[l+1:r]
file_path = mape_maker_path + dir_sep + "samples"
test_with_error = True

def _basic_dict():
    basedict = {"input_file": "",
                "second_file": None,
                "target_mape": None,
                "simulated_timeseries": "actuals",
                "base-process": "ARMA",
                "a": 4,
                "output_dir": None,
                "number_simulations": 1,
                "input_start_dt": None,
                "input_end_dt": None,
                "simulation_start_dt": None,
                "simulation_end_dt": None,
                "title": None,
                "seed": None,
                "load_pickle": False,
                "curvature": None,
                "time_limit": 3600,
                "curvature_target": None,
                "mip_gap": 0.3,
                "solver": "gurobi",
                "latex_output": False,
                "show": True,
                "verbosity": 2,
                "verbosity_output": None
                }
    return basedict

def test_first():
    """
    here is the command : python -m mape_maker "mape_maker/samples/CAISO_wind_operational_data.csv" -s 1234 -n 5
    -bp "ARMA" -o "Wind_Operation1" -is "2013-7-1 00:00:00" -ie "2015-6-30 23:00:00" -sd "2015-6-29 23:00:00" -ed
    "2015-6-30 23:00:00" :return:
    """
    # print("Running ", str(self.id()).split('.')[2])
    parm_dict = _basic_dict()
    parm_dict["input_file"] = file_path + dir_sep + "CAISO_wind_operational_data.csv"
    parm_dict["simulated_timeseries"] = "actuals"
    parm_dict["number_simulations"] = 5
    parm_dict["output_dir"] = "Wind_Operation1"
    parm_dict["seed"] = 1234
    parm_dict["input_start_dt"] = datetime(year=2013, month=7, day=1, hour=0, minute=0, second=0)
    parm_dict["input_end_dt"] = datetime(year=2015, month=6, day=30, hour=23, minute=0, second=0)
    parm_dict["simulation_start_dt"] = datetime(year=2015, month=6, day=29, hour=23, minute=0, second=0)
    parm_dict["simulation_end_dt"] = datetime(year=2015, month=6, day=30, hour=23, minute=0, second=0)
    parm_list = list(parm_dict.values())
    mapemain.main_func(*parm_list)

def test_second(self):
    """
    here is the command : python -m mape_maker "mape_maker/samples/CAISO_wind_operational_data.csv" -s 1234 -n 5
    -bp "iid" -o "Wind_Operation2" -is "2013-7-1 00:00:00" -ie "2014-6-30 23:00:00" -sd "2015-6-29 23:00:00" -ed
    "2015-6-30 23:00:00" :return:
    """
    # print("Running ", str(self.id()).split('.')[2])
    parm_dict = _basic_dict()
    parm_dict["input_file"] = file_path + dir_sep + "CAISO_wind_operational_data.csv"
    parm_dict["simulated_timeseries"] = "actuals"
    parm_dict["number_simulations"] = 5
    parm_dict["output_dir"] = "Wind_Operation2"
    parm_dict["seed"] = 1234
    parm_dict["input_start_dt"] = datetime(year=2013, month=7, day=1, hour=0, minute=0, second=0)
    parm_dict["input_end_dt"] = datetime(year=2014, month=6, day=30, hour=23, minute=0, second=0)
    parm_dict["simulation_start_dt"] = datetime(year=2015, month=6, day=29, hour=23, minute=0, second=0)
    parm_dict["simulation_end_dt"] = datetime(year=2015, month=6, day=30, hour=23, minute=0, second=0)
    parm_list = list(parm_dict.values())
    mapemain.main_func(*parm_list)


def test_third():
    """
    here is the command : python -m mape_maker "mape_maker/samples/rts_gmlc/WIND_forecasts_actuals.csv" -s 1234
    -n 5 -bp "ARMA" -o "RTS_Operation1" -is "2020-2-1 00:00:00" -ie "2020-10-31 23:00:00" -sd "2020-11-1 0:00:00"
    -ed "2020-11-7 00:00:00" :return:
    """
    # print("Running ", str(self.id()).split('.')[2])
    parm_dict = _basic_dict()
    parm_dict["input_file"] = file_path + dir_sep + "rts_gmlc" + dir_sep + "WIND_forecasts_actuals.csv"
    parm_dict["simulated_timeseries"] = "actuals"
    parm_dict["number_simulations"] = 5
    parm_dict["output_dir"] = "RTS_Operation1"
    parm_dict["seed"] = 1234
    parm_dict["input_start_dt"] = datetime(year=2020, month=2, day=1, hour=0, minute=0, second=0)
    parm_dict["input_end_dt"] = datetime(year=2020, month=10, day=31, hour=23, minute=0, second=0)
    parm_dict["simulation_start_dt"] = datetime(year=2020, month=11, day=1, hour=0, minute=0, second=0)
    parm_dict["simulation_end_dt"] = datetime(year=2020, month=11, day=7, hour=0, minute=0, second=0)
    parm_list = list(parm_dict.values())
    mare_embedder = mapemain2.main_func(*parm_list)

    tmare = None
    curvature = None
    list_of_date_ranges = [[parm_dict["simulation_start_dt"], parm_dict["simulation_end_dt"]]]
    scores = mare_embedder.simulate(second_file=None, target_mare=tmare, base_process="ARMA",
                                    n=1,
                                    full_dataset=False, output_dir="RTS_Operation1",
                                    list_of_date_ranges=list_of_date_ranges, curvature_parameters=None,
                                    latex=None)

    # t = mare_embedder.r_tilde
    # text = "Dataset used : {}\n" \
    #        "Computed Mape from the dataset {}%\n" \
    #        "Mape fit from the dataset {}%\n" \
    #        "Target Mape : {}%\n" \
    #        "Simulated from {} to {}\n" \
    #        "With base process {}\n" \
    #        "Computed {} simulations from {} to {}".format(input_file,
    #                                                       round(100 * mare_embedder.mare, 2),
    #                                                       round(100 * mare_embedder.r_m_hat, 2), round(100 * t, 2),
    #                                                       mare_embedder.x, mare_embedder.y, base_process,
    #                                                       number_simulations,
    #                                                       mare_embedder.start_date.strftime("%Y-%m-%d"),
    #                                                       mare_embedder.end_date.strftime("%Y-%m-%d"))
    #
    # logger.info(text)
    #
    # mare_embedder.save_all_outputs(output_dir)
    # if output_dir is not None:
    #     text = text + "\nOutput stored in directory {}".format(output_dir)
    #
    # if show:
    #     mare_embedder.plot_example(title=title)

    # mare_embedder = mapemain.main_func(*parm_list)


import math


class Solver:

    def demo(self, a, b, c):
        d = b ** 2 - 4 * a * c
        if d > 0:
            disc = math.sqrt(d)
            root1 = (-b + disc) / (2 * a)
            root2 = (-b - disc) / (2 * a)
            return root1, root2
        elif d == 0:
            return -b / (2 * a)
        else:
            return "This equation has no roots"


if __name__ == '__main__':
    solver = Solver()

    while True:
        a = int(input("a: "))
        b = int(input("b: "))
        c = int(input("c: "))
        result = solver.demo(a, b, c)
        print(result)
