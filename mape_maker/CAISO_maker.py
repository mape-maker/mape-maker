import os
from mape_maker.__main__ import main as mapemain
import mape_maker
import pandas as pd
from argparse import ArgumentParser
from datetime import timedelta

# TODO: don't have actual for the last day, still allow last day?

p = str(mape_maker.__path__)
p_start = p.find("'")
p_end = p.find("'", p_start + 1)
file_path = p[p_start + 1:p_end] + \
    '/samples/CAISO_wind_operational_data.csv'
# date range: 07-01-2013 to 06-30-2015


def make_parser():
    parser = ArgumentParser()
    parser.add_argument('-ss', '--simulation_start_time',
                        help='start time for simulation',
                        type=str,
                        default=None)
    parser.add_argument('-se', '--simulation_end_time',
                        help='end time for simulation',
                        type=str,
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
    parser.add_argument('-s', '--seed',
                        help='seed for simulation',
                        type=int,
                        default=1234)
    parser.add_argument('-p', '--plot',
                        help='plot simulations',
                        default=False,
                        action='store_true')
    return parser


def main(args):
    if args.output_dir == None:
        raise ValueError("No output directory specified.")
    args.input_xyid_file = file_path
    # dataset does not have a header
    df = pd.read_csv(args.input_xyid_file, header=None)
    start_date = df.iloc[0][0]
    end_date = df.iloc[-1][0]
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    if args.simulation_start_time == None:
        args.simulation_start_time = start_date
    if args.simulation_end_time == None:
        args.simulation_end_time = end_date
    if not (end_date >= pd.to_datetime(args.simulation_start_time) >= start_date):
        raise ValueError(
            'Invalid start time. Valid date range: 2013-07-01 00:00:00 to 2015-06-30 23:00:00')
    if not (end_date >= pd.to_datetime(args.simulation_end_time) >= start_date):
        raise ValueError(
            'Invalid end time. Valid date range: 2013-07-01 00:00:00 to 2015-06-30 23:00:00')

    args.input_xyid_file = file_path
    args.target_scaled_capacity = None
    args.input_sid_file = None
    args.verbosity_output = None
    args.input_start_time = None
    args.input_end_time = None
    args.a = 4
    args.curvature_target = None
    args.mip_gap = 0.3
    args.time_limit = 3600
    args.plot_start_date = 0
    args.verbosity = 2
    args.sid_feature = 'actuals'
    args.base_process = 'ARMA'
    args.load_pickle = False
    args.curvature = False
    args.show_curv_model = False
    args.solver = 'gurobi'
    args.title = None
    args.x_legend = None
    args.scale_by_capacity = 0
    mapemain(args)


if __name__ == '__main__':
    parser = make_parser()
    args = parser.parse_args()
    main(args)

 #  python -m mape_maker.CAISO_maker -o "CAISO_maker_test_output" -n 3 -ss "2015-01-01 00:00:00" -se "2015-06-30 23:00:00"
