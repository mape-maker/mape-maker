python process_RTS_GMLC_data_s.py "RTS-GMLC/RTS_Data/timeseries_data_files/" "RTS-GMLC/RTS_Data/SourceData/" "prescient_rts_gmlc/timeseries_data_files_noerror/"

python compute_mape_plot.py "../../mape_maker/samples/rts_gmlc/Load_forecasts_actuals.csv" "load_actuals_ARMA/load_scenarios_actuals.csv" "actuals"

python compute_mape_plot.py "../../mape_maker/samples/wind_total_forecast_actual_070113_063015.csv" "../../wind_data_command_2/target_mape__of_the_empirical_dataset-_base_process_ARMA__seed-1234.csv" "actuals"