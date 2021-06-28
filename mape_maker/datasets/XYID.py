from mape_maker.datasets.Dataset import Dataset
from mape_maker.utilities.BaseProcess import BaseProcess
import numpy as np
from scipy.optimize import fsolve
from scipy.stats import norm
from scipy import stats
from scipy.stats import beta
from scipy import optimize
import pandas as pd
loading_bar = "-"*70


class XYID(Dataset):
    """Input dataset, extends Dataset and implements specific methods to estimate the conditional distribution coefs

    Attributes:
        extends Dataset
        m_max (Dict[datasetx, float]): dictionary of maximum attainable mean absolute error for each x

    """
    len_s_hat = 2000  #: number of elements on which estimate s_hat

    def __init__(self, a: float, base_process: str = "ARMA", xyid_load_pickle: bool = True, **kwargs) -> None:
        """Initiate a XYID object

            a (float): percent/2 of data for estimation samples
            base_process (str): "iid" or "ARMA"
            **kwargs (object): inputs of the Dataset constructor

        """
        super().__init__(**kwargs)
        self.m_max = None  #: dictionary of maximum attainable mean absolute error
        self.a = a
        if xyid_load_pickle:
            try:
                self.load_pickle()
                self.logger.info(
                    loading_bar + "\n Estimation parameters, conditional MAES, weight function have been loaded")
                self.create_arma_process(
                    base_process=base_process, xyid_load_pickle=xyid_load_pickle)
            except Exception as e:
                self.logger.error(e)
                self.logger.error(loading_bar + "\nCouldn't load")
                self.fit(base_process=base_process)
        else:
            self.fit(base_process=base_process)
        self.save_pickle()
        self.compute_estimation_statistics()
        self.logger.info(
            loading_bar + "\nMax MAPE attainable for full dataset {}%".format("%2.f" % (100 * self.dataset_info["r_m_max"])))

    def fit(self, base_process: str = "ARMA", xyid_load_pickle: bool = False):
        """
        estimate parameters, get conditional mean absolute errors, compute statistics, create weight function and
        create ARMA Process
        Args:
            base_process:
            xyid_load_pickle:

        Returns:

        """
        self.logger.info(
            loading_bar + "\nEstimation parameters are being computed\n")
        self.estimate_parameters()
        self.logger.info(
            loading_bar + "\nConditional Mean Absolute Errors are being computed\n")
        self.get_maes_from_parameters()
        self.compute_estimation_statistics()
        self.logger.info(loading_bar + "\nWeight function is being computed\n")
        self.create_weight_function(self.dataset_info.get("scale_by_capacity"))
        self.logger.info(
            loading_bar + "\nBase Process {} is being fitted\n".format(base_process))
        self.create_arma_process(
            base_process=base_process, xyid_load_pickle=xyid_load_pickle)

    def create_arma_process(self, base_process: str = "ARMA", xyid_load_pickle: bool = False):
        """create an ARMAProcess object in self.arma_process

        Args:
            xyid_load_pickle (bool): loads the computed coef (order + coef) if True

        Returns:

        """
        if base_process == "ARMA":
            z_hat = [0.] * self.n_samples
            for j in range(self.n_samples):
                p = self.s_x[self.x_t.iloc[j]]
                y = stats.beta.cdf(
                    self.e_t.iloc[j], p[0], p[1], loc=p[2], scale=p[3])
                y = 0.00001 if y == 0 else y
                y = 0.99999 if y == 1 else y
                z_hat[j] = norm.ppf(y)
            z_hat = pd.Series(index=self.x_t.index, data=z_hat)
        else:
            z_hat = None
        self.arma_process = BaseProcess(self.logger, z_hat=z_hat, base_process=base_process, name=self.name,
                                        load_coeffs=xyid_load_pickle)  #: second we fit an ARMA process and save it

    def estimate_parameters(self):
        """estimate the conditional beta coefficients and store them in self.s_x
        """
        x_bar, s_x_a = self.get_s_hat_datasetx_a()
        self.s_x = dict([(key, []) for key in self.dataset_x])
        p = self.n_samples // 8
        for j, x in enumerate(self.dataset_x):
            i = np.argmin(abs(x_bar - x))
            nx = x_bar[i]
            self.s_x[x] = s_x_a[nx]
            if j % p == 0:
                self.logger.info("     - Closest xbar for x = {} is {},  {}% done"
                                 .format("%.3f" % x, "%.3f" % nx, (round(100 * j / (self.n_samples - 1), 3))))
        return self.s_x

    def get_s_hat_datasetx_a(self):
        """loop over a grid of uniformally distributed real between 0 and cap and return S_hat_dataset_a
        """
        index_search = np.linspace(
            0, self.dataset_info.get("cap"), XYID.len_s_hat)
        beta_parameters = [[0] * 4] * XYID.len_s_hat
        mean_var_sample = [[0] * 2] * XYID.len_s_hat
        x_bar = np.array([0] * XYID.len_s_hat, dtype=float)
        for k, x_ in enumerate(index_search):
            a_ = 1 if x_ == index_search[-1] else self.a
            x_bar[int(k)], beta_parameters[k], mean_var_sample[k] = self.find_parameters(
                x_, a_)
            if k % 50 == 0:
                self.logger.info("{}% of the dataset fit".format(
                    round(100 * k / XYID.len_s_hat, 2)))
        return x_bar, dict([(x_bar[i], beta_parameters[i]) for i in range(XYID.len_s_hat)])

    def find_parameters(self, x_, a_):
        """For a given x_, find the sample with a% on the right and a% on the left, set its bounds (l and s) and
        find the shape parameters with the method of moment

        Args
            x_: real around which to take the sample
            a_: percent/2 of data for estimation samples
        """
        index_x_ = np.argwhere(self.dataset_x >= x_)[0][0]
        half_length_sample = int((a_ / 100) * self.n_different_samples)
        left_bound = index_x_ - half_length_sample if index_x_ - \
            half_length_sample > 0 else 0
        right_bound = index_x_ + half_length_sample if index_x_ + half_length_sample < self.n_different_samples \
            else self.n_different_samples - 1

        interval_index = (self.x_t > self.dataset_x[left_bound]) & (
            self.x_t < self.dataset_x[right_bound])  # strict condition used in v1
        x_bar = np.mean(self.x_t[interval_index])
        error_sample = self.e_t[interval_index]
        mean, var = np.mean(error_sample), np.std(error_sample) ** 2
        abs_lower = - x_bar
        abs_upper = self.dataset_info.get("cap") - x_bar
        if min(error_sample) < abs_lower:
            lower = abs_lower
        else:
            lower = min(error_sample)
        if max(error_sample) > abs_upper:
            upper = self.dataset_info.get("cap") - x_bar - lower
        else:
            upper = max(error_sample) - lower
        [a, b] = fsolve(find_alpha_beta, np.array(
            [1, 1]), args=(lower, upper, mean, var))
        return x_bar, [a, b, lower, upper], [mean, var]

    def get_maes_from_parameters(self):
        """Get the Mean absolute error of each distribution with parameters in s_x
        """
        last_good_parameters = None  # deal with failure to get good beta parameters
        m_hat, m_max = {}, {}
        p = self.n_samples // 16
        for i, x in enumerate(self.dataset_x):
            a, b, l_, s_ = self.s_x[x]
            try:
                sample = beta.rvs(a, b, loc=l_, scale=s_,
                                  size=4000, random_state=1234)
            except:
                self.logger.warning("******* WARNING!! **********")
                self.logger.warning(
                    " beta rvs failed at i={},x={}; a={}, b={}, l_={}, s_={}".format(i, x, a, b, l_, s_))
                if last_good_parameters is None:
                    raise
                else:
                    self.logger.warning(" Using last good beta parameters.")
                    a, b, l_, s_ = last_good_parameters
                    sample = beta.rvs(a, b, loc=l_, scale=s_,
                                      size=4000, random_state=1234)
            last_good_parameters = (a, b, l_, s_)
            opt = optimize.minimize(integrate_a_mean_1d, x0=np.array((l_, s_)),
                                    bounds=((-x, 0), (0, self.dataset_info["cap"])), args=(a, b),
                                    tol=1e-1)
            m_max[x] = max(-opt.fun,
                           ((self.dataset_info["cap"] - x) * a) / (a + b))
            stored_l, stored_s = opt.x
            if i % p == 0:
                self.logger.info(" {}% of the m_max computed".format(
                    "%.1f" % (100 * i / self.n_samples)))
                self.logger.info(" - for input {}, m_max = {} for l {} and s {}".format("%.3f" % x, "%.3f" % m_max[x],
                                                                                        "%.3f" % stored_l,
                                                                                        "%.3f" % stored_s))
            m_hat[x] = np.mean(abs(sample))

        self.m = m_hat
        self.m_max = m_max

    def create_weight_function(self, scale_by_capacity):
        """create the weight function from the mean absolute error s and the estimated r
        :return: om_x
        """
        om = {}
        for x in self.dataset_x:
            if x != 0:
                if scale_by_capacity == None:
                    om[x] = self.m[x] / (self.dataset_info["r_m_hat"] * x)
                elif scale_by_capacity == 0:
                    om[x] = self.m[x] / \
                        (self.dataset_info["r_m_hat"]
                         * self.dataset_info.get("cap"))
                else:
                    om[x] = self.m[x] / \
                        (self.dataset_info["r_m_hat"] * scale_by_capacity)
        self.om = om
        return self.om


def find_alpha_beta(p, *args):
    """
    Return mean of a beta distribution with parameters p, loc and scale - mean of the sample
    and  variance of a beta distribution with parameters p, loc and scale - variance of the sample
    :param p:
    :param args:
    :return:
    """
    loc, scale, mean, var = args
    a, b = p
    return (scale * a) / (a + b) + loc - mean, (scale ** 2 * a * b) / ((a + b) ** 2 * (a + b + 1)) - var


def integrate_a_mean_2d(l_, x_, a=0, b=0, verbose=False):
    if verbose:
        print(l_, x_)
    test = beta.rvs(a, b, loc=l_, scale=x_, size=4000, random_state=1234)
    beta_mare = np.mean(abs(test))
    return beta_mare


def integrate_a_mean_1d(x, a=0, b=0, verbose=False):
    l_, x_ = x
    return -integrate_a_mean_2d(l_, x_, a=a, b=b, verbose=verbose)
