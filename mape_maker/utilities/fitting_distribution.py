from scipy.stats import norm
import warnings
import numpy as np
from scipy.optimize import fsolve, least_squares
from scipy.stats import beta
from scipy import optimize
import pandas as pd
import scipy as scp
warnings.filterwarnings('ignore', 'The iteration is not making good progress')
TypeDistrib = type(scp.stats.norm)
TypeFunction = type(lambda x: 0)

"""
Main functions for estimating the parameters of the conditional distribution:
    * get_s_hat_datasetx_b calling find_parameters calling find_alpha_beta
    * get_s_x looping over the element of the datasetx to get the closest parameters
"""


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


def find_parameters(x_, x_timeseries, datasetx, errors, cap=4500, a=1):
    """
    For a given x_, find the sample with a% on the right and a% on the left, set its bounds (l and s) and
    find the shape parameters with the method of moment
    :param x_: real around which to take the sample
    :param datasetx:
    :param errors:
    :param cap:
    :param a:
    :return: x_bar, parameters of the beta conditionned by x_bar and mean - variane of the sample
    """
    index_x = np.argwhere(np.array(datasetx) >= x_)[0][0]
    dx = int((a/100)*len(datasetx))
    left_bound = index_x-dx if index_x-dx > 0 else 0
    right_bound = index_x+dx if index_x+dx < len(datasetx) else len(datasetx)-1
    interval = [datasetx[left_bound], datasetx[right_bound]]
    x_bar = np.mean(x_timeseries[(x_timeseries > interval[0]) & (x_timeseries < interval[1])])
    sub_delta = errors[(x_timeseries > interval[0]) & (x_timeseries < interval[1])]
    mean, var = np.mean(sub_delta), np.std(sub_delta) ** 2
    abs_lower = - x_bar
    abs_upper = cap - x_bar
    if min(sub_delta) < abs_lower:
        lower = abs_lower
    else:
        lower = min(sub_delta)
    if max(sub_delta) > abs_upper:
        upper = cap - x_bar - lower
    else:
        upper = max(sub_delta) - lower
    a, b = fsolve(find_alpha_beta, (1, 1), args=(lower, upper, mean, var))
    return x_bar, [a, b, lower, upper], [mean, var]


def get_s_hat_datasetx_a(x_timeseries, datasetx, errors, cap, logger, a=4, return_sequence=False):
    """
    loop over a grid of uniformally distributed real between 0 and cap and return S_hat_dataset_a
    :param datasetx:
    :param errors: vector of errors
    :param cap: max of the capacity
    :param a: percent/2 of data for the sample
    :param return_sequence: if True will return x_bar(x,a)
    :return: s_hat_dataset_a
    """
    len_s_hat = 2000
    index_search = np.linspace(0, cap, len_s_hat)
    parameters = [[0] * 4] * len_s_hat
    other_stuffs = [[0]*2] * len_s_hat
    index_plot = []
    x_bar = [0]*len_s_hat
    for k, x_ in enumerate(index_search):
        if x_ == index_search[-1]:
            a = 1
        new_x, parameters[k], other_stuffs[k] = find_parameters(x_, x_timeseries, datasetx, errors, cap=cap, a=a)
        x_bar[int(k)] = new_x
        index_plot.append(new_x)
        if k % 50 == 0:
            logger.info("{}% of the dataset fit".format(round(100*k/len_s_hat, 2)))
    if return_sequence:
        return index_search, x_bar
    return dict([(index_plot[i], parameters[i]) for i in range(len(index_plot))])


def get_s_x(parameters, datasetx, logger):
    """
    For all x in datasetx find the closest parameters in the dic parameters
    :param parameters:
    :param datasetx:
    :return: s_x
    """
    index_parameters = np.array(list(parameters.keys()))
    test_parameters = dict([(key, []) for key in datasetx])
    _, _, l, s = parameters[index_parameters[0]]
    p = len(datasetx) // 8
    for j, x in enumerate(datasetx):
        i = np.argmin(abs(index_parameters - x))
        nx = index_parameters[i]
        test_parameters[x] = parameters[nx]
        if j % p == 0:
            logger.info("     - Closest xbar for x = {} is {},  {}% done"
                        .format("%.3f" % x, "%.3f" % nx, (round(100 * j / len(datasetx[:-1]), 3))))
    return test_parameters


