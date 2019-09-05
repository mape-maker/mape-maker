import tempfile
import sys
import os.path
import os
import glob
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt
import shutil
from datetime import datetime
import shutil
import mape_maker
import numpy as np
register_matplotlib_converters()
file_path = os.path.abspath(os.path.dirname(__file__))
dir_sep = '/'


def compute_mare_and_plot(input_file, output_file, scenario_type):
    """
    :param input_file:
    :param output_file:
    :param scenario_type:
    :return:
    """
    output_dataframe = pd.read_csv(output_file, index_col=0)
    input_dataframe = pd.read_csv(input_file, index_col=0)
    input_dataframe.columns = ['actuals', 'forecasts']
    input_dataframe.index = pd.to_datetime(input_dataframe.index)
    frames = [output_dataframe, input_dataframe]
    final_dataframe = pd.concat(frames, axis=1, sort=True)

    # raise error for missing entries
    # calculating MAPE (using formula from MapeMaker lines 61-62
    ares = abs(final_dataframe["forecasts"] - final_dataframe["actuals"] / final_dataframe["actuals"])
    mare = np.mean(ares)
    mare =  mare/100
    print("mare = ", mare)
    # computing mare of the simulated scenarios
    if scenario_type == "actuals":
        ares1 = abs(final_dataframe["forecasts"] - final_dataframe["simulation_n_1"] / final_dataframe["simulation_n_1"])
        mare1 = np.mean(ares1)/100
        ares2 = abs(final_dataframe["forecasts"] - final_dataframe["simulation_n_2"] / final_dataframe["simulation_n_2"])
        mare2 = np.mean(ares2)/100
        ares3 = abs(final_dataframe["forecasts"] - final_dataframe["simulation_n_3"] / final_dataframe["simulation_n_3"])
        mare3 = np.mean(ares3)/100
    else:
        ares1 = abs(final_dataframe["simulation_n_1"] - final_dataframe["actuals"] / final_dataframe["actuals"])
        mare1 = np.mean(ares1)/100
        ares2 = abs(final_dataframe["simulation_n_2"] - final_dataframe["actuals"] / final_dataframe["actuals"])
        mare2 = np.mean(ares2)/100
        ares3 = abs(final_dataframe["simulation_n_3"] - final_dataframe["actuals"] / final_dataframe["actuals"])
        mare3 = np.mean(ares3)/100

    scenario_mare = [mare1, mare2, mare3]
    average_scenario_mare = np.mean(scenario_mare )
    print("Average scenario mare is ", average_scenario_mare )
    std_scenario_mare = np.std(scenario_mare)
    print("Standard deviation of mare in scenarios is ", std_scenario_mare )
    # average, sd
    # saving final_dataframe as csv file in current directory
    simulation_file_path = os.path.join(file_path, "final_dataframe.csv")
    final_dataframe.to_csv(simulation_file_path)

    # plotting the actuals, forecasts, and the scenarios
    first = list(final_dataframe.keys())[0]
    screen = 1
    index = final_dataframe[first].iloc[screen*40:(screen+1)*40].index
    fig, ax1 = plt.subplots(figsize=(15, 6), dpi=80, facecolor='w', edgecolor='k',
                            num="MapeMaker - Plot of simulations")
    color = 'black'

    ax1.plot(index, final_dataframe["simulation_n_1"].loc[index], "-", marker="o", color="red", linewidth=0.5)
    ax1.plot(index, final_dataframe["simulation_n_2"].loc[index], "-", marker="o", color="orange", linewidth=0.5)
    ax1.plot(index, final_dataframe["simulation_n_3"].loc[index], "-", marker="o", color="yellow", linewidth=0.5)
    # ax1.plot(index, final_dataframe["simulation_n_4"].loc[index], "-", marker="o", color="green", linewidth=0.5)
    # ax1.plot(index, final_dataframe["simulation_n_5"].loc[index], "-", marker="o", color="pink", linewidth=0.5)

    plt.legend(loc='best')
    # saving plot in current directory
    plot_path = file_path + dir_sep + "scenarios_plot"
    plt.savefig(plot_path)
    return 0

def print_usage(msg):
    print(msg)
    print("Usage: python CAISO_wind_compute_mape.py input_file_path output_file_path scenario_type")
    sys.exit(1)

if __name__ == '__main__':
    # Format for the command line arguements:
    # python CAISO_wind_compute_mape.py input_file_path output_file_path scenario_type
    scenario_type = "forecasts"
    # scenario_type = "actuals"

    if len(sys.argv) != 4:
        print_usage("Need four arguments")

    # example:
    # input_file_path = "../../mape_maker/samples/wind_total_forecast_actual_070113_063015.csv"
    # output_file_path = "../../wind_actuals_iid/target_mape__of_the_empirical_dataset-_base_process_iid__seed-1234.csv"
    # scenario_type = "actuals"
    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    scenario_type = sys.argv[3]

    if not os.path.exists(input_file_path):
        print_usage(input_file_path + " does not exist.")

    if not os.path.exists(output_file_path):
        print_usage(output_file_path + " does not exist.")

    if (scenario_type != 'actuals') and (scenario_type != 'forecasts'):
        print_usage(scenario_type + " does not exist.")

    output_file_list = glob.glob(output_file_path)
    compute_mare_and_plot(input_file_path, output_file_path, scenario_type)