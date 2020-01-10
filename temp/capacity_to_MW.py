import sys
import os.path
import os
import pandas as pd
import numpy as np

def compute_megawatt(input_file, capacity_file):
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

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Need three arguments")
        print("python capacity_to_MW.py input_file capacity_file")

    input_file = sys.argv[1]
    capacity_file = sys.argv[2]

    if not os.path.exists(input_file):
        print_usage(input_file + " does not exist.")

    if not os.path.exists(capacity_file):
        print_usage(capacity_file + " does not exist.")

    compute_megawatt(input_file, capacity_file)

    print("")