"""
Main functions :
    * make_datasetx
    
For estimating the weight, target function :
    * create_weight_function
    * get_maes_from_parameters
    * get_r_from_m_hat
    
For creating the weight, target function for the sid :
    * create_sid_weight_function
    *get_maes_from_weight_target
    
"""


def make_datasetx(x):
    """
    returns the list of sorted values of the input dataset and
    :param x: input dataset timeseries format
    :return: datasetX
    """
    datasetx = list(set(x))
    datasetx.sort()
    return datasetx


def get_maes_from_parameters(s_x, cap, logger):
    """
    Get the Mean absolute error of each distribution with parameters in s_x
    :param s_x:
    :return: m_hat, m_max
    """
    lastgood = None # deal with failure to get good beta parameters
    m_hat, m_max = {}, {}
    p = len(list(s_x.keys())) // 16
    for i, x in enumerate(s_x.keys()):
        a, b, l_, s_ = s_x[x]
        try:
            sample = beta.rvs(a, b, loc=l_, scale=s_, size=4000, random_state=1234)
        except:
            logger.warning ("******* WARNING!! **********")
            logger.warning (" beta rvs failed at i={},x={}; a={}, b={}, l_={}, s_={}".format(i,x,a,b,l_,s_))
            if lastgood is None:
                raise
            else:
                logger.warning (" Using last good beta parameters.")
                a, b, l_, s_ = lastgood
                sample = beta.rvs(a, b, loc=l_, scale=s_, size=4000, random_state=1234)
        lastgood = (a, b, l_, s_)
        opt = optimize.minimize(integrate_a_mean_1d, x0=(l_, s_), bounds=((-x, 0), (0, cap-x)), args=(a, b),
                                tol=1e-1)
        m_max[x] = max(-opt.fun, ((cap-x)*a)/(a+b))
        stored_l, stored_s = opt.x
        if i % p == 0:
            logger.info(" {}% of the m_max computed".format("%.1f" % (100 * i / len(list(s_x.keys())))))
            logger.info(" - for input {}, m_max = {} for l {} and s {}".format("%.3f" % x, "%.3f" % m_max[x],
                                                                          "%.3f" % stored_l, "%.3f" % stored_s))
        m_hat[x] = np.mean(abs(sample))
    return m_hat, m_max


def get_r_from_m_hat(m_hat):
    """
    Get the theorical mare from an error simulated with the estimated distributions
    :param m_hat:
    :return: r_m_hat
    """
    r_m_hat = 0
    for x in m_hat.keys():
        if x != 0:
            r_m_hat += m_hat[x]/x
    r_m_hat = r_m_hat/len(m_hat.keys())
    return r_m_hat


def create_weight_function(m, r_m):
    """
    Create the weight function from the maes and the estimated r
    :param m:
    :param r_m:
    :return: om_x
    """
    om_x = {}
    for x in m.keys():
        if x != 0:
            om_x[x] = m[x]/(r_m*x)
    return om_x


def create_sid_weight_function(om_x, x_sid, logger):
    """
    Create the weight function for the sid from the distribution of the sid and the estimated weight function
    :param om_x: omega for the fitting data
    :param x_sid:
    :return: om_x_sid
    """
    # see if the x are very different tbd improve this
    index_parameters = np.array(list(om_x.keys()))
    max_x = np.max(index_parameters)
    min_x = np.min(index_parameters)
    min_sid = min(x_sid)
    max_sid = max(x_sid)
    if min_sid > max_x or max_sid < min_x:
        raise RuntimeError("x values in SID completely outside fitting x values")
    e = 0
    length_of_non_zeros = 0
    fitting_x = {}
    for x in x_sid:
        if x != 0:
            length_of_non_zeros += 1
            if x not in om_x:
                i = np.argmin(abs(index_parameters - x))
                fitting_x[x] = index_parameters[i]
            else:
                fitting_x[x] = x
            e += om_x[fitting_x[x]]
    if length_of_non_zeros == 0:
        raise RuntimeError("No non-zeros in simulation X (maybe bad dates?)")
    e = e/length_of_non_zeros
    om_sid = {}
    for x in x_sid:
        if x != 0:
            om_sid[x] = om_x[fitting_x[x]] / e
        else:
            om_sid[x] = 0
    return om_sid, e

