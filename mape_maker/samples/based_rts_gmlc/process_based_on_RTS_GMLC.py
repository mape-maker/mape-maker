import pandas as pd
import numpy as np
import glob
import os
import sys


def process_rts_using_threshold(source, write, threshold):
    """
    This takes processed RTS-GMLC time series data and modified the data, if required, using a specified threshold
    :param source: file path to RTS_GMLC's aggregrated WIND, LOAD or POWER csv files
    :param write: existing directory path where the output file will be saved
    :param threshold: used to compare relative error
           if the RE is greater, forecast is will replaced so that the RE becomes equal to the threshold
    :return: writes the processed csv file to the specified write path, and prints the number of rows modified,
            the corresponding datetime, and the mape of the final dataset (modified or not)
    """

    # read the file into a dataframe
    source_data = pd.read_csv(source, index_col=0)
    source_data.columns = ['forecasts', 'actuals']
    source_data.index = pd.to_datetime(source_data.index)
    frame = [source_data]
    final_dataframe = pd.concat(frame, axis=1, sort=True)

    # check if the relative error in each row is less than the threshold,
    # otherwise replace forecast in the row such that RE = threshold
    modified_indexes = []
    for i in range(len(final_dataframe["forecasts"])):
        relative_error = abs((final_dataframe["forecasts"][i] - final_dataframe["actuals"][i])) / final_dataframe["actuals"][i]

        if relative_error > threshold :
            new_value = final_dataframe["actuals"][i] * (1 - threshold)
            final_dataframe["forecasts"][i] = new_value
            modified_indexes.append(i)

        elif -relative_error > threshold :
            new_value = final_dataframe["actuals"][i] * (threshold - 1)
            final_dataframe["forecasts"][i] = new_value
            modified_indexes.append(i)

    # print the number of rows modified
    print("Number of rows modified are", len(modified_indexes), ".")
    # if data is modified, print the corresponding datetime
    if len(modified_indexes) > 0:
        print("The corresponding date and times are: ")
        for i in modified_indexes:
            print(source_data.index[i])

    # calculating the mape of the dataset
    ares = abs(final_dataframe["forecasts"] - final_dataframe["actuals"]) / final_dataframe["actuals"]
    mare = np.mean(ares)
    mape =  mare/100
    print("The mape of the data is ", mape)

    processed_file_path = os.path.join(write, "processed_file.csv")
    final_dataframe.to_csv(processed_file_path)

def print_usage(msg):
    print(msg)
    print("Usage: python process_based_on_rts_gmlc.py source_path write_path threshold")
    sys.exit(1)

if __name__ == '__main__':
    # Format for the command line arguements:
    # python process_based_on_rts_gmlc.py source_path write_path threshold
    # example: python3 process_based_on_rts_gmlc.py "../rts_gmlc/Load_forecasts_actuals.csv" "Load_rts_gmlc_based" 10
    # example: python3 process_based_on_rts_gmlc.py "../rts_gmlc/WIND_forecasts_actuals.csv" "Wind_rts_gmlc_based" 10
    if len(sys.argv) != 4:
        print_usage("Need four arguments")

    source_path = sys.argv[1]
    write_path = sys.argv[2]
    threshold = sys.argv[3]

    if not os.path.exists(source_path):
        print_usage(source_path + " does not exist.")

    if not os.path.exists(write_path):
        print_usage(write_path + " does not exist.")

    try:
        threshold = float(threshold)
    except:
        print_usage(threshold + " is not a valid input.")

    process_rts_using_threshold(source_path, write_path, threshold)