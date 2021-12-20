import pandas as pd
import datetime as dt
import numpy as np
import mape_maker
from mape_maker.__main__ import main as mapemain
from argparse import ArgumentParser
import os
import glob


def my_to_datetime(date_str):
    if date_str[8:10] != '24':
        return pd.to_datetime(date_str, format='%Y%m%d%H%M%S')
    # convert all 24 to 00
    date_str = date_str[0:8] + '00' + date_str[10:]
    return pd.to_datetime(date_str, format='%Y%m%d%H%M%S') + \
        dt.timedelta(days=1)


def date_time(df):
    df['dateInt'] = df['Year'].astype(
        str) + df['Month'].astype(str).str.zfill(2) + df['Day'].astype(str).str.zfill(2) \
        + df['Period'].astype(str).str.zfill(2) + '00'+'00'
    df['datetime'] = df.dateInt.apply(my_to_datetime)
    df = df.set_index(['datetime'])
    df = df.drop(['dateInt', 'Year', 'Month', 'Day',
                  'Period'], axis=1)
    return df


def load_dataset(data_source):
    p = str(mape_maker.__path__)
    l = p.find("'")
    r = p.find("'", l + 1)
    mape_maker_path = p[l + 1:r]
    if data_source == 'Princeton_test':
        forecast = pd.read_csv(
            mape_maker_path + "/Texas_7k/Prelim_Princeton/Scenario0/timeseries_data_files/WIND/test_data/test_Prelim_Princeton_DAY_AHEAD_wind.csv")
        actual = pd.read_csv(
            mape_maker_path + "/Texas_7k/Prelim_Princeton/Scenario0/timeseries_data_files/WIND/test_data/test_Prelim_Princeton_REAL_TIME_wind.csv")
        forecast = date_time(forecast)
        actual = date_time(actual)

    elif data_source == 'Princeton':
        forecast = pd.read_csv(
            mape_maker_path + '/Texas_7k/Prelim_Princeton/Scenario0/timeseries_data_files/WIND/DAY_AHEAD_wind.csv')
        actual = pd.read_csv(
            mape_maker_path + '/Texas_7k/Prelim_Princeton/Scenario0/timeseries_data_files/WIND/REAL_TIME_wind.csv')
        forecast = date_time(forecast)
        actual = date_time(actual)

    elif data_source == 'NREL_ECMWF_PEFORM_test':
        forecast = pd.read_csv(
            mape_maker_path + "/Texas_7k/NREL_ECMWF_PEFORM/timeseries_data_files/WIND/test_data/test_NREL_ECMWF_PEFORM_DAY_AHEAD_wind.csv")
        actual = pd.read_csv(
            mape_maker_path + "/Texas_7k/NREL_ECMWF_PEFORM//timeseries_data_files/WIND/test_data/test_NREL_ECMWF_PEFORM_REAL_TIME_wind.csv")
        forecast = date_time(forecast)
        actual = date_time(actual)

    elif data_source == 'NREL_ECMWF_PEFORM':
        forecast = pd.read_csv(
            '../mape_maker/Texas_7k/NREL_ECMWF_PEFORM/timeseries_data_files/WIND/DAY_AHEAD_wind.csv')
        actual = pd.read_csv(
            '../mape_maker/Texas_7k/NREL_ECMWF_PEFORM/timeseries_data_files/WIND/REAL_TIME_wind.csv')
        forecast = date_time(forecast)
        actual = date_time(actual)
    return actual, forecast


