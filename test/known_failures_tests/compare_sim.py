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

def find_sim_diff(file1, file2, file3, file4, file5, file6):
    dataframe1 = pd.read_csv(file1, index_col=0)
    dataframe2 = pd.read_csv(file2, index_col=0)
    dataframe3 = pd.read_csv(file3, index_col=0)
    dataframe4 = pd.read_csv(file4, index_col=0)
    dataframe5 = pd.read_csv(file5, index_col=0)
    dataframe6 = pd.read_csv(file6, index_col=0)


    frames = [dataframe1, dataframe2, dataframe3]
    final_df = pd.concat(frames, axis=1, sort=True)
    #find the difference in the secong scenario between the three files
    final_df["dtmape_diff"] = dataframe1["simulation_n_2"] - dataframe2["simulation_n_2"]
    final_df["90mape_diff"] = dataframe3["simulation_n_2"] - dataframe4["simulation_n_2"]
    final_df["370mape_diff"] = dataframe5["simulation_n_2"] - dataframe6["simulation_n_2"]


    #plotting the differences
    first = list(final_df.keys())[0]
    screen = 1
    index = final_df[first].iloc[screen * 40:(screen + 1) * 40].index
    fig, ax1 = plt.subplots(figsize=(15, 6), dpi=80, facecolor='w', edgecolor='k',
                            num="MapeMaker - Plot of differences between simulations")
    ax1.plot(index, final_df["dtmape_diff"].loc[index], "-", marker="+", color="red", linewidth=0.5)
    ax1.plot(index, final_df["dtmape_diff"].loc[index], "-", marker="+", color="orange", linewidth=0.5)
    ax1.plot(index, final_df["dtmape_diff"].loc[index], "-", marker="+", color="green", linewidth=0.5)

    plt.legend(loc='best')
    # saving plot in current directory
    plot_path = file_path + dir_sep + "scenarios_plot"
    plt.savefig(plot_path)


    # saving final_dataframe as csv file in current directory
    simulation_file_path = os.path.join(file_path, "final_df_cm.csv")
    final_df.to_csv(simulation_file_path)

if __name__ == '__main__':
    # Format for the command line arguements:
    # python compute_sim.py file1_path file2_path file3_path
    # to check mape's affect
    # python compare_sim.py "wind_ops/full_dtmape/fulldtmape.csv"  "wind_ops/full_90mape/full90mape.csv" "wind_ops/full_370mape/full370mape.csv"
    # to check curvature's affect
    # python compare_sim.py "wind_ops/full_dtmape/fulldtmape.csv"  "wind_ops/full_dtmape_curvature/fulldtmapecurv.csv" "wind_ops/full_dtmape_curvature_only/fulldtcurv.csv"
    # to check both
    # python compare_sim.py "wind_ops/full_dtmape/*.csv" "wind_ops/full_dtmape_curvature/*.csv" "wind_ops/full_90mape/*.csv" "wind_ops/full_90mape_curvature/*.csv" "wind_ops/full_370mape/*.csv" "wind_ops/full_370mape_curvature/*.csv"



    file1_path = sys.argv[1]
    file2_path = sys.argv[2]
    file3_path = sys.argv[3]
    file4_path = sys.argv[4]
    file5_path = sys.argv[5]
    file6_path = sys.argv[6]

    find_sim_diff(file1_path, file2_path, file3_path, file4_path, file5_path, file6_path)

