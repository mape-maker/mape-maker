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

def find_sim_diff(file1, file2, file3):
    dataframe1 = pd.read_csv(file1, index_col=0)
    dataframe2 = pd.read_csv(file2, index_col=0)
    dataframe3 = pd.read_csv(file3, index_col=0)
    dataframe4 = dataframe1["simulation_n_2"]
    frames = [dataframe1, dataframe2, dataframe3]
    final_df = pd.concat(frames, axis=1, sort=True)
    #final_df["df1_diff_df2"] = da

    # saving final_dataframe as csv file in current directory
    simulation_file_path = os.path.join(file_path, "final_df.csv")
    final_df.to_csv(simulation_file_path)

if __name__ == '__main__':
    # Format for the command line arguements:
    # python compute_sim.py file1_path file2_path file3_path
    # python compute_sim.py

    file1_path = sys.argv[1]
    file2_path = sys.argv[2]
    file3_path = sys.argv[3]

    find_sim_diff(file1_path, file2_path, file3_path)

