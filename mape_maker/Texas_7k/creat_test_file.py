# not intended for users
# convenient for creating small test data site
import pandas as pd


def load_dataset(site):
    if site == "Prelim_Princeton":
        forecast = pd.read_csv(
            'Prelim_Princeton/Scenario0/timeseries_data_files/WIND/DAY_AHEAD_wind.csv')
        actual = pd.read_csv(
            'Prelim_Princeton/Scenario0/timeseries_data_files/WIND/REAL_TIME_wind.csv')
        # first 6 sites
        forecast_test = forecast.iloc[:, :10]
        forecast_test.to_csv(
            "test_Prelim_Princeton_DAY_AHEAD_wind.csv", index=False)
        actual_test = actual.iloc[:, :10]
        actual_test.to_csv(
            "test_Prelim_Princeton_REAL_TIME_wind.csv", index=False)

    if site == "NREL_ECMWF_PEFORM":
        forecast = pd.read_csv(
            'NREL_ECMWF_PEFORM/timeseries_data_files/WIND/DAY_AHEAD_wind.csv')
        actual = pd.read_csv(
            'NREL_ECMWF_PEFORM/timeseries_data_files/WIND/REAL_TIME_wind.csv')
        forecast_test = forecast.iloc[:, :10]
        forecast_test.to_csv(
            "test_NREL_ECMWF_PEFORM_DAY_AHEAD_wind.csv", index=False)
        actual_test = actual.iloc[:, :10]
        actual_test.to_csv(
            "test_NREL_ECMWF_PEFORM_REAL_TIME_wind.csv", index=False)


load_dataset("Prelim_Princeton")
load_dataset("NREL_ECMWF_PEFORM")
