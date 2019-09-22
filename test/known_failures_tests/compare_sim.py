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

def find_sim_diff(file1, file2, file3, file4, file5, file6, file7, n):
    dataframe1 = pd.read_csv(file1, index_col=0)
    dataframe2 = pd.read_csv(file2, index_col=0)
    dataframe3 = pd.read_csv(file3, index_col=0)
    dataframe4 = pd.read_csv(file4, index_col=0)
    dataframe5 = pd.read_csv(file5, index_col=0)
    dataframe6 = pd.read_csv(file6, index_col=0)
    dataframe7 = pd.read_csv(file7, index_col=0)

    #renaming the col titles
    dataframe1.columns = ['actuals', 'forecasts']
    dataframe1.index = pd.to_datetime(dataframe1.index)
    dataframe2.columns = ['dt_mape_1', 'dt_mape_2']
    dataframe2.index = pd.to_datetime(dataframe2.index)
    dataframe3.columns = ['dt_mape_c_1', 'dt_mape_c_2']
    dataframe3.index = pd.to_datetime(dataframe3.index)
    dataframe4.columns = ['370_mape_1', '370_mape_2']
    dataframe4.index = pd.to_datetime(dataframe4.index)
    dataframe5.columns = ['370_mape_c_1', '370_mape_c_2']
    dataframe5.index = pd.to_datetime(dataframe5.index)
    dataframe6.columns = ['90_mape_1', '90_mape_2']
    dataframe6.index = pd.to_datetime(dataframe6.index)
    dataframe7.columns = ['90_mape_c_1','90_mape_c_2']
    dataframe7.index = pd.to_datetime(dataframe7.index)

    frames = [dataframe1,dataframe2,dataframe3,dataframe4,dataframe5,dataframe6,dataframe7]
    final_df = pd.concat(frames, axis=1, sort=True)

    #To find the row-wise differences in the second scenario between the three files
    # same mape, with and without curvature
    final_df["dtmape_diff"]  = final_df["dt_mape_2"]  - final_df["dt_mape_c_2"]
    final_df["90mape_diff"]  = final_df["90_mape_2"]   - final_df["90_mape_2"]
    final_df["370mape_diff"] = final_df["370_mape_2"] - final_df["370_mape_c_2"]

    ares =  abs((final_df["actuals"] - final_df["forecasts"]) / final_df["forecasts"])
    dataset_mape  = np.mean(ares)
    print("dataset_mape = ", dataset_mape)
    final_df["input_mape"] = dataset_mape

    r_m_hat = 0
    for x in m_hat.keys():
        if x != 0:
            r_m_hat += m_hat[x]/x
    r_m_hat = r_m_hat/len(m_hat.keys())
    return r_m_hat
    '''
    #to find the mape per scenario
    per_scenario_mare = []
    for i in range(n):
        print("here")
        per_scenario_mare.append("scenario_" + str(i + 1))
        print("simulation_n_" + str(i + 1))
        ares = abs((dataframe2["simulation_n_" + str(i + 1)] - final_df["actuals"]) / final_df["actuals"])
        mare = np.mean(ares)
        per_scenario_mare.append(mare)

        ares = abs((dataframe3["simulation_n_" + str(i + 1)] - final_df["actuals"]) / final_df["actuals"])
        mare = np.mean(ares)
        per_scenario_mare.append(mare)

        ares = abs((dataframe4["simulation_n_" + str(i + 1)] - final_df["actuals"] )/ final_df["actuals"])
        mare = np.mean(ares)
        per_scenario_mare.append(mare)

        ares = abs((dataframe5["simulation_n_" + str(i + 1)] - final_df["actuals"]) / final_df["actuals"])
        mare = np.mean(ares)
        per_scenario_mare.append(mare)

        ares = abs((dataframe6["simulation_n_" + str(i + 1)] - final_df["actuals"]) / final_df["actuals"])
        mare = np.mean(ares)
        per_scenario_mare.append(mare)

        ares = abs((dataframe7["simulation_n_" + str(i + 1)] - final_df["actuals"]) / final_df["actuals"])
        mare = np.mean(ares)
        per_scenario_mare.append(mare)


    print("per_scenario_mare = ")
    print(per_scenario_mare)

    #plotting the differences
    first = list(final_df.keys())[0]
    screen = 1
    index = final_df[first].iloc[screen * 40:(screen + 1) * 40].index
    fig, ax1 = plt.subplots(figsize=(15, 6), dpi=80, facecolor='w', edgecolor='k',
                            num="MapeMaker - Plot of differences between simulations")
    ax1.plot(index, final_df["90mape_diff"].loc[index], "-",  marker="+", color="red",    linewidth=0.5)
    ax1.plot(index, final_df["370mape_diff"].loc[index], "-", marker="+", color="orange", linewidth=0.5)
    ax1.plot(index, final_df["dtmape_diff"].loc[index], "-",  marker="+", color="green",  linewidth=0.5)

    plt.legend(loc='best')
    # saving plot in current directory
    plot_path = file_path + dir_sep + "scenarios_plot"
    plt.savefig(plot_path)

    '''
    # saving final_df as csv file in current directory
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

    '''
    file1_path    = sys.argv[1]
    file2_path    = sys.argv[2]
    file3_path    = sys.argv[3]
    file4_path    = sys.argv[4]
    file5_path    = sys.argv[5]
    file6_path    = sys.argv[6]
    file7_path    = sys.argv[7]
    num_scenarios = sys.argv[8]
    '''
    file1_path    = "../../mape_maker/samples/rts_gmlc/WIND_forecasts_actuals.csv"
    file2_path    = "wind_ops/full_dtmape/full_dtmape.csv"
    file3_path    = "wind_ops/full_dtmape_curvature/full_dtmape_curvature.csv"
    file4_path    = "wind_ops/full_370mape/full_370mape.csv"
    file5_path    = "wind_ops/full_370mape_curvature/full_370mape_curvature.csv"
    file6_path    = "wind_ops/full_90mape/full_90mape.csv"
    file7_path    = "wind_ops/full_90mape_curvature/full_90mape_curvature.csv"
    num_scenarios = 2


    find_sim_diff(file1_path, file2_path, file3_path, file4_path, file5_path, file6_path, file7_path, num_scenarios)

