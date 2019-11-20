import sys
import os.path
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def compute_mape(input_file, x, y):
    """
    This function will use the for loop to compute the scenarios.
    When x is 0, that row will be skipped.
    :param input_file: The input dataset
    :param x:
    :param y: the target simulation
    :return:
    """
    input_dataframe = pd.read_csv(input_file, index_col=0)
    total_num = len(input_dataframe.index)
    # initialize the sum
    error_sum = 0
    for i in range(0, len(input_dataframe.index)):
        actual_num = input_dataframe.iloc[i, 1]
        forecast_num = input_dataframe.iloc[i, 0]
        if y == 'forecasts':
            # skip the row if y value is equal to 0
            if actual_num == 0:
                total_num -= 1
                continue
            error = abs(forecast_num - actual_num) / actual_num
        if y == 'actuals':
            # skip the row if y value is equal to 0
            if forecast_num == 0:
                total_num -= 1
                continue
            error = abs(forecast_num - actual_num) / forecast_num
        error_sum += error
    mape = error_sum/total_num * 100
    print("mape: ", mape)





def print_usage(msg):
    print(msg)
    print("Usage: python compute_mape_for_loop.py input_file_path scenario_type")
    sys.exit(1)


if __name__ == '__main__':

    # sample command line: python compute_mape_for_loop.py "../mape_maker/samples/rts_gmlc/WIND_forecasts_actuals.csv"  "forecasts"
    input_file_path = sys.argv[1]
    scenario_type = sys.argv[2]

    if not os.path.exists(input_file_path):
        print_usage(input_file_path + " does not exist.")

    if (scenario_type != 'actuals') and (scenario_type != 'forecasts'):
        print_usage(scenario_type + " is not a valid input.")

    if scenario_type == 'actuals':
        x = 'forecasts'
    else:
        x = 'actuals'

    compute_mape(input_file_path, x, scenario_type)

    print("done computation")



