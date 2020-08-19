from mape_maker.datasets.SID import SID
from mape_maker.datasets.XYID import XYID
from logging import Logger
from scipy.stats import beta
from typing import List, Dict
from scipy.optimize import least_squares
import numpy as np
loading_bar = "-"*70

class SimParams:
    def __init__(self, xyid: XYID, sid: SID, logger: Logger, r_tilde: float = None, base_process: str = None,
                 n: int = 1, full_dataset: bool = False, seed: int = None, list_of_date_ranges: List = None,
                 curvature_parameters: Dict = None, latex: bool = False, show: bool = False, **kwargs):
        """ load all the parameters useful for the simulation

        Args:
            xyid: used to obtain simulation coefficients
            sid: used to obtain simulation coefficients
            logger:
            r_tilde:
            base_process:
            n:
            full_dataset:
            seed:
            list_of_date_ranges:
            curvature_parameters:
            latex:
            show:
            **kwargs:
        """
        self.logger = logger
        self.cap = xyid.dataset_info.get("cap")
        self.curvature_parameters = check_curvature_parameters(curvature_parameters, xyid)
        self.n = n
        self.full_dataset = full_dataset
        self.seed = seed
        self.latex = latex
        self.floored = True
        self.desired_base_process: str = base_process
        self.show = show

        self.r_tilde = r_tilde
        if self.r_tilde is None:
            self.r_tilde = xyid.dataset_info.get("r_m_hat")

        self.base_process = xyid.arma_process
        self.cfx = None
        self.om_tilde, self.e_score = None, np.inf
        self.r_tilde_max = 0
        self.s_x_tilde, nb_errors = None, None
        self.m_tilde = None
        self.m_max = None
        self.adjust_distributions(xyid, sid)  #: populates all the instances above

    def adjust_distributions(self, xyid, sid):
        """
        creates the simulation weight function, the simulation beta coefficients, check the feasibility of the
        simulation mare
        Args:
            xyid:
            sid:

        Returns:

        """
        self.cfx = self.construct_cfx(xyid.dataset_x, sid.dataset_x)
        self.logger.info(loading_bar + "\nDetermination of the weight function om_tilde")
        self.om_tilde, self.e_score = self.create_sid_weight_function(xyid.om, xyid.dataset_x, sid.dataset_x)
        self.logger.info(loading_bar + "\nDetermination of the maximum of mare attainable")
        self.m_max, self.r_tilde_max = self.infer_r_tilde_max(xyid.m_max, sid.dataset_x)
        self.check_feasibility()
        self.logger.info(loading_bar + "\nDetermination of the target function m_tilde")
        self.get_maes_from_weight_target(sid.dataset_x)
        self.logger.info(loading_bar + "\nComputation of the new simulation parameters")
        self.s_x_tilde, nb_errors = self.get_s_tilde_sid(sid.dataset_x, xyid.s_x, xyid.m)

    def check_feasibility(self):
        if abs(self.e_score - 1) < 0.1:
            s = " == 1, the dataset_SID is balanced like dataset_X"
        elif self.e_score > 1:
            s = " > 1, there is a prevalence of low power input in the SID"
        else:
            s = " < 1, there is a prevalence of high power input in the SID"
            if self.r_tilde > self.r_tilde_max:
                s += "\nThe requested r_tilde is too high"
                s += "\n     => Either change your requested mape to be less than {}".format(self.r_tilde_max * 100)
                s += "\n     => Or change your SID so the e_score increases"
                raise RuntimeError(s)
        inequality = " <= " if self.r_tilde > self.r_tilde_max else " > "
        s += "\nMaximum of mare attainable with this score is {}".format("%.2f" % self.r_tilde_max) + \
                   inequality + "target {}".format("%.2f" % self.r_tilde)
        self.logger.info("Plausibility score = {} ".format('%.3f' % self.e_score) + s)

    def create_sid_weight_function(self, om_x, dataset_x, dataset_sid):
        """create the weight function for the sid from the weight function of the xyid and the distribution of the sid

        Args:
            om_x:
            dataset_sid:

        Returns:

        """
        # see if the x are very different tbd improve this
        min_x, max_x = dataset_x[[0,-1]]
        min_sid, max_sid = dataset_sid[[0,-1]]
        if min_sid > max_x or max_sid < min_x:
            raise RuntimeError("x values in SID completely outside fitting x values")
        e = 0
        length_of_non_zeros = 0
        for x in dataset_sid:
            if x != 0:
                length_of_non_zeros += 1
                e += om_x[self.cfx[x]]
        if length_of_non_zeros == 0:
            raise RuntimeError("No non-zeros in simulation X (maybe bad dates?)")
        e = e / length_of_non_zeros
        om_sid = {}
        for x in dataset_sid:
            if x != 0:
                om_sid[x] = om_x[self.cfx[x]] / e
            else:
                om_sid[x] = 0
        return om_sid, e

    def construct_cfx(self, dataset_x, dataset_sid):
        """ Outputs a dictionary of Closest fitting x (maybe the x comes from SID, maybe fitting)
        """
        self.cfx = {}
        for x in dataset_sid:
            if x in dataset_x:
                self.cfx[x] = x
            else:
                i = np.argmin(abs(dataset_x - x))
                self.cfx[x] = dataset_x[i]
        return self.cfx

    def get_maes_from_weight_target(self, dataset_sid):
        """
        Infer the mae to get from each conditional distribution for the simulation
        """
        self.m_tilde = {}
        # self.bound_list = []
        nb_bound_exceptions = 0
        for x in dataset_sid:
            self.m_tilde[x] = self.r_tilde * x * self.om_tilde[x]
            if self.m_tilde[x] > self.m_max[self.cfx[x]]:
                # self.bound_list.append(x)
                nb_bound_exceptions += 1
                if nb_bound_exceptions < 10:
                    self.logger.info("Anticipating bound exception...  \n" + " " * 5 + "- MAE targeted {},\n".format(
                        "%.2f" % self.m_tilde[x]) +
                                " " * 5 + "- MAE max obtainable {}".format("%.2f" % self.m_max[x]))
                self.m_tilde[x] = self.m_max[self.cfx[x]]
        if nb_bound_exceptions == 0:
            self.logger.info("There were no bound exceptions anticipated")
        else:
            self.logger.info("There were {} ({}%) bound exceptions anticipated,".\
                             format(nb_bound_exceptions, round(100*float(nb_bound_exceptions/len(dataset_sid)), 2)))
            self.logger.info("so the scenario MAPEs might be a little lower than requested.")

    def infer_r_tilde_max(self, m_max, dataset_sid):
        max_r_tilde_list = []
        index_parameters = np.array(list(m_max.keys()))
        for x in dataset_sid:
            if x != 0:
                if x not in m_max:
                    i = np.argmin(abs(index_parameters - x))
                    m_max[x] = m_max[index_parameters[i]]
                max_r_tilde_list.append(m_max[self.cfx[x]] / (x * self.om_tilde[x]))
        return m_max, min(max_r_tilde_list)

    def get_s_tilde_sid(self, dataset_sid, s_x, m_hat):
        """
        Get the correct parameters for the simulation functions

        Args:
            dataset_sid:
            s_x:
            m_hat:

        Returns:

        """
        s_x_sid = dict([(key, []) for key in dataset_sid])
        _, _, l, s = s_x[list(s_x.keys())[0]]
        p = len(dataset_sid) // 8
        nb_errors = 0
        for j, x in enumerate(dataset_sid):
            a, b, loc_nx, scale_nx = s_x[self.cfx[x]]
            try:
                loc_nx = -x if loc_nx < -x else loc_nx
                scale_nx = self.cap if scale_nx > self.cap else scale_nx
                oh = max(abs(loc_nx), abs(scale_nx), self.m_tilde[x])
                # NOTE: the upper bound for s should be cap - x - l
                nl, ns = least_squares(find_intersections,
                                       x0=(loc_nx, scale_nx),
                                       bounds=([-x, 0], [loc_nx, self.cap]),
                                       args=(self.m_tilde[x], a, b, loc_nx, scale_nx, oh, False),
                                       ftol=1e-3, method="dogbox").x
                if ns == 0:
                    ns = scale_nx
                if j % p == 0:
                    self.logger.info("     - l_hat and s_hat = {}, {} for m_hat(x) = {} => l_tilde and s_tilde = {}, {} "
                                "for m_tilde = {} < m_max = {}: {}% done".format("%.1f" % loc_nx, "%.1f" % scale_nx,
                                                                                 "%.1f" % m_hat[x],
                                                                                 "%.1f" % nl, "%.1f" % ns,
                                                                                 "%.1f" % self.m_tilde[x], "%.1f" % self.m_max[x],
                                                                                 (round(100 * j / len(dataset_sid[:-1]),
                                                                                        3))))
            except Exception as e:
                if x != 0 and x != self.cap:  # bounds are equal for these cases
                    nb_errors += 1
                    if self.m_tilde[x] > self.m_max[self.cfx[x]]:
                        self.logger.error(
                            "     * The MAE target {} is greater than the maximum target {}".format(round(self.m_tilde[x]),
                                                                                                    round(self.m_max[self.cfx[x]])))
                    self.logger.error(" * For x = {}, infeasible to meet the target exactly".format(x))
                    self.logger.error(" {}".format(e))
                nl, ns = loc_nx, scale_nx
            s_x_sid[x] = [a, b, nl, ns]
        return s_x_sid, nb_errors


