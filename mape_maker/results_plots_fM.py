from MapeMaker import MapeMaker
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

if __name__ == "__main__" :
    # CAISO DATASET + SEED = 1
    CAISO_path = "samples/wind_total_forecast_actual_070113_063015.csv"
    mare_embedder = MapeMaker(path=CAISO_path, ending_feature="forecasts",
                              load_pickle=False, seed=1)
    curvature_parameters = {
        "MIP": 0.05,
        "time_limit": 120,
        "smoothness_target": None,
        "solver": "cplex",
    }
    # first select M
    M = 20
    # Then we compute the results, the metrics are stored in mare_embedder.saved_scores
    mare_embedder.simulate(target_mare=2,
                               full_dataset = True,
                                base_process="iid",
                                curvature_parameters=None,
                                n=M),
    mare_embedder.simulate(target_mare=2,
                               full_dataset=True,
                               base_process="ARMA",
                               curvature_parameters=None,
                               n=M),
    mare_embedder.simulate(target_mare=2,
                               full_dataset=True,
                               base_process="ARMA",
                               curvature_parameters=curvature_parameters,
                               n=M)

    #Use this function with the metric you want
    def plot_results_in_f_M(results, M, metric="mare"):
        """

        :param results:
        :param metric: choose between "mare", "", ""
        :return:
        """
        Ms = [i for i in range(1, M+1)]
        fig, ax1 = plt.subplots(figsize=(9, 6), dpi=80, facecolor='w', edgecolor='k')
        color = 'black'

        ax1.set_xlabel('Number of Simulations')
        ax1.set_ylabel(metric, color=color) 
        for k in results:
            simulated_metrics = results[k][metric]["simulated"]
            if metric == "error_auto_correlation":
                simulated_metrics = sum(abs(np.array(results[k][metric]["simulated"])-
                                            np.array(results[k][metric]["target"]))) # Watch out for this one !
            moving_mean = [np.mean(simulated_metrics[:i]) for i in Ms]
            plt.plot(Ms, moving_mean, marker="x", linestyle="dashed", label="{}".format(metric + " " + k))
        target = 0 if metric == "error_auto_correlation" else results[k][metric]["target"]
        plt.plot(Ms, [target] * len(Ms), label="target {}".format(metric))
        plt.legend()
        plt.title("Convergence of the simulations {} ({} simulations)".format(metric, M))
        plt.grid(True)
        fname = metric+".png"
        plt.savefig(fname)
        print ("plot saved to", fname)

        #plt.show()


    plot_results_in_f_M(mare_embedder.saved_scores, M, metric="mare")
    plot_results_in_f_M(mare_embedder.saved_scores, M, metric="curvature")
    plot_results_in_f_M(mare_embedder.saved_scores, M, metric="error_auto_correlation")
