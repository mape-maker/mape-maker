import os
import pickle
import datetime
import numpy as np
import pandas as pd
from logging import Logger
from typing import Tuple, Dict, List
file_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
loading_bar = "-"*70


class Dataset:
    """an embedder class that saves, separates, and processes an actual/forecast dataset

    Attributes:
        logger (_Logger): Logger to use to store the console output
        name (str): unique name of the dataset with respect to the ending feature.
            Example : if we load "dataset.csv" as the SID to simulate actuals, name = "dataset_toactuals_SID"
        x_t, y_t, e_t, ares_t (pd.DataFrame): timeseries of the independent input data (e.g. "actuals"),
            dependent input data (e.g. "forecasts"), errors and absolute relative errors
        dataset_x (list): sorted list of independent input data
        arma_process (ARMAProcess): ARMA process of the underlying base process
        om (Dict[datasetx, float]): dictionary associating the independent input data to its respective weight in
            the mean absolute relative error computation.
        s_x (Dict[datasetx, beta_coefficient]): dictionary associating the independent input data to its respective
            estimated conditional beta coefficients.
        dataset_info (Dict[str, float]): statistics of the dataset

    """

    def __init__(self, logger: Logger, csv_filepath: str = None, dataset: 'Dataset' = None, start_date: str = None,
                 end_date: str = None, ending_feature: str = "actuals", scale_by_capacity: float = None) -> None:
        """

        Args:
            logger(Logger): logger
            csv_filepath (str): the filepath to the input data csv. Defaults to None. In that case, you must provide with
                an existing object of the class Dataset.
            dataset ('Dataset'): an input dataset, in that case, you will create a nearly identical object, expect it
                will be delimited by start and end_date. Defaults to None. In that case, you must provide with
                a csv_filepath.
            start_date (str): start_date of the input data. Default to None. In that case, start_date is the first date of
                the csv or dataset.
            end_date (str): start_date of the input data. Default to None. In that case, start_date is the first date of
                the csv or dataset.
            ending_feature (str): the name of the dependent variable that will be simulated. Defaults to "actuals".

        """
        self.logger = logger
        self.cap = None
        self.scale_by_capacity = scale_by_capacity
        self.y_name = ending_feature
        if ending_feature == "actuals":
            self.y_name = ending_feature
            self.x_name = "forecasts"
        elif ending_feature == "forecasts":
            self.y_name = ending_feature
            self.x_name = "actuals"
        else:
            raise RuntimeError("Bad ending feature: {}".format(ending_feature))

        start_date, end_date = check_date(start_date), check_date(end_date)
        """
        TODO:
        We need to perform some checks : either dataset is None, either csv_filepath is. Both cannot be None 
        at the same time
        """
        if csv_filepath is not None:  #: then this is a sid
            self.name = csv_filepath.split(
                "/")[-1].split(".")[0] + "_to{}".format(self.y_name)
            self.x_t, self.y_t, self.e_t, self.ares_t, self.full_df = self.cut_timeseries(
                csv_filepath, start_date, end_date)
        else:
            self.name = dataset.name + "_SID"
            self.x_t, self.y_t, self.e_t, self.ares_t = self.get_timeseries_from_dataset(
                dataset, start_date, end_date)
        test_holes(self.logger, self.x_t.index)
        self.dataset_x = get_dataset_x(self.x_t)
        self.n_samples = len(self.x_t)
        self.n_different_samples = len(self.dataset_x)
        self.arma_process = None
        self.om = None  #: weight function
        self.s_x = None  #: conditional distribution
        self.m = None  #: conditional mean absolute error function
        self.m_max = None
        self.dataset_info = self.compute_statistics()
        self.outfile_estimation_parameters = os.path.join(file_path,
                                                          "stored_vectors/{}_parameters.pkl".format(
                                                              self.name))

    def cut_timeseries(self, csv_filepath: str, start_date: datetime.datetime, end_date: datetime.datetime) \
            -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """slice the dataset, process it and computes the errors

        Notes:
            All the dataframes outputted must have datetime objects as indexes

        Args:
            csv_filepath (str): the filepath to the input data csv.
            start_date (datetime): start date to start from
            end_date (datetime): end date to end

        Returns:
            x_t (pd.DataFrame): independent data timeseries
            y_t (pd.DataFrame): dependent data timeseries
            e_t (pd.DataFrame): error timeseries
            ares_t (pd.DataFrame): absolute error timeseries
            df (pd.DataFrame): full data frame

        """
        self.logger.info(
            loading_bar + "\nXY data is being loaded and processed")
        df = pd.read_csv(csv_filepath)
        df = set_index(self, df)
        number_of_columns = df.shape[1]
        if number_of_columns == 2:
            self.logger.info("Column for forecasts found"
                             "\nColumn for actuals found")
            if df.columns[0] == "actuals" or df.columns[1] == "forecasts":
                df = df.rename(
                    columns={list(df)[0]: "actuals", list(df)[1]: "forecasts"})
            else:
                df = df.rename(
                    columns={list(df)[0]: "forecasts", list(df)[1]: "actuals"})
            df[self.x_name] = pd.to_numeric(df[self.x_name])
            df[self.y_name] = pd.to_numeric(df[self.y_name])
            df = replace_negative(self.logger, df, self.x_name)
            df["errors"] = df[self.y_name] - df[self.x_name]
            df["ares_t"] = abs(df["errors"]) / df[self.x_name]
            full_df = df
            df = remove_na(self.logger, self.y_name, df)
            x_t, y_t, e_t, ares_t = df[self.x_name].copy(), df[self.y_name].copy(), \
                df["errors"].copy(), (abs(df["errors"]) / df["ares_t"]).copy()
        elif number_of_columns == 1:
            self.logger.info(
                "Operation mode : One Column for {} found".format(self.x_name))
            df = df.rename(columns={list(df)[0]: self.x_name})
            df[self.x_name] = pd.to_numeric(df[self.x_name])
            df = replace_negative(self.logger, df, self.x_name)
            full_df = df
            x_t, y_t, e_t, ares_t = df[self.x_name].copy(), None, None, None
        else:
            raise AttributeError(
                "There are more than two columns of data in the dataset")

        return slice_timeseries(x_t, start_date, end_date), slice_timeseries(y_t, start_date, end_date), \
            slice_timeseries(e_t, start_date, end_date), slice_timeseries(
                ares_t, start_date, end_date), full_df

    def get_timeseries_from_dataset(self, dataset: 'Dataset', start_date: datetime.datetime, end_date: datetime.datetime) \
            -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """

        Args:
            dataset ('Dataset'): a Dataset object from which we are slicing its 4 instances.
            start_date (datetime): start_date of the slice.
            end_date (datetime): end_date of the slice.

        Returns:
            x_t (pd.DataFrame): independent data timeseries
            y_t (pd.DataFrame): dependent data timeseries
            e_t (pd.DataFrame): error timeseries
            ares_t (pd.DataFrame): absolute error timeseries

        """
        x_t, y_t = slice_timeseries(dataset.full_df[dataset.x_name], start_date, end_date), \
            slice_timeseries(
                dataset.full_df[dataset.y_name], start_date, end_date)
        if sum(y_t.isna()) == len(y_t):
            y_t, e_t, ares_t = None, None, None
        else:
            e_t = y_t - x_t
            ares_t = abs(e_t) / x_t
        return x_t, y_t, e_t, ares_t

    def load_pickle(self) -> bool:
        """loads s_x, m, om, m_max for an XYID

        Notes :
            using the name of the dataset (self.name). Try to unpickle the s_x pickle file.

        Returns:
            bool : if the file existed or not

        """
        # TODO check the class is XYID when loading
        with open(self.outfile_estimation_parameters, 'rb') as f:
            d = pickle.load(f)
            self.s_x = d["s_x"]
            self.m = d["m"]
            self.om = d["om"]
            self.m_max = d["m_max"]
        return True

    def save_pickle(self) -> bool:
        """saves s_x

        Notes :
            using the name of the dataset (self.name). Pickle the s_x pickle file.

        Returns:
            bool : if it worked

        """
        # TODO check the class is XYID when saving
        with open(self.outfile_estimation_parameters, 'wb') as f:
            d = dict([["s_x", self.s_x], ["m", self.m], [
                     "m_max", self.m_max], ["om", self.om]])
            pickle.dump(d, f, pickle.HIGHEST_PROTOCOL)
        return True

    def compute_statistics(self) -> Dict[str, float]:
        """compute and stores useful statistics in self.dataset_info

        Notes:
            The statistics to compute are :
                - "r": the mare of the dataset (if possible otherwise None)
                - "cap": the maximum of dataset_x
                - "r_m": the mare of the estimated distribution of error
                - "d": mean of second-difference of y_t
                - to continue

        Returns: self.dataset_info

        """
        cap = max(self.x_t)
        self.cap = cap
        if self.y_t is not None:
            y = self.y_t.diff(1).diff(1).dropna()
            d = np.mean(abs(y))
        else:
            d = None

        if self.ares_t is not None:
            max_ares = max(self.ares_t[self.x_t != 0])
            dt = self.ares_t[self.ares_t == max_ares].index
            if max_ares > 100:
                self.logger.warning("WARNING: the maximum relative error in the input {}% occurs at {}".
                                    format(round(100 * max_ares), dt[0]))
            mare = np.mean(self.ares_t[self.x_t != 0])
        else:
            mare, max_ares = None, None

        if (self.y_t is None) or (sum(self.y_t.isna()) > 0):
            self.logger.info(
                "-"*60 + "\n\n There are some missing {} => OPERATION MODE\n".format(self.y_name))
            operation = True
        else:
            operation = False

        self.dataset_info = {"r": mare, "cap": cap,
                             "operation": operation, "second_differences": d, "scale_by_capacity": self.scale_by_capacity}
        return self.dataset_info

    def compute_estimation_statistics(self) -> Dict[str, float]:
        if self.m_max is not None and self.m is not None:
            self.dataset_info["r_m_hat"] = get_mare_from_m_hat(
                self.m, self.scale_by_capacity, self.cap)
            self.dataset_info["r_m_max"] = get_mare_from_m_hat(
                self.m_max, self.scale_by_capacity, self.cap)
        return self.dataset_info


