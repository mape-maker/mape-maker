import numpy as np
from scipy.stats import beta
import pandas as pd
import mape_maker.utilities.curvature_correction as curvature
from statsmodels.tsa.stattools import acf

"""
Main functions for simulation :

    * simulate_multiple_scenarios :  a loop over the number of simulation
    * simulate_errors_from_base_process calling from_bp_to_errors : simulate the base process and generate the errors 
    sample
    * simulate_output_from_errors calling from_errors_to_simulated_naive : simulate the output from the errors and 
    operate curvature corrections if specified

"""


def simulate_multiple_scenarios(x_sid, s_x_tilde, cap=4500, base_process=None, n=1, seeds=None,
                                curvature_parameters=None):
    """
    For every simulation, simulate the errors with the base_process and the conditional distribution
    then, simulate the output from the errors and add curvature if there are some parameters
    :param x_sid: timeseries of the input from the sid
    :param s_x_tilde:
    :param cap:
    :param base_process:
    :param n:
    :param seeds:
    :param curvature_parameters:
    :return:
    """
    global errors
    if seeds is None:
        seeds = [None] * n
    simulations = pd.DataFrame()
    for i in range(1, n+1):
        raw_errors = simulate_errors_from_base_process(x_sid, s_x_tilde, base_process=base_process, seed=seeds[i-1])
        simulation, errors = simulate_output_from_errors(raw_errors, cap=cap, curvature_parameters=curvature_parameters)
        simulation.name = simulation.name + "_n_{}".format(i)
        simulations = pd.concat([simulations, simulation], axis=1)
    return simulations, errors


def simulate_errors_from_base_process(x_sid, s_x_tilde, base_process=None, seed=None):
    """
    Create a sample of uniformely distributed base process sample in [0,1] and simulate the errors with s_x_tilde
    :param x_sid:
    :param s_x_tilde:
    :param base_process:
    :param seed:
    :return:
    """
    simulation = pd.DataFrame(index=x_sid.index, columns=["errors"])
    simulation.loc[x_sid.index, "x"] = x_sid
    if base_process is None:
        np.random.seed(seed=seed)
        base_process = pd.Series(index=simulation.index, data=np.random.uniform(0, 1, len(simulation.index)))
    else:
        base_process = base_process.simulate_base_process_arma(index=simulation.index, seed=seed)
    simulation["base_process"] = base_process
    simulation["errors"] = simulation.apply(from_bp_to_errors, axis=1, **{"s_x_tilde": s_x_tilde})
    return simulation


def from_bp_to_errors(row, s_x_tilde=None):
    x = row["x"]
    bp = row["base_process"]
    a, b, loc, scale = s_x_tilde[x]
    return beta.ppf(bp, a, b, loc=loc, scale=scale)


def simulate_output_from_errors(raw_errors, cap=4500, curvature_parameters=None):
    """
    From the errors generate a sample of output with curvature if specified
    :param raw_errors:
    :param cap:
    :param curvature_parameters:
    :return:
    """
    simulation = raw_errors.apply(from_errors_to_simulated_naive, axis=1, **{"cap": cap})
    simulation.name = "simulation"
    try:
        if curvature_parameters is not None:
            model = curvature.model_first_second_dif(curvature_parameters["name"],
                                                     curvature_parameters["curvature_target"],
                                                     curvature_parameters["x"],
                                                     raw_errors["errors"], cap=cap)
            simulation = curvature.solve(model, raw_errors.index, solver=curvature_parameters["solver"],
                                         time_limit=curvature_parameters["time_limit"],
                                         mip_gap=curvature_parameters["MIP"], show=False)
            simulation.name = "simulation_curvature"
    except Exception as e:
        print(e)
    return simulation, raw_errors


def from_errors_to_simulated_naive(row, floored=True, simulators=(), floor=0, cap=4500, show_errors=False):
    """
    function returning the simulation x in function of the simulated error
    :param row: one line of a dataframe
    :param floored: apply the floor and cap or not
    :param simulators: function used to recompute a random variable if row is outside of the bounds [floor, cap]
    :param floor: min of the value that your simulation can take
    :param cap: max of the value that your simulation can take
    :return: simulation
    """
    actual = row["x"]
    y = actual + row["errors"]
    if floored:
        if y < floor or y > cap:
            if show_errors is True :
                print("Error : y = {} max is {}, \n   {}".format(y, cap, row))
            if len(simulators) == 2:
                while y < floor:
                    y = simulators[0](np.random.uniform(0, 1, 1))[0]
                while y > cap:
                    y = simulators[1](np.random.uniform(0, 1, 1))[0]
            else:
                y = floor if y < floor else cap
    return y


"""
Main functions for scoring the simulations

    * score_simulations_from_measures calling :
        - check_simulation_mare
        - check_simulation_curvature
        - check_simulation_auto_correlation
"""