def sum_or_indv_sites(args, sum_or_indv, actual, forecast):

    if sum_or_indv == 'sum':
        data_forecast = forecast.sum(axis=1)
        data_actual = actual.sum(axis=1)
        data_sum = pd.DataFrame(data_forecast, columns=[
                                'forecasts'], index=forecast.index)
        data_sum['actuals'] = data_actual
        data_sum.to_csv('data_sum.csv')
        return data_forecast, data_actual
    else:
        for i in range(0, len(forecast.columns)):
            name = str(forecast.columns[i])
            data = pd.DataFrame(index=forecast.index)
            data['forecasts'] = forecast.iloc[:, i]
            data['actuals'] = actual.iloc[:, i]
            data.to_csv('temp_data_for_individual_sites.csv')
            args.input_xyid_file = 'temp_data_for_individual_sites.csv'
            df = pd.read_csv(args.input_xyid_file)
            start_date = df.iloc[0][0]
            end_date = df.iloc[0][-1]
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)
            if args.simulation_start_time == None:
                args.simulation_start_time = start_date
            if args.simulation_end_time == None:
                args.simulation_end_time = end_date
            args.input_sid_file = None
            args.verbosity_output = None
            args.input_start_time = None
            args.input_end_time = None
            args.a = 15
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
            args.plot = False
            args.solver = 'gurobi'
            args.title = None
            args.x_legend = None
            args.output_dir = name
            mapemain(args)
            # code for plot goes here
            if args.t7k_plot == True:
                filename = glob.glob(name+'/'+'*.csv')
                filename = filename[0]
                df = pd.read_csv(filename, index_col=0)
                df.index = pd.to_datetime(df.index)
                df['actual'] = actual.iloc[:, i]
                df['forecast'] = forecast.iloc[:, i]
                act = df.pop("actual")
                df.insert(0, act.name, act)
                fore = df.pop("forecast")
                df.insert(0, fore.name, fore)
                df = df.head(50)
                fig = df.plot(style=['--', '--'])
                fig.figure.savefig(name+'/'+name+'_results')

        os.remove('temp_data_for_individual_sites.csv')


def make_parser():
    parser = ArgumentParser()
    parser.add_argument('-ds', '--data_source',
                        help='the source of simulation data (_test contains smaller datasets for quick test)',
                        choices=['Princeton', 'Princeton_test',
                                 'NREL_ECMWF_PEFORM', 'NREL_ECMWF_PEFORM_test'],
                        default='Princeton_test')
    parser.add_argument('-gs', '--geographic_scale',
                        help='simulation for the sum of all sites or for individual sites',
                        choices=['sum', 'individual'],
                        default='sum')
    parser.add_argument('-ss', '--simulation_start_time',
                        help='start time for simulation',
                        type=str,
                        default=None)
    parser.add_argument('-se', '--simulation_end_time',
                        help='end time for simulation',
                        type=str,
                        default=None)
    parser.add_argument('-o', '--output_dir',
                        help='path to a directory to save the simulations. Required input',
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
    parser.add_argument('-pl', '--t7k_plot',
                        help='True if the user wants to plot the results',
                        default=True,
                        action='store_false')
    parser.add_argument('-sb', '--scale_by_capacity',
                        help='scale by capacity instead of observations '
                        'optionally enter the capacity (enter 0 to use max observation)',
                        type=float,
                        default=None)
    parser.add_argument('-ts', '--target_scaled_capacity',
                        help='scale all scenario data by target_capacity/capacity',
                        type=float,
                        default=None)
    return parser


def main(args):
    args.use_output_as_intermidiate = False
    actual, forecast = load_dataset(args.data_source)
    sum_or_indv_sites(args, args.geographic_scale, actual, forecast)
    if args.geographic_scale == "sum":
        data_forecast, data_actual = sum_or_indv_sites(
            args, args.geographic_scale, actual, forecast)
        if args.output_dir == None:
            raise ValueError("No output directory specified")
        args.input_xyid_file = 'data_sum.csv'
        df = pd.read_csv(args.input_xyid_file)
        start_date = df.iloc[0][0]
        end_date = df.iloc[0][-1]
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        if args.simulation_start_time == None:
            args.simulation_start_time = start_date
        if args.simulation_end_time == None:
            args.simulation_end_time = end_date
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
        args.plot = False
        args.solver = 'gurobi'
        args.title = None
        args.x_legend = None
        mapemain(args)
        os.remove("data_sum.csv")
        name = args.output_dir
        if args.t7k_plot == True:
            filename = glob.glob(name+'/'+'*.csv')
            filename = filename[0]
            df = pd.read_csv(filename, index_col=0)
            df.index = pd.to_datetime(df.index)
            df['actual'] = data_actual
            df['forecast'] = data_forecast
            act = df.pop("actual")
            df.insert(0, act.name, act)
            fore = df.pop("forecast")
            df.insert(0, fore.name, fore)
            df = df.head(50)
            fig = df.plot(style=['--', '--'])
            fig.figure.savefig(name+'/'+name+'_results')


if __name__ == '__main__':
    parser = make_parser()
    args = parser.parse_args()
    main(args)


# python 7k_maker.py -ds "Princeton_test" -gs "individual" -n 2