def get_mare_from_m_hat(m, scale_by_capacity, cap):
    """
    Get the theorical mare from an error simulated with the estimated distributions
    :param m:
    :return: r_m_hat
    """
    r_m_hat = 0
    for x in m.keys():
        if x != 0:
            if scale_by_capacity == None:
                r_m_hat += m[x] / x
            elif scale_by_capacity == 0:
                r_m_hat += m[x] / cap
            else:
                # TODO: ADD capacity validation
                r_m_hat += m[x] / scale_by_capacity
    r_m_hat = r_m_hat / len(m.keys())
    return r_m_hat


def get_dataset_x(x: pd.DataFrame) -> np.array:
    """

    Args:
        x (pd.Dataframe): the indenpendent input data timeseries
        logger (_Logger): Logger

    Returns:
        dataset_X

    """
    dataset_x = np.array(list(set(x.copy().values)))
    dataset_x.sort()
    return dataset_x


def replace_negative(logger, df, x):
    index = df[df[x] < 0].index
    if len(index) == 0:
        logger.info("No negative X values found")
    else:
        logger.info("Replacing negative values by 0 at indexes : ")
        for i, ind in enumerate(index):
            logger.info(
                "     *{}, value = {}".format(ind, float(df.loc[ind][x])))
            if i > 5:
                logger.info("{} negative values replaced and not displayed"
                            .format(len(index) - 5))
                break
        df[df[x] < 0] = 0

    index = df[df[x] == 0].index
    if len(index) != 0:
        logger.warning("WARNING: {} X values at zero are present".
                       format(len(index)))

    return df