def score_simulations_from_measures(raw_measures):
    """
    compute the three scores for each of the targets and the final score with weights = 1
    Careful the dict format for raw_scores is very specific
    :param raw_measures:
    :return:
    """
    raw_scores = {
                   "parameters": raw_measures["params_simulation"],
                   "mare": {"target": raw_measures["params_simulation"]["target_mare"],
                            "observed": raw_measures["mares"]["observed"],
                            "simulated": raw_measures["mares"]["simulated"], "scores_mare": []},
                   "curvature": {"target": raw_measures["second-differences"]["target"],
                                 "observed": raw_measures["second-differences"]["observed"],
                                 "simulated": raw_measures["second-differences"]["simulated"],
                                 "scores": []},
                   "error_auto_correlation": {"target": raw_measures["auto-correlation"]["target"],
                                              "simulated": raw_measures["auto-correlation"]["simulated"],
                                              "scores": [],
                                              },
                   "total_scores": [],
                   }

    raw_scores["mare"]["scores"] = [(m - raw_scores["mare"]["target"])**2 for m in raw_scores["mare"]["simulated"]]
    raw_scores["curvature"]["scores"] = [(d - raw_scores["curvature"]["target"]) ** 2
                                         for d in raw_scores["curvature"]["simulated"]]
    raw_scores["error_auto_correlation"]["scores"] = \
        [sum([(m[i] - raw_scores["error_auto_correlation"]["target"][i]) ** 2 for i in range(5)]) for m in
         raw_scores["error_auto_correlation"]["simulated"]]

    w0, w1, w2 = 1, 1, 1
    for i in range(len(raw_scores["mare"]["scores_mare"])):
        t_mare, t_curvature, t_auto_corr = raw_scores["mare"]["scores_mare"][i], \
                                        raw_scores["curvature"]["scores_curvature"][i], \
                                        raw_scores["error_auto_correlation"]["scores_auto_correlation"][i],
        score = w0 * t_mare + w1 * t_curvature + w2 * t_auto_corr
        raw_scores["total_scores"].append(round(score, 2))

    return raw_scores


def check_simulation_mare(X, Y, results, r_tilde):
    """
    computes the MARE over the sid (observed) and over the simulations in results
    :param X: timeseries of input
    :param Y: timeseries of output
    :param results: results of the simulations
    :param r_tilde: target_mare
    :return:
    """
    x, y = X.loc[results.index], Y.loc[results.index]
    re_hat = (y - x) / x
    re_hat = re_hat[x > 0] ## dlw 
    re_hat = re_hat.dropna() 
    are_hat = re_hat.apply(abs)
    simulation_mares = []
    for c in results.columns:
        print("\n" + "-" * 60)
        print("|" + " " * 20 + c + " " * (38 - len(c)) + "|")
        print("-" * 60)
        simulation = results[c]
        re_tilde = (simulation-x)/x
        re_tilde = re_tilde[x > 0] ## dlw
        re_tilde = re_tilde.dropna()
        are_tilde = re_tilde.apply(abs)
        mare_hat = np.mean(are_hat)
        print("Mape targeted was {}% and estimated over the sid was {}%".format(round(100*float(r_tilde), 2),
                                                                                round(100*float(mare_hat), 2)))
        print("Mape simulated is {}%".format(round(100*float(np.mean(are_tilde)), 2)))
        simulation_mares.append(np.mean(are_tilde))

    title = "Overall mape of the scenario of sets is = {}%, targeted was {}%".format(round(
        100*float(np.mean(simulation_mares)), 2), round(100*float(r_tilde), 2))
    print("\n" + "-" * 100)
    print("|" + " " * 10 + title + " " * (88 - len(title)) + "|")
    print("-" * 100)

    return simulation_mares, np.mean(are_hat)


def check_simulation_curvature(Y, results):
    """
    Computes the curvature (second difference) of the simulations and of the input dataset
    :param Y: timeseries of output
    :param results: results of the simulation
    :return:
    """
    y = Y.loc[results.index]
    observed = (y.diff(1).diff(1).dropna()).values
    d_obs = np.mean(abs(observed))
    d_simuls = []
    for c in results.columns:
        second_diff_simulated = (results[c].diff(1).diff(1).dropna()).values
        d_simul = np.mean(abs(second_diff_simulated))
        d_simuls.append(d_simul)
    return d_simuls, d_obs


def check_simulation_auto_correlation(x, errors_, results, p=5):
    """
    Computes the auto-correlation of the errors of the simulations and of the input dataset for the first p lags
    :param x: timeseries of input
    :param errors_: timeseries of errors
    :param results: timeseries of simulations
    :param p: first lags of auto-correlation to compute
    :return:
    """
    acf_ = acf(errors_)[:p]
    rho_real = [round(a, 2) for a in acf_]
    rho_simuls = []
    for c in results.columns:
        errors_ = (results[c] - x).dropna()
        acf_2 = acf(errors_)[:p]
        rho_simuls.append([round(a, 2) for a in acf_2])
    return rho_simuls, rho_real
