import pyomo.environ as pyo
import pandas as pd

"""
Main functions for optimizing curvature :

    * second_curvature_rule, equality, create_lambda_constraints : contraints for pyomo model
    * model_first_second_dif : function to create model
    * solve : function to optimize the second differences
"""

# defining contraints and objective


def second_curvature_rule(model, i):
    return model.lambda_p[i] - model.lambda_m[i] == model.y[i] - 2*model.y[i-1] + model.y[i-2]


def equality(model, i):
    return model.z[i] == model.lambda_p[i] + model.lambda_m[i]


def create_lambda_constraints(cap):
    d_max = 4 * cap

    def lambda_m(model, i):
        return model.lambda_m[i] <= model.b[i]*d_max

    def lambda_p(model, i):
        return model.lambda_p[i] <= (1-model.b[i])*d_max

    return lambda_m, lambda_p

# defining the model


def model_first_second_dif(name, d2, x, delta, cap=4000):
    """
    create model with constraints and objective
    :param name: name of the model
    :param d2: second difference target
    :param x: time series of input data
    :param delta: errors vector
    :param cap: max capacity
    :return: pyomo model
    """
    print("Building model... ")
    for df in [x, delta]:
        if len(df[df.isna()]) > 0:
            print("na in {}".format(df.columns))
            print(df[df.isna()])
    w1, w2 = 1, 1
    model = pyo.ConcreteModel(name=name)
    model.index = range(len(x))
    model.y = pyo.Var(model.index, within=pyo.NonNegativeReals)
    model.z = pyo.Var(model.index)
    model.lambda_p = pyo.Var(model.index, within=pyo.NonNegativeReals)
    model.lambda_m = pyo.Var(model.index, within=pyo.NonNegativeReals)
    model.b = pyo.Var(model.index, within=pyo.Binary)

    lambda_m, lambda_p = create_lambda_constraints(cap)
    model.equality_constraint = pyo.Constraint(model.index, rule=equality)
    model.secondsmoothness_constraint = pyo.Constraint(model.index[2:], rule=second_curvature_rule)
    model.lambdam_constraint = pyo.Constraint(model.index, rule=lambda_m)
    model.lambdap_constraint = pyo.Constraint(model.index, rule=lambda_p)

    def obj_func(model_):
        sum_ = 0
        for date in model_.index[2:]:
            sum_ += w1 * (model_.y[date] - x[date] - delta[date]) ** 2 + w2 * (
                        model_.z[date] - d2) ** 2
        return sum_

    model.obj = pyo.Objective(rule=obj_func)

    return model


def solve(model, index, solver="gurobi", time_limit="15", mip_gap=0.05, show=False):
    """

    :param model: pyomo model
    :param index: datetime index
    :param solver: type of solver (default = gurobi)
    :param time_limit: time limit to stop the solver (default =15)
    :param mip_gap: mip gap (default 5%)
    :param show: pprint
    :return:
    """
    name_simul = "Adding Smoothness"
    print("\n" + "_" * 40)
    print("|" + " " * 10 + name_simul + " " * (28 - len(name_simul)) + "|")
    print("-" * 40)
    solver = pyo.SolverFactory(solver)
    solver.options['TimeLimit'] = time_limit
    solver.options['mipgap'] = mip_gap
    solver.solve(model, tee=True)
    if show:
        model.pprint()

    # Results
    results = [pyo.value(model.y[i]) for i in model.index]
    smoothened_result = pd.DataFrame(index=index,
                                     columns=["smooth_simulation"],
                                     data=results)
    return pd.Series(smoothened_result["smooth_simulation"])
