import sys
import os.path
import os
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt
import numpy as np
import numbers
register_matplotlib_converters()
file_path = os.path.abspath(os.path.dirname(__file__))
dir_sep = '/'

def combine_mape_plot(input_file, output_file, scenario_type, number_of_scenarios):
    """
    This function will compute average scenario mare and plot all the scenario in the file.
    """
    output_dataframe = pd.read_csv(output_file, index_col=0)
    input_dataframe = pd.read_csv(input_file, index_col=0)
    input_dataframe.columns = ['actuals', 'forecasts']
    input_dataframe.index = pd.to_datetime(input_dataframe.index)
    frames = [output_dataframe, input_dataframe]
    final_dataframe = pd.concat(frames, axis=1, sort=True)
    # raise error for missing entries
    # calculating MAPE (using formula from MapeMaker lines 61-62
    ares = abs(final_dataframe["actuals"] - final_dataframe["forecasts"] / final_dataframe["actuals"])
    mare = np.mean(ares)
    mare =  mare/100
    print("mare = ", mare)
    scenario_mare = []
    # computing mare of the simulated scenarios
    if scenario_type == "actuals":
        for i in range(number_of_scenarios):
            ares = abs(final_dataframe["simulation_n_"+str(i+1)] - final_dataframe["forecasts"] / final_dataframe["forecasts"])
            mare = np.mean(ares)/100
            scenario_mare.append(mare)
    else:
        for i in range(number_of_scenarios):
            ares = abs((final_dataframe["simulation_n_"+str(i+1)] - final_dataframe["actuals"]) / final_dataframe["actuals"])
            mare = np.mean(ares)/100
            scenario_mare.append(mare)

    average_scenario_mare = np.mean(scenario_mare )
    print("Average scenario mare is ", average_scenario_mare )
    std_scenario_mare = np.std(scenario_mare)
    print("Standard deviation of mare in scenarios is ", std_scenario_mare )

    # saving final_dataframe as csv file in current directory
    simulation_file_path = os.path.join(file_path, "final_dataframe.csv")
    final_dataframe.to_csv(simulation_file_path)

    # plotting the actuals, forecasts, and the scenarios
    first = list(final_dataframe.keys())[0]
    screen = 1
    index = final_dataframe[first].iloc[screen*40:(screen+1)*40].index
    fig, ax1 = plt.subplots(figsize=(15, 6), dpi=80, facecolor='w', edgecolor='k',
                            num="MapeMaker - Plot of simulations")

    color_list = ["red", "green", "orange", "purple", "brown", "pink", "blue"]

    if number_of_scenarios > 5:
        number_of_scenarios = 5

    for j in range(number_of_scenarios):
        ax1.plot(index, final_dataframe["simulation_n_"+ str(j+1)].loc[index], "-", marker="+",
                 color = color_list[j], linewidth=0.5)

    #ax1.plot(index, final_dataframe["simulation_n_2"].loc[index], "-", marker="+", color="green", linewidth=0.5)
    #ax1.plot(index, final_dataframe["simulation_n_3"].loc[index], "-", marker="+", color="brown", linewidth=0.5)
    #ax1.plot(index, final_dataframe["simulation_n_4"].loc[index], "-", marker="+", color="purple", linewidth=0.5)
    #ax1.plot(index, final_dataframe["simulation_n_5"].loc[index], "-", marker="+", color="orange", linewidth=0.5)

    plt.legend(loc='best')
    # saving plot in current directory
    plot_path = file_path + dir_sep + "scenarios_plot"
    plt.savefig(plot_path)
    return 0

def print_usage(msg):
    print(msg)
    print("Usage: python compute_mape_plot.py input_file_path output_file_path scenario_type")
    sys.exit(1)

if __name__ == '__main__':
    # Format for the command line arguements:
    # python compute_mape_plot.py input_file_path output_file_path scenario_type number_of_scenarios

    if len(sys.argv) != 5:
        print_usage("Need five arguments")

    # example:
    # input_file_path = "../mape_maker/samples/rts_gmlc/Load_forecasts_actuals.csv"
    # output_file_path = "../load_actuals/load_output.csv"
    # scenario_type = "actuals"
    # number_of_scenarios = 3

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    scenario_type = sys.argv[3]
    num_of_scenarios = sys.argv[4]

    if not os.path.exists(input_file_path):
        print_usage(input_file_path + " does not exist.")

    if not os.path.exists(output_file_path):
        print_usage(output_file_path + " does not exist.")

    if (scenario_type != 'actuals') and (scenario_type != 'forecasts'):
        print_usage(scenario_type + " is not a valid input.")

    try:
        num_of_scenarios = int(num_of_scenarios)
    except:
        print_usage(num_of_scenarios + " is not a valid input.")

    combine_mape_plot(input_file_path, output_file_path, scenario_type, num_of_scenarios )