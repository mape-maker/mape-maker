import sys
import os
import glob
from mape_maker import __main__ as mapemain
from temp.MW_to_capacity import compute_capacity_percentage
from temp.capacity_to_MW import compute_megawatt, plot_megawatt_simulation
dir_sep = '/'


def call_main(output_dir):
    basedict = {"input_file": "solar_capacity_percentage.csv",
                "target_mape": 13,
                "simulated_timeseries": "actuals",
                "base-process": "ARMA",
                "a": 5,
                "output_dir": output_dir,
                "number_simulations": 5,
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
                "verbosity_output": "solar_verbose.log"
                }
    parm_list = list(basedict.values())
    mapemain.main_func(*parm_list)

if __name__ == '__main__':
    input_file = sys.argv[1]
    capacity_file = sys.argv[2]
    simulation_target = sys.argv[3]
    target_mare = sys.argv[3]

    if not os.path.exists(input_file):
        print(input_file + " does not exist.")
        sys.exit(1)

    if not os.path.exists(capacity_file):
        print(capacity_file + " does not exist.")
        sys.exit(1)

    # convert MW into percentage of capacity
    compute_capacity_percentage(input_file, capacity_file)
    # call the mape_maker main function to generate the simulations
    call_main("solar_output")
    # grab the simulation file
    temp_file = "solar_output" + dir_sep + "*.csv"
    mape_output = glob.glob(temp_file)
    # convert the simulation file back into MW
    mw_output = compute_megawatt(mape_output[0], capacity_file)
    # generate the simulation graph
    plot_megawatt_simulation(mw_output, input_file, "", target_mare, simulation_target)