def integrate_a_mean_2d(l_, x_, a=0, b=0, verbose=False):
    if verbose:
        print(l_, x_)
    test = beta.rvs(a, b, loc=l_, scale=x_, size=4000, random_state=1234)
    beta_mare = np.mean(abs(test))
    return beta_mare


def find_intersections(x, target=0, a=0, b=0, l_hat=0, s_hat=0, oh=0, verbose=False):
    # x is a list, x[0] is l and x[1] is s
    # this is not exactly what is in the paper
    sqarg = integrate_a_mean_2d(x[0], x[1], a=a, b=b, verbose=verbose) - target \
            + abs((x[0] - l_hat) / oh) + abs((x[1] - s_hat) / oh)
    return [sqarg, 0]

def check_curvature_parameters(curvature_parameters, xyid):
    if curvature_parameters is not None:
        if curvature_parameters.get("MIP") is None:
            curvature_parameters["MIP"] = 0.3
        if curvature_parameters.get("time_limit") is None:
            curvature_parameters["time_limit"] = 3600
        if curvature_parameters.get("curvature_target") is None:
            curvature_parameters["curvature_target"] = xyid.dataset_info.get("second_differences")
        if curvature_parameters.get("solver") is None:
            curvature_parameters["solver"] = "gurobi"
    return curvature_parameters