def check_date(s):
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        msg = "Not a valid date: '{0}'".format(s)
        raise Exception(msg)
    except TypeError:
        return None


def slice_timeseries(ts, start_date, end_date):
    if start_date is not None:
        ts = ts.loc[start_date:] if ts is not None else None
    if end_date is not None:
        ts = ts.loc[:end_date] if ts is not None else None
    return ts


def set_index(self, df):
    """
    find datetime column and set it as index
    Args:
        df(DataFrame): a dataframe
    Returns:
        df(DataFrame): a dataframe with datetime as index
    """
    rows = df.iloc[0]
    first_data = df.columns
    if first_data[0].isnumeric() or first_data[1].isnumeric():
        df.loc[-1] = first_data
        df.index = df.index + 1
        df = df.sort_index()
        df.columns = range(len(rows))
    else:
        df.columns = first_data
    for i in range(len(rows)):
        if type(rows[i]) == str and pd.to_datetime(rows[i]):
            self.logger.info("columns for datetime found")
            df.rename(columns={list(df)[i]: "datetime"}, inplace=True)
            break
    try:
        df["datetime"] = pd.to_datetime(df["datetime"])
    except ValueError:
        self.logger.error("No datetime indicated in the csv")
    df = df.set_index("datetime")
    return df


def test_holes(logger: Logger, index: List[datetime.datetime], time_gap: int = 1.0):
    """
    Test holes in the datetime index
    Args:
        logger:
        index (list): a list of datetime index
        time_gap(int): time gap between two consecutive data

    """
    holes = False
    holes_list = []
    for i in range(len(index) - 1):
        if index[i + 1] > index[i] + datetime.timedelta(hours=time_gap):
            holes = True
            holes_list.append(i)
    if holes:
        for i in holes_list:
            logger.warning("     * Holes found in the index between {} and {}".format(index[i],
                                                                                      index[i + 1]))
    else:
        logger.info("no holes in the index of the dataset")


def remove_na(logger, col_name, df):
    if len(df[df[col_name].isna()]) > 0:
        logger.warning("There are some missing {}".format(col_name))
        logger.info("The missing data are removed")
        index_not_na = df[~df[col_name].isna()].index
        df = df.loc[index_not_na]
    return df
