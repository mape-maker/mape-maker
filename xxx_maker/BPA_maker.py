import os
from mape_maker.__main__ import main as mapemain
import mape_maker
import pandas as pd
from argparse import ArgumentParser
from datetime import timedelta
# p = str(mape_maker.__path__)
# p_start = p.find("'")
# p_end = p.find("'", p_start + 1)
# file_path = p[p_start + 1:p_end] + \
#     '/samples/2012-2013_BPA_forecasts_actuals.csv'


def make_parser():
    parser = ArgumentParser()
    parser.add_argument('-xf', '--input_xyid_file',
                        help='input file for simulation',
                        type=str, required=True)
    parser.add_argument('-d', '--days_of_simulation',
                        help='days of simulation, simulate the whole dataset if None',
                        type=int,
                        default=None)
    parser.add_argument('-o', '--output_dir',
                        help='path to a directory to save the simulations',
                        type=str,
                        default=None)
    parser.add_argument('-t', '--target_mape',
                        help='mape you want in return, otherwise will take the mape of the dataset',
                        type=float,
                        default=None)
    parser.add_argument('-n', '--simulations_num',
                        help='number of simulations',
                        type=int,
                        default=1)
    parser.add_argument('-ts', '--target_scaled_capacity',
                        help='scale all scenario data by target_capacity/capacity',
                        type=float,
                        default=None)
    return parser


def main(args):
    input_xyid_file = args.input_xyid_file
    df = pd.read_csv(input_xyid_file)
    start_date = df.iloc[0][0]
    start_date = pd.to_datetime(start_date)
    output_dir = args.output_dir
    target_mape = args.target_mape
    simulations_num = args.simulations_num
    target_scaled_capacity = args.target_scaled_capacity

    args.input_sid_file = None
    args.verbosity_output = None
    args.input_start_time = None
    args.input_end_time = None
    args.simulation_start_time = start_date
    args.simulation_end_time = args.simulation_start_time + \
        timedelta(days=args.days_of_simulation)
    args.a = 4
    args.curvature_target = None
    args.mip_gap = 0.3
    args.time_limit = 3600
    args.plot_start_date = 0
    args.seed = None  # TODO: double check this, none in default, 1234 in BPA example
    args.verbosity = 2
    args.sid_feature = 'actuals'
    args.base_process = 'ARMA'
    args.load_pickle = False
    args.curvature = False
    args.show_curv_model = False
    args.plot = True
    args.solver = 'gurobi'
    args.title = None
    args.x_legend = None
    args.scale_by_capacity = 0  # TODO: double check this option
    mapemain(args)


if __name__ == '__main__':
    parser = make_parser()
    args = parser.parse_args()
    main(args)
