import sys
import pandas as pd
import click
import glob
from datetime import datetime as dt
from mape_maker import __main__ as mapemain
import matplotlib.pyplot as plt
import logging
from mape_maker.utilities.df_utilities import plot_from_date, pre_treat

dir_sep = '/'


def click_callback(f):
    return lambda _, __, x: f(x)


def check_date(s):
    try:
        return dt.strptime(s, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise Exception(msg)
    except TypeError:
        return None


@click.command()
@click.argument('input_file')
@click.argument('capacity_file')
@click.option('--target_mape', "-t", default=None, type=float,
              help='mape you want in return otherwise will take the mape of the dataset')
@click.option('--simulated_timeseries', '-st', default="actuals",
              help="feature you want to simulate 'actuals' or 'forecasts'")
@click.option('--base_process', '-bp', default="ARMA", help="method used to this end 'iid' or 'ARMA")
@click.option('--a', '-a', default=4, type=float, help="percent of data on the left or on the right for the estimation")
@click.option('--output_dir', "-o", default=None, help="path to a directory to save the simulations")
@click.option('--number_simulations', '-n', default=1, help="number of simulations")
@click.option('--input_start_dt', '-is', default=None, callback=click_callback(check_date),
              help="start_date for the computation of the distributions, format='Y-m-d %H:%M:%S' ")
@click.option('--input_end_dt', '-ie', default=None, callback=click_callback(check_date),
              help="end_date for the computation of the distributions, format='Y-m-d %H:%M:%S'")
@click.option('--simulation_start_dt', '-sd', default=None, callback=click_callback(check_date),
              help="start_date for the simulation, format='Y-m-d %H:%M:%S' ")
@click.option('--simulation_end_dt', '-ed', default=None, callback=click_callback(check_date),
              help="end_date for the simulation, format='Y-m-d %H:%M:%S'")
@click.option('--title', '-ti', default=None, help="title for the plot")
@click.option('--seed', '-s', default=None, help="random seed")
@click.option('--load_pickle', '-lp', default=False, type=bool, help="Load the pickle file instead of estimating")
@click.option('--curvature', '-c', default=False, help="curvature")
@click.option('--time_limit', '-tl', default=3600, help="time limit of the computation of curvature")
@click.option('--curvature_target', '-ct', default=None, type=float, help="the target of the second difference")
@click.option('--mip_gap', '-m', default=0.3, type=float, help="the curvature mip gap")
@click.option('--solver', '-so', default="gurobi", help="curvature solver")
###@click.option('--full_dataset', '-fd', default=False, type=bool, help="simulation over all the dataset")
@click.option('--latex_output', '-lo', default=False, type=bool, help="write results in latex file")
@click.option('--show', '-sh', default=True, type=bool, help="plot simulations")
@click.option('--verbosity', '-v', default=2, type=int, help="verbosity level")
@click.option('--verbosity_output', '-vo', default=None, help="the output file to save the verbosity")

def main(input_file, capacity_file, target_mape, simulated_timeseries, base_process, a, output_dir, number_simulations,
              input_start_dt, input_end_dt, simulation_start_dt, simulation_end_dt, title, seed, load_pickle, curvature,
              time_limit, curvature_target, mip_gap, solver, latex_output, show, verbosity, verbosity_output):
    # convert MW into percentage of capacity
    compute_capacity_percentage(input_file, capacity_file)
    # call the mape_maker main function to generate the simulations
    mare_embedder = mapemain.main_func(input_file, target_mape, simulated_timeseries, base_process, a, output_dir,
                                       number_simulations, input_start_dt, input_end_dt, simulation_start_dt,
                                       simulation_end_dt, title, seed, load_pickle,
                                       curvature, time_limit, curvature_target, mip_gap, solver, latex_output, show,
                                       verbosity, verbosity_output)
    t = mare_embedder.r_tilde * 100
    # convert the simulation file back into MW
    mw_df = compute_megawatt(capacity_file, output_dir)
    # reset plt
    plt.clf()
    plot_megawatt_simulation(mw_df, input_file, "", round(100 * t, 2), simulated_timeseries)


def compute_megawatt(capacity_file, output_dir):
    # grab the simulation file
    temp_file = output_dir + dir_sep + "*.csv"
    mape_output = glob.glob(temp_file)
    input_file = mape_output[0]
    # generate csv files
    input_df = pd.read_csv(input_file, index_col=0)
    capacity_df = pd.read_csv(capacity_file, index_col=0, )
    if input_df.shape[0] != capacity_df.shape[0]:
        print("Number of rows unmatched")
        print("Input file has", input_df.shape[0], "rows")
        print("Capacity file has", capacity_df.shape[0], "rows")
        sys.exit(1)
    for i in range(0, len(input_df.index)):
        upper_bound = capacity_df.iloc[i, 0]
        input_df.iloc[i, :] = input_df.iloc[i, :] / 100 * upper_bound
    input_df.to_csv("solar_megawatt.csv")
    print("saved as solar_megawatt.csv")
    return input_df


def plot_megawatt_simulation(mw_input, input_file, name_simul, target_mare, simulated_timeseries):
    # initialize logger
    logger = logging.getLogger('mape-maker')
    logging.basicConfig(level=logging.INFO)
    # rename the columns (datetime, forecasts, actuals)
    full_df = pre_treat(logger, path=input_file, type_of_simulation=simulated_timeseries)
    # prepare for ending_features and x_legend
    if simulated_timeseries == "actuals":
        simulated_from = "forecasts"
    elif simulated_timeseries == "forecasts":
        simulated_from = "actuals"
    else:
        print("st should be either actuals or forecasts")
        sys.exit(1)
    # initialize results
    results = {}
    mw_input.index = pd.to_datetime(mw_input.index)
    results[name_simul] = mw_input
    x = full_df[simulated_from]
    y = full_df[simulated_timeseries]
    plot_from_date(logger, x, y, screen=0,
                   results=results, title=" ",
                   target_mare=target_mare, ending_features=simulated_timeseries,
                   x_legend=simulated_from)


def compute_capacity_percentage(input_file, capacity_file):
    input_df = pd.read_csv(input_file, index_col=0)
    capacity_df = pd.read_csv(capacity_file, index_col=0)
    if input_df.shape[0] != capacity_df.shape[0]:
        print("Number of rows unmatched")
        print("Input file has", input_df.shape[0], "rows")
        print("Capacity file has", capacity_df.shape[0], "rows")
        sys.exit(1)
    actual_list, forecast_list = [0], [0]
    for i in range(1, len(input_df.index) - 1):
        upper_bound, previous, past = capacity_df.iloc[i, 0], capacity_df.iloc[i - 1, 0], \
                                      capacity_df.iloc[i + 1, 0]
        actual, forecast = input_df.iloc[i, 1], input_df.iloc[i, 0]
        # set the MW of night hours to 0
        if upper_bound == 0:
            actual_list.append(0)
            forecast_list.append(0)
        # set MW of the hour after sunrise and the hour before sunset to 0
        elif previous == 0 or past == 0:
            actual_list.append(0)
            forecast_list.append(0)
        # if the actual/forecast number is negative, set the capacity to 0
        else:
            if actual < 0:
                actual_list.append(0)
            else:
                actual_list.append(actual / upper_bound * 100)
            if forecast < 0:
                forecast_list.append(0)
            else:
                forecast_list.append(forecast / upper_bound * 100)
    actual_list.append(0)
    forecast_list.append(0)
    output_d = {"forecast": pd.Series(forecast_list),
                "actual": pd.Series(actual_list)}
    df = pd.DataFrame(output_d)
    df.index.name = "datetimes"
    df.index = capacity_df.index
    # fill all the night time values with 10
    df.to_csv("solar_capacity_percentage.csv")
    print("saved as solar_capacity_percentage.csv")

if __name__ == '__main__':
    main()
