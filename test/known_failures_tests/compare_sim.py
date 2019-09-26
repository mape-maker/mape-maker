import sys
import os.path
import os
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt
import numpy as np
import csv
register_matplotlib_converters()
file_path = os.path.abspath(os.path.dirname(__file__))
dir_sep = '/'

def compute_mape(file1, file2,file3):
    # input file
    input_file  = pd.read_csv(file1, index_col=0)
    # file with scenarios
    output_file = pd.read_csv(file2, index_col=0)
    #combining the dataframes into a single frame
    frames = [input_file, output_file]
    #creating the final dataset
    final_df = pd.concat(frames, axis=1, sort=True)
    # renaming the col titles
    input_file.columns = ['forecasts','actuals']
    input_file.index = pd.to_datetime(input_file.index)
    output_file.columns = ['scenario_1', 'scenario_2']
    output_file.index = pd.to_datetime(output_file.index)

    # data from input file
    actuals   = input_file["actuals"]
    forecasts = input_file["forecasts"]
    scenario1 = output_file["scenario_1"]
    scenario2 = output_file["scenario_2"]
    ## relative error in the input file
    #final_df["input_errors"] = actuals - forecasts
    ##relative errors in the output file
    #final_df["errors_in_scenario_1"] = output_file['scenario_1'] - input_file["forecasts"]
    #final_df["errors_in_scenario_2"] = output_file['scenario_2'] - input_file["forecasts"]

    # computing mape using error; excluding rows where forecast <= c
    relative_error = 0
    non_zeros = 0
    for i in range(len(forecasts)):
        if forecasts[i] > 0:
            relative_error = relative_error + (abs(actuals[i] - forecasts[i]) /forecasts[i])
            non_zeros = non_zeros + 1

    print("relative_error = ",relative_error)
    print("len(forecasts) = ", len(forecasts))
    print("non_zeros = ", non_zeros)
    input_mape = relative_error/non_zeros * 100
    print("input_mape = ", input_mape)
    print("There are",len(forecasts)-non_zeros,"zeros in the dataset.")


    '''
    #find the mape per scenario

    #plotting
    first = list(final_df.keys())[0]
    screen = 1
    index = final_df[first].iloc[screen * 40:(screen + 1) * 40].index
    fig, ax1 = plt.subplots(figsize=(15, 6), dpi=80, facecolor='w', edgecolor='k',
                            num="MapeMaker - Plot of differences between simulations")
    ax1.plot(index, final_df["actuals"].loc[index], "-",  marker="+", color="red",    linewidth=0.5)
    ax1.plot(index, final_df["forecasts"].loc[index], "-", marker="+", color="orange", linewidth=0.5)
    ax1.plot(index, final_df["scenario_1"].loc[index], "-",  marker="+", color="green",  linewidth=0.5)
    ax1.plot(index, final_df["scenario_2"].loc[index], "-",  marker="+", color="blue",  linewidth=0.5)

    plt.legend(loc='best')
    # saving plot in current directory
    plot_path = file_path + dir_sep + "scenarios_plot"
    plt.savefig(plot_path)

    # saving final_df as csv file in current directory
    simulation_file_path = os.path.join(file_path, "final_df_cm.csv")
    final_df.to_csv(simulation_file_path)
    '''

    simulation_file_path = os.path.join(file_path, "final_df.csv")
    final_df.to_csv(simulation_file_path)

if __name__ == '__main__':
    # Format for the command line arguements:
    # python compute_sim.py input_file_path output_file_path
    '''
    file1_path    = sys.argv[1]
    file2_path    = sys.argv[2]
    num_scenarios = sys.argv[3]
    cutoff_value  = sys.argv[4]
    '''
    #input file
    file1_path    = ".." + dir_sep + ".." + dir_sep + "mape_maker" + dir_sep + "samples" + dir_sep +\
                    "rts_gmlc" + dir_sep + "WIND_forecasts_actuals.csv"
    #simulation from command line
    file2_path    = ".." + dir_sep + ".." + dir_sep + "wind_scenarios" + dir_sep + "scenarios.csv"
    # number of scenarios in the output file
    #num_scenarios = 2
    #forecast <= this value will not be considered when calculating mape
    #cutoff_value = 0
    file3 = ".." + dir_sep + ".." + dir_sep + "mape_maker" + dir_sep + "samples" + dir_sep +\
                    "rts_gmlc" + dir_sep + "WIND_forecasts_actuals_new.csv"

    compute_mape(file1_path, file2_path, file3) #, num_scenarios, cutoff_value)

