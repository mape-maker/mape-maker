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
    This function will compute dataset's mape, average scenario mape, and plot upto 5 the scenario in the input file.
    :param input_file: file path to RTS_GMLC's aggregrated WIND, LOAD or POWER csv files
    :param output_file: file path to mape-maker's output for WIND, LOAD or POWER csv files
    :param scenario_type: simulated_timeseries given as input to mape-maker, "actuals" or "forecasts"
    :param number_of_scenarios: given as input to mape-maker, integer value
    :return: prints the mare of the dataset, and the average over the scenarios, and plots upto 5 scenarios;
             also saved the input and output file as a combined csv in the dir of this script
    """

    # read the files into a dataframe
    output_dataframe = pd.read_csv(output_file, index_col=0)
    input_dataframe = pd.read_csv(input_file, index_col=0)
    input_dataframe.columns = ['actuals', 'forecasts']
    input_dataframe.index = pd.to_datetime(input_dataframe.index)
    frames = [output_dataframe, input_dataframe]
    final_dataframe = pd.concat(frames, axis=1, sort=True)

    # calculating MAPE of the input dataset
    ares = abs(final_dataframe["forecasts"] - final_dataframe["actuals"] / final_dataframe["actuals"])
    mare = np.mean(ares)
    mape =  mare/100
    print("The input dataset's mape = ", mape)

    scenario_mape = []
    # computing mape of the simulated scenarios
    if scenario_type == "actuals":
        for i in range(number_of_scenarios):
            ares = abs(final_dataframe["simulation_n_"+str(i+1)] - final_dataframe["forecasts"] / final_dataframe["forecasts"])
            mape = np.mean(ares)/100
            scenario_mape.append(mape)
    else:
        for i in range(number_of_scenarios):
            ares = abs((final_dataframe["simulation_n_"+str(i+1)] - final_dataframe["actuals"]) / final_dataframe["actuals"])
            mape = np.mean(ares)/100
            scenario_mape.append(mape)

    average_scenario_mape = np.mean(scenario_mape )
    print("Average scenario mape is ", average_scenario_mape )
    std_scenario_mape = np.std(scenario_mape)
    print("Standard deviation of mape in scenarios is ", std_scenario_mape )

    # saving the combined final_dataframe as csv file in current directory
    simulation_file_path = os.path.join(file_path, "final_dataframe.csv")
    final_dataframe.to_csv(simulation_file_path)

    # plotting the actuals, forecasts, and upto 5 scenarios in one screen
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

    plt.legend(loc='best')

    # saving plot in current directory
    plot_path = file_path + dir_sep + "scenarios_plot"
    plt.savefig(plot_path)
    return 0


def print_usage(msg):
    print(msg)
    print("Usage: python compute_mape_plot.py input_file_path output_file_path scenario_type num_of_scenarios")
    sys.exit(1)

if __name__ == '__main__':
    # Format for the command line arguements:
    # python compute_mape_plot.py input_file_path output_file_path scenario_type number_of_scenarios
    # python compute_mape_plot.py "../mape_maker/samples/based_rts_gmlc/Load_rts_gmlc_based/processed.file.csv"
    # python compute_mape_plot.py "../mape_maker/samples/based_rts_gmlc/Wind_rts_gmlc_based/processed.file.csv"

    if len(sys.argv) != 5:
        print_usage("Need five arguments")


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
