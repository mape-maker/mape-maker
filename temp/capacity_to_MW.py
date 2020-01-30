import sys
import os
import pandas as pd
import logging
from mape_maker.utilities.df_utilities import plot_from_date, pre_treat

def compute_megawatt(input_file, capacity_file):
    # generate csv files
    input_df = pd.read_csv(input_file, index_col=0)
    capacity_df = pd.read_csv(capacity_file, index_col=0,)
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

def plot_megawatt_simulation(mw_input, orig_file, name_simul, target_mare, st):
    # initialize logger
    logger = logging.getLogger('mape-maker')
    logging.basicConfig(level=logging.INFO)
    # rename the columns (datetime, forecasts, actuals)
    full_df = pre_treat(logger, path=orig_file, type_of_simulation=st)
    # prepare for ending_features and x_legend
    if st == "actuals":
        sf = "forecasts"
    elif st == "forecasts":
        sf = "actuals"
    else:
        print("st should be either actuals or forecasts")
        sys.exit(1)
    # initialize results
    results = {}
    mw_input.index = pd.to_datetime(mw_input.index)
    results[name_simul] = mw_input
    x = full_df[sf]
    y = full_df[st]
    plot_from_date(logger, x, y, screen=0,
                   results=results, title=" ",
                   target_mare=target_mare, ending_features=st,
                   x_legend=sf)

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Need five arguments")
        print("python capacity_to_MW.py input_file capacity_file orig_file name_simul target")

    input_file = sys.argv[1]
    capacity_file = sys.argv[2]
    orig_file = sys.argv[3]
    name_simul = sys.argv[4]
    target = sys.argv[5]


    if not os.path.exists(input_file):
        print(input_file + " does not exist.")
        sys.exit(1)

    if not os.path.exists(capacity_file):
        print(capacity_file + " does not exist.")
        sys.exit(1)

    if not os.path.exists(orig_file):
        print(orig_file + " does not exist.")
        sys.exit(1)

    mw_input = compute_megawatt(input_file, capacity_file)
    plot_megawatt_simulation(mw_input, orig_file, name_simul, 13.2, target)
