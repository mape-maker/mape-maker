'''
This script contains command line examples for running

    process_RTS_GMLC_data_s.py : to process the rts_gmlc files from github into csv files for MapeMaker
    compute_mape_plot.py       : which computes the average scenario mape, and plots the scenarios from the input files
'''


'''
Example 1: process_RTS_GMLC_data_s.py

    here we take:
    timeseries_path = "RTS-GMLC/RTS_Data/timeseries_data_files/"
    source_path     = "RTS-GMLC/RTS_Data/SourceData/"
    write_path      = "prescient_rts_gmlc/timeseries_data_files_noerror/"
    The user is expected to download the data files from github and store it in a directory,
    and update the paths relative to the python script
    The write_path must be an existing directory
'''
python process_RTS_GMLC_data_s.py "RTS-GMLC/RTS_Data/timeseries_data_files/" "RTS-GMLC/RTS_Data/SourceData/" "prescient_rts_gmlc/timeseries_data_files_noerror/"

###############################################################################
'''
Example 2: compute_mape_plot.py

    here we take:
    input_file_path     = "../mape_maker/samples/rts_gmlc/Load_forecasts_actuals.csv"
    output_file_path    = "../load_actuals_iid/load_scenarios_3.csv"
    scenario_type       = "actuals"
    number_of_scenarios = 3
    The user is expected to create and store the required files in the directory,
    and update the paths relative to the python script
    Right now the code works 1 to 5 scenarios only, but can be updates for more scenarios.
'''
python compute_mape_plot.py "../mape_maker/samples/rts_gmlc/Load_forecasts_actuals.csv" "../load_actuals_iid/load_scenarios_3.csv" "actuals" 3
