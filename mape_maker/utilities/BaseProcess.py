from scipy.stats import norm
import numpy as np
import pandas as pd
from logging import Logger
import os
import itertools
import scipy.optimize
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.arima.model import ARIMAResults
file_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
loading_bar = "-"*70


class BaseProcess:
    """Class estimating and simulating the base process of an underlying error timeseries

    Notes:
        The base process is a random process (either IID or ARMA) which transformation yields the error.
        The transformation is defined as the composition of the conditional percent point function of the error by
        the gaussian cdf.

    """
    n_init = 10  # for simulation

    def __init__(self, logger: Logger, z_hat: pd.DataFrame = None, base_process: str = "ARMA", name: str = None,
                 load_coeffs: bool = False) -> None:
        """

        Args:
            logger (Logger): the logger of the MapeMaker class
            z_hat (pd.DataFrame): the estimated base process of the error. Defaults to None. In that case, the base process will be
                iid.
            base_process (str): either "ARMA" or "iid". Defaults to "ARMA". In that case, the best order and coefficients of
                the base process will be infered.
            name (str): the name of the dataset. Used to store and load coefficients.
            load_coeffs (bool): if True will load the coefficients stored in a previous run under "name".

        """
        self.logger = logger
        self.base_process = base_process
        self.name = name
        self.outfile_estimation_parameters = os.path.join(file_path,
                                                          "stored_vectors/{}_ARMAmodel.pkl".format(self.name))
        if base_process == "ARMA":
            if load_coeffs:
                try:
                    self.logger.info(
                        loading_bar + "\n ARMA Coefficients have been loaded")
                    self.load()
                except Exception as e:
                    self.logger.error(e)
                    self.logger.error(loading_bar + "\nCouldn't load")
                    self.find_best_model(z_hat.values)
            else:
                self.find_best_model(z_hat.values)
            self.store()
        else:
            self.model = None

    def simulate_base_process(self, x_t):
        simulation = pd.DataFrame(index=x_t.index, columns=["base_process"])
        if self.model is None:  # user wants IID
            base_process = pd.Series(
                index=simulation.index, data=np.random.uniform(0, 1, len(simulation.index)))
        else:
            base_process = self.simulate_arma(index=x_t.index)
            base_process = base_process.iloc[BaseProcess.n_init:]
        simulation["base_process"] = base_process.values
        return simulation

    def simulate_arma(self, index=None):
        n = len(index) + BaseProcess.n_init
        simulations = np.array([0.] * n)
        ar, ma = self.model.arparams, self.model.maparams
        sigma = self.model.sigma2
        errors = np.random.normal(scale=np.sqrt(sigma), size=n)
        i = max(len(ar), len(ma))
        while i < n:
            simulations[i] = np.inner(ar[::-1], simulations[i - len(ar):i]) + np.inner(ma[::-1],
                                                                                       errors[i - len(ma):i]) \
                + errors[i]
            i += 1
        testing_estimation = pd.DataFrame(
            columns=["base_process"], data=simulations)
        simulations = norm.cdf(simulations)
        self.logger.info("Checking assumptions. Variance simulated should be close to 1 and is {} \n"
                         "Mean simulated should be close to 0 and is {}".format(
                             '%.1f' % np.std(testing_estimation) ** 2,
                             '%.1f' % np.mean(testing_estimation) ** 2))
        simulation = pd.DataFrame(columns=["base_process"], data=simulations)
        return simulation

    def setting_correct_sigma(self):
        pass

    def find_best_model(self, z_hat):
        pgq = find_best_arma_repr(self.logger, z_hat)
        model = ARIMA(z_hat, order=pgq)
        self.model = model.fit(disp=0)
        self.logger.info(self.model.summary())
        self.logger.info(
            "\n-Setting up the correct std for the error so that V[Z] = 1")
        n_sigma = setting_correct_sigma(
            self.model.arparams, self.model.maparams)
        before = self.model.sigma2
        self.model.sigma2 = n_sigma
        self.logger.info("The sigma2 of the estimated model was {} and is now {}".format(
            before, self.model.sigma2))
        # self.logger.info("Testing ...")
        return self.model
        # self.order = pgq

    def load(self):
        self.model = ARIMAResults.load(self.outfile_estimation_parameters)

    def store(self):
        self.model.save(self.outfile_estimation_parameters)


def find_best_arma_repr(logger, base_process):
    """
    find the best arma representation for the base_process timeseries according to the BIC criterion
    :param base_process:
    :return:
    """
    ps, ds, qs = list(range(5)), [0], list(range(5))
    best_model, bic = None, np.inf
    logger.info("Start search for ARMA parameters:")
    for p, d, q in itertools.product(ps, ds, qs):
        model = ARIMA(base_process, order=(p, d, q))
        try:
            model_fit = model.fit(disp=0)
            if model_fit.bic < bic:
                best_model = (p, d, q)
                bic = model_fit.bic
                logger.info("{},{},{} BIC = {}".format(p, d, q, model_fit.bic))
        except Exception as e:
            logger.info("{},{},{} rejected:".format(p, d, q))
            logger.error(e)
            continue

    logger.info("End search for ARMA parameters\n")
    return best_model


def setting_correct_sigma(ar, ma):
    n = 20000
    simulations = np.array([0.] * n)
    sig_stream = np.random.RandomState()
    sig_stream.seed(11111)

    def sigma(sig):
        # sig is really the variance
        sig = abs(sig)
        errors = sig_stream.normal(scale=np.sqrt(sig), size=n)
        i = max(len(ar), len(ma))
        while i < n:
            simulations[i] = np.inner(ar[::-1], simulations[i - len(ar):i]) + np.inner(ma[::-1], errors[i - len(ma):i]) \
                + errors[i]
            i += 1
        return (float(np.std(simulations))**2 - 1)**2

    new_sigma = abs(scipy.optimize.minimize_scalar(sigma, tol=1e-2).x)
    return new_sigma