"""
Main functions for getting the simulation parameters of the conditional distribution:
    * get_s_tilde_sid calling find_intersections calling integrate_a_mean_2d 
"""


def integrate_a_mean_2d(l_, x_,  a=0, b=0, verbose=False):
    if verbose:
        print(l_, x_)
    test = beta.rvs(a, b, loc=l_, scale=x_, size=4000, random_state=1234)
    beta_mare = np.mean(abs(test))
    return beta_mare


def integrate_a_mean_1d(x, a=0, b=0, verbose=False):
    l_, x_ = x
    return -integrate_a_mean_2d(l_, x_, a=a, b=b, verbose=verbose)


def find_intersections(x, target=0, a=0, b=0, l_hat=0, s_hat=0, oh=0, verbose=False):
    # x is a list, x[0] is l and x[1] is s
    # this is not exactly what is in the paper
    sqarg = integrate_a_mean_2d(x[0], x[1], a=a, b=b, verbose=verbose) - target \
            + abs((x[0] - l_hat)/oh) + abs((x[1] - s_hat)/oh)
    return [sqarg, 0]


def get_s_tilde_sid(s_x, m_tilde, m_hat, m_max, cap, logger):
    """
    Get the correct parameters for the simulation functions
    :param s_x:
    :param m_tilde:
    :param m_hat:
    :param cap:
    :return: s_tilde_sid
    note: l_hat is loc_nx, s_hat is scale_nx
    """
    datasetsid = list(m_tilde.keys())
    index_parameters = np.array(list(s_x.keys()))
    s_x_sid = dict([(key, []) for key in datasetsid])
    _, _, l, s = s_x[index_parameters[0]]
    p = len(datasetsid)//8
    nb_errors = 0
    for j, x in enumerate(datasetsid):
        i = np.argmin(abs(index_parameters-x))
        nx = index_parameters[i]
        a, b, loc_nx, scale_nx = s_x[nx]
        try:
            loc_nx = -x if loc_nx < -x else loc_nx
            scale_nx = cap - x if scale_nx > cap - x else scale_nx
            oh = max(abs(loc_nx), abs(scale_nx), m_tilde[x])
            # bounds are ([lower, lower], [upper,upper])
            # NOTE: the upper bound for s should be cap - x - l
            nl, ns = least_squares(find_intersections,
                                   x0=(min(loc_nx+5,-x/2), scale_nx),
                                   bounds=([-x, 0], [0, cap-x]),
                                   # args=(m_tilde[x], a, b, loc_nx, scale_nx, oh, False),
                                   args=(m_tilde[x], a, b, loc_nx, scale_nx, oh, False),
                                   ftol=1e-3, method="dogbox").x
            if ns == 0:
                print("ns == 0 set by least square")
                print("a, b, nl, ns:", a, b, nl, ns)
                print("    loc_nx, scale_nx", loc_nx, scale_nx)
                print("         sid x, fitting nx", x, nx)
                print("             m_tilde[x]", m_tilde[x])
                print("HORRIBLE HACK!!!!!")
                ns = scale_nx
            if j % p == 0:
                logger.info("     - l_hat and s_hat = {}, {} for m_hat(x) = {} => l_tilde and s_tilde = {}, {} "
                      "for m_tilde = {} < m_max = {}: {}% done".format("%.1f" % loc_nx, "%.1f" % scale_nx, "%.1f" % m_hat[x],
                                                  "%.1f" % nl, "%.1f" % ns, "%.1f" % m_tilde[x], "%.1f" % m_max[x],
                                                                       (round(100*j / len(datasetsid[:-1]), 3))))
        except Exception as e:
            if x != 0 and x != cap:  # bounds are equal for these cases
                nb_errors += 1
                if m_tilde[x] > m_max[x]:
                    logger.error("     * The MAE target {} is greater than the maximum target {}".format(round(m_tilde[x]),
                                                                                             round(m_max[x])))
                logger.error(" * For x = {}, infeasible to meet the target exactly.".format(x))
                logger.error(" {}".format(e))
            nl, ns = loc_nx, scale_nx
        s_x_sid[x] = [a, b, nl, ns]
    return s_x_sid, nb_errors
