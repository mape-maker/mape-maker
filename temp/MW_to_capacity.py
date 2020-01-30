import sys
import os
import pandas as pd

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
        upper_bound, previous, past = capacity_df.iloc[i, 0], capacity_df.iloc[i - 1, 0],\
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
    if len(sys.argv) != 3:
        print("Need three arguments")
        print("python MW_to_capacity.py input_file capacity_file")

    input_file = sys.argv[1]
    capacity_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(input_file + " does not exist.")
        sys.exit(1)

    if not os.path.exists(capacity_file):
        print(capacity_file + " does not exist.")
        sys.exit(1)

    compute_capacity_percentage(input_file, capacity_file)