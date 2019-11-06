from scipy.stats import norm
from scipy import stats
import warnings
import numpy as np
import pandas as pd
import os
import sys
import itertools
import json
import scipy.optimize
from statsmodels.tsa.arima_model import ARIMA
sys.path.append("..")
warnings.filterwarnings('ignore', 'The iteration is not making good progress')
warnings.filterwarnings("ignore")

"""
Main Class to infer ARMA (Auto Regressive Moving Average) coef and simulate base process
    
    * SolverARMA containing :
        - init_tools : loading or finding best arma coefficients and saving the model
        - simulate_base_process_arma : simulate a BP
        - init and save_arma_order : saving and loading the orders

Main function to infer base process :
    * estimate_base_process

Main function to find the best order for modeling the base process :
    * find_best_arma_repr
    
"""


class SolverARMA:
    """
    Find the best coefficents ARMA to model a timeseries
    Simulate auto-correlated samples for the base process
    """
    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), "stored_ARTA_coef/ar_coeffs.json")

    def __init__(self, base_process_hat, name, logger):
        """
        :param base_process_hat: the estimation of the base process over the errors timeseries
        :param name: name of the simulation - used to store the coeffs
        """
        logger.info("\n"+"*"*50 + "{}".format("Solver ARMA") + "*"*50 + "\n")
        self.name = name
        self.logger = logger
        self.arma_order = None
        self.model = None
        self.init_tools(base_process_hat)

    def init_tools(self, base_process):
        pgq = self.init_arma_order()
        if pgq is None:
            pgq = find_best_arma_repr(self.logger, base_process)
            self.save_arma_order(pgq)
        model = ARIMA(base_process, order=pgq)
        self.model = model.fit(disp=0)
        self.logger.info(self.model.summary())
        self.logger.info("-"*60 + "\nSetting up the correct std for the error so that V[Z] = 1")
        n_sigma = setting_correct_sigma(self.model.arparams, self.model.maparams)
        before = self.model.sigma2
        self.model.sigma2 = n_sigma
        self.logger.info("The sigma2 of the estimated model was {} and is now {}".format(before, self.model.sigma2))
        self.logger.info("Testing ...")
        self.simulate_base_process_arma(index=[i for i in range(50000)])

    def simulate_base_process_arma(self, index=None, seed=None):
        n = len(index)
        simulations = np.array([0.]*n)
        ar, ma = self.model.arparams, self.model.maparams
        sigma = self.model.sigma2
        np.random.seed(seed)
        errors = np.random.normal(scale=np.sqrt(sigma), size=n)
        i = len(ar)
        while i < n:
            simulations[i] = np.inner(ar[::-1], simulations[i-len(ar):i]) + np.inner(ma[::-1], errors[i-len(ma):i]) \
                             + errors[i]
            i += 1
        testing_estimation = pd.DataFrame(index=index, columns=["base_process"], data=simulations)
        simulations = norm.cdf(simulations)
        self.logger.info("Checking assumptions. Variance simulated should be close to 1 and is {} \n"
                         "Mean simulated should be close to 0 and is {}".format('%.1f' % np.std(testing_estimation)**2,
                                              '%.1f' % np.mean(testing_estimation)**2))
        simulation = pd.DataFrame(index=index, columns=["base_process"], data=simulations)
        return simulation

    def init_arma_order(self):
        """
        Load the json file storing AR Params and try to find the one corresponding to its name
        :return:
        """
        """ DLW Sept 2019; this should be only with load_pickle
        with open(SolverARMA.filename, 'r') as f:
            ar_params = json.load(f)
        if self.name in ar_params.keys():
            print("Found computed AR Coef {}".format(ar_params[self.name]))
            self.arma_order = ar_params[self.name]
        else:
            print("Did not find pretrained AR Coef, will launch the computation... Takes a few minutes...")
            self.arma_order = None
        """
        self.arma_order = None
        return self.arma_order

    def save_arma_order(self, ar):
        """ DLW sept 2019; restore when the load is restored in init
        with open(SolverARMA.filename, 'r') as f:
            ar_params = json.load(f)
        ar_params[self.name] = list(ar)
        with open(SolverARMA.filename, "w") as f:
            json.dump(ar_params, f)
        print("Saved ar_params")
        ###self.init_arma_order() 
        """
        pass


def setting_correct_sigma(ar, ma):
    n = 20000
    simulations = np.array([0.] * n)
    np.random.seed(11111)

    def sigma(sig):
        sig = abs(sig)
        errors = np.random.normal(scale=np.sqrt(sig), size=n)
        i = len(ar)
        while i < n:
            simulations[i] = np.inner(ar[::-1], simulations[i - len(ar):i]) + np.inner(ma[::-1], errors[i - len(ma):i]) \
                             + errors[i]
            i += 1
        testing_estimation = pd.DataFrame(index=[i for i in range(n)], columns=["base_process"], data=simulations)
        return (float(np.std(testing_estimation))**2 - 1)**2

    new_sigma = abs(scipy.optimize.minimize_scalar(sigma, tol=1e-2).x)
    return new_sigma


def estimate_base_process(x, errors, s_x):
    """
    infer Z_hat from the errors timeries and the estimated beta distributions
    :param x:
    :param errors:
    :param s_x:
    :return:
    """
    base_process = [0.] * len(x)
    for j in range(len(x)):
        p = s_x[x.iloc[j]]
        y = stats.beta.cdf(errors.iloc[j], p[0], p[1], loc=p[2], scale=p[3])
        y = 0.00001 if y == 0 else y
        y = 0.99999 if y == 1 else y
        base_process[j] = norm.ppf(y)
    base_process = pd.Series(index=x.index, data=base_process)
    return base_process


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
                # print(p,d,q, " BIC = {}".format(model_fit.bic))
                logger.info("{} {} {} BIC = {}".format(p,d,q, model_fit.bic))
        except Exception as e:
            logger.info("{} {} {} rejected:".format(p,d,q))
            logger.error(e)
            continue

    logger.info("End search for ARMA parameters.")
    return best_model

