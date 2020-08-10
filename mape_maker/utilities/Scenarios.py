from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt
from logging import Logger
import numpy as np
import os
register_matplotlib_converters()
loading_bar = "-"*70


class Scenarios:
    """
    An embedded class that compute mare, save simulations, and plot simulations
    """
    def __init__(self, logger: Logger, X, Y, results=None, target_mare=None, f_mare=None, plot_start_date=0, output_dir: str = None, plot: bool = True,
                 title: str = "", x_legend: str = "", ending_feature: str = ""):
        """

                Args:
                    :param logger: logger
                    :param X: timeseries of the independent data
                    :param Y: timeseries of the dependent data
                    :param results: simulations
                    :param target_mare: target mare
                    :param f_mare: fitted mare
                    :param plot_start_date: start date of the plot
                    :param output_dir: directory to store output
                    :param plot: True if plot the simulations
                    :param title: plot title
                    :param x_legend: x legend
                    :param ending_features: ending features

        """
        self.X = X
        self.Y = Y
        self.scenarios = results
        self.target_mare = target_mare
        self.f_mare = f_mare
        self.plot_start_date = plot_start_date
        self.output_dir = output_dir
        self.title = title
        self.x_legend = x_legend
        self.ending_feature = ending_feature
        self.logger = logger

        if results is not None:
            self.scenario = []
            self.sim_mares = []
            self.logger.info(loading_bar + "\nComputation of mare for scenarios")
            for r in range(len(results.columns)):
                result = results.iloc[:, r]
                self.scenario.append(Scenario(X, Y, result, target_mare, logger))
                if self.scenario[r].s_tilde is not None:
                    s_mape = round(100*float(self.scenario[r].s_tilde), 2)
                    self.logger.info("scenario {} has target mape {}% and simulated mape {}%". \
                                     format(r+1, round(100*float(target_mare), 2), s_mape))
                    self.sim_mares.append(self.scenario[r].s_tilde)
                else:
                    self.logger.error("fail to find simulated mape for scenario {}".format(r))
            if self.sim_mares is not None:
                s_mape = round(100*float(np.mean(self.sim_mares)), 2)
                self.logger.info("scenarios have target mape {}% and overall mape {}%".\
                                 format(round(100*float(target_mare), 2), s_mape))
            else:
                self.logger.error("fail to find overall mape")
            r_tilde = calc_mare(X, Y) if Y is not None else None
            if r_tilde is not None:
                self.logger.info("observed mape of the input data is {}%".format(round(100*float(r_tilde), 2)))
            else:
                self.logger.info("no observed mape of the input data")
            if f_mare is not None:
                self.logger.info("fitted mape of the inut data is {}%".format(round(100*float(f_mare), 2)))
            else:
                self.logger.info("no fitted mape of the input data")
        if output_dir is not None:
            self.save_output()

        if plot:
            self.plot_results()

    def save_output(self):
        """
        save output as files to directory
        """
        try:
            os.mkdir(self.output_dir)
        except FileExistsError:
            raise RuntimeError("Directory {} already exists".format(self.output_dir))
        tg = "{}".format('%.1f' % (100 * self.target_mare))
        name = "simulations of target mape {}".format(tg)
        basename = name.replace(',', '-')
        basename = basename.replace(':', '-')
        basename = basename.replace(' ', '_')
        outfile = self.output_dir + os.sep + basename + ".csv"
        if outfile is not None:
            self.logger.info(loading_bar + "\nStoring the output for {} in {}".format(name, outfile))
            self.scenarios.to_csv(outfile)

    def plot_results(self):
        """
        plot forecasts, actuals, and simulations
        """
        datetime = list(self.scenarios.keys())[0]
        index = self.scenarios[datetime].iloc[self.plot_start_date * 40:(self.plot_start_date + 1) * 40].index

        fig, ax1 = plt.subplots(figsize=(15, 6), dpi=80, facecolor='w', edgecolor='k',
                                num="MapeMaker - Plot of simulations from {} to {}".format(
                                    index[0].strftime("%Y-%m-%d"),
                                    index[-1].strftime("%Y-%m-%d")))
        color = 'black'
        ax1.set_xlabel('datetime')
        ax1.set_ylabel('Power', color=color)
        if self.Y is not None:
            try:
                ax1.plot(index, self.Y.loc[index].values, '--', marker=".", color="blue", label=self.ending_feature)
            except Exception as e:
                self.logger.error(e)
                self.logger.error("**** Y Plot failed ****")
                self.logger.error("dumping data: {}".format(self.Y.loc[index]))
                self.logger.error("end dump")
        try:
            ax1.plot(index, self.X.loc[index].values, "-", marker="o", color="black",
                     label=self.x_legend, linewidth=0.5)
        except Exception as e:
            self.logger.error(e)
            self.logger.error("********* Plot failed for", self.x_legend)
            self.logger.error("dumping data: {}".format(self.X.loc[index]))
            self.logger.error("end dump")
        if self.scenarios is not None:
            for r in range(len(self.scenarios.columns)):
                simulation = self.scenarios.iloc[:, r]
                try:
                    ax1.plot(index, simulation.loc[index].values, marker=".",
                             linewidth=0.5) # label="simulation {}".format(r+1)
                except Exception as e:
                    self.logger.error(e)
                    self.logger.error("******* Plot failed for simulation {}".format(r+1))
        ax1.legend()
        if self.title is None:
            self.title = "MapeMaker - Plot of simulations from {} to {}, Target Mape {}%".format(
                index[0].strftime("%Y-%m-%d"),
                index[-1].strftime("%Y-%m-%d"), '%.1f' % (100 * self.target_mare))
        name = "{}\nForecasts, actuals and simulation of {}".format(self.title, self.ending_feature)
        plt.title(name)
        plt.savefig("mmFinalFig.png")
        self.logger.info("Plot saved to mmFinalFig.png")


class Scenario:

    def __init__(self, X, Y, result, target_mare, logger):
        """

        Args:
            :param X: timeseries of the independent data
            :param Y: timeseries of the dependent data
            :param result: simulations
            :param target_mare:
            :param logger:

        """
        self.scenario = result
        self.t_tilde = target_mare
        self.r_tilde = calc_mare(X, Y) if Y is not None else None
        self.s_tilde = calc_mare(X, result) if result is not None else None
        self.logger = logger


def calc_mare(x, y):
    r_tilde = (y - x) / x
    r_tilde = r_tilde[x > 0]
    r_tilde = r_tilde.dropna()
    are_hat = r_tilde.apply(abs)
    mare_hat = np.mean(are_hat)
    return mare_hat
