import pandas as pd
from typing import Tuple, List, Sequence
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime
from pandas.plotting import register_matplotlib_converters
from mape_maker.dataset_easy_fix import repair_nan_zeros
register_matplotlib_converters()
pd.set_option('mode.chained_assignment', None)  # prevent SettingWithCopyWarning

"""
Main functions to pretreat the data :

    * pre_treat : get a workable dataframe from the CSV - calling 
        - set_datetime_index 
        - create_errors_columns
        - find_longest_index_sequence and test_for_holes : test the dataset to find holes 

Function to plot the results :
    * plot_from_date : plot the simulation results
    
"""


def pre_treat(logger, path: str = "", type_of_simulation: str = "actuals") -> pd.DataFrame:
    """
    Verifies the consistency of the data, create the errors columns returns the relative error dataframe, the zero data
    frame and the whole dataframe
    :param path: path to the csv file
    :param type_of_simulation: the target column of the simulation
    :return: df
    """
    print("here")
    print(path)
    logger.info(("-"*50 + "\n{}\n" + "-"*50).format("1. Importing and Treating the dataframe to get the {}".format(
        type_of_simulation)))
    df = set_datetime_index(logger, pd.read_csv(path))

    logger.info("testing for holes in the dataframe ...")
    holes, list_of_holes = test_for_holes(df.index)
    if holes:
        for ind_h in list_of_holes:
            logger.info("     * Holes found in the index between {} and {}".format(df.index[ind_h], df.index[ind_h+1]))
    else:
        logger.info("no holes in the index of the dataset. Good to go.")

    df = create_errors_columns(logger, df, type_of_simulation=type_of_simulation)
    df.index = pd.to_datetime(df.index)
    return df


def set_datetime_index(logger, df: pd.DataFrame) -> pd.DataFrame:
    """
    Find correct datetime column and set it as index
    :param df: bunk dataframe
    :return: dataframe
    """
    row, columns = df.iloc[0], df.columns
    date_col = df.columns[0]
    for i in range(len(row)):
        if type(row[i]) == str and pd.to_datetime(row[i]):
            logger.info("Datetime column found : {} replaced by \'datetime\'".format(columns[i]))
            date_col = columns[i]
            break
    df = df.rename(columns={date_col: "datetime"})
    try:
        df["datetime"] = pd.to_datetime(df["datetime"])
    except ValueError:
        logger.error("No datetime indicated in the csv")
    df = df.set_index("datetime")
    return df


def create_errors_columns(logger, df: pd.DataFrame, type_of_simulation: str = "actuals") -> \
        Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Find columns for forecast and actual and compute the following metrics :
        - Error : forecast - actual
        - RE : Relative Error, Error/actual => Creation of a zero_df
        - ARE : Absolute Relative Error, abs(RE)
    :param df:
    :param type_of_simulation:
    :return:
    """
    col_forecasts, col_actuals = df.columns[:2]
    logger.info("Column for forecasts found : {} replaced by \'forecasts\' "
          "\nColumn for actuals found : {} replaced by \'actuals\' ".format(col_forecasts, col_actuals))
    df = df.rename(columns={col_forecasts: "forecasts", col_actuals: "actuals"})
    denominator = "forecasts" if type_of_simulation == "actuals" else "actuals"
    numerator = "actuals" if type_of_simulation == "actuals" else "forecasts"
    df = repair_nan_zeros.replace_negative(logger, df, denominator)
    df["errors"] = df[numerator] - df[denominator]
    return df


def find_longest_index_sequence(index: List[datetime.datetime], n: int, hour_gap: int = 1) -> int:
    """
    Find the longest consecutive sequence in index
    :param index:
    :param n: number of consecutive data you desire
    :param hour_gap: distance between two consecutive data
    :return: first index of the n-consecutive sequence
    """
    following_index = 1
    ind = 0
    while following_index < n and ind < len(index):
        if index[ind+1] - index[ind] == datetime.timedelta(hours=hour_gap):
            following_index += 1
        else:
            following_index = 1
        ind += 1
    return ind - following_index + 1


def test_for_holes(index: List[datetime.datetime], hour_gap: int = 1) -> Tuple[bool, list]:
    """
    Test for holes in the datetime index
    :param index:
    :param hour_gap: distance between two consecutive data
    :return: True if there is at least one hole, the list of these holes
    """
    holes = False
    list_of_holes = []
    ind = 0
    while ind < len(index)-1:
        if index[ind+1] - index[ind] > datetime.timedelta(hours=hour_gap):
            list_of_holes.append(ind)
            holes = True
        ind += 1
    return holes, list_of_holes


def plot_from_date(logger, X, Y, screen, results=None, title: str = "",
                   target_mare=None, ending_features: str = "",
                   x_legend: str = ""):
    """
    Plot forecasts, actuals and simulations
    :param X: timeseries of the input
    :param Y: timeseries of the output
    :param screen: where to begin the screen of plot
    :param results: simulations
    :param title:
    :param target_mare:
    :param ending_features:
    :param x_legend:
    :return:
    """
    first = list(results.keys())[0]
    index = results[first].iloc[screen*40:(screen+1)*40].index
    fig, ax1 = plt.subplots(figsize=(15, 6), dpi=80, facecolor='w', edgecolor='k',
                            num="MapeMaker - Plot of simulations from {} to {}".format(
                                index[0].strftime("%Y-%m-%d"),
                                index[-1].strftime("%Y-%m-%d")))
    color = 'black'

    ax1.set_xlabel('datetime')
    ax1.set_ylabel('Power', color=color)  # we already handled the x-label with ax1
    if Y is not None:
        try:
            ax1.plot(index, Y.loc[index], '--', marker=".", label=ending_features)
        except:
            logger.error ("**** Y Plot failed ****")
            logger.error ("dump of Y.loc[index]")
            logger.error (Y.loc[index])
            logger.error ("end dump")
    try:
        ax1.plot(index, X.loc[index], "-", marker="o", color="black",
                 label=x_legend, linewidth=0.5)
    except:
        logger.warning ("********* WARNING: Plot failed for", x_legend)
        logger.warning ("dumping data: {}".format(X.loc[index]))
        logger.warning ("****** end WARNING ******")
    if results is not None:
        for r in results:
            simulations = results[r]
            for i, c in enumerate(simulations.columns):
                try:
                    ax1.plot(index, simulations[c].loc[index], marker=".",
                             linewidth=0.5, label=r+" s_{}".format(i))
                except:
                    logger.warning ("******* WARNING: Plot failed for simulation {}"\
                           .format(c))
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.legend()

    if title is None:
        title = "MapeMaker - Plot of simulations from {} to {}, Target Mape {}%".format(
                                index[0].strftime("%Y-%m-%d"),
                                index[-1].strftime("%Y-%m-%d"), '%.1f' % (100*target_mare))
    name = "{}\nForecasts, actuals and simulation of {}".format(title, ending_features)
    plt.title(name)
    plt.savefig("mmFinalFig.png")
    logger.info("plot saved to mmFinalFig.png")
    #plt.show()
