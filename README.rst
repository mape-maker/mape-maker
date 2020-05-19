******
README
******

Introduction
############

Beta release.

This package can be used to create simulations of wind power forecasts from actuals or the other way around
from actuals to forecasts. It has been implemented so that a generalization to any type of dataframe providing
actuals and forecasts, is possible.

Documentation is available at `readthedocs <https://mape-maker.readthedocs.io/en/latest/>`_ and there is a paper on `arXiv. <http://arxiv.org/abs/1909.01919>`

The main inputs of the package are :

* an input dataset giving forecasts and actuals for specified datetimes.
* a simulation input dataset : the start and end-date of the subset of the input dataset
* r_tilde : a desired MAPE (i.e mean absolute percent error see more at `Percent Errors and MAPEs`_ ) for the simulations in output
* user-specified technical parameters

The mape_maker class estimates the conditioned distribution of the errors considering the input values.
It adjusts these distribution to satisfy the specified target MAPE. Having fitted a base process, it simulates
highly auto-correlated errors and finally if the user specifies it, it operates a curvature optimization.
With these three steps, MapeMaker aims at satisfying the plausability criteria. See more at `Plausability criteria`_.

In this regard, the two technical specification to make for each simulation are the following :

* Base Process : IID (generate IDD and so uncorrelated base process), ARMA (default)
* Curvature : boolean (This is usually not needed, so the default is FALSE)


Skeleton of the project
########################

::

    .
    ├── README.rst
    ├── mape_maker
    │   ├── __init__.py
    │   ├── __main__.py
    │   ├── dataset_easy_fix
    │   │   ├── __init__.py
    │   │   └── repair_nan_zeros.py
    │   ├── latex_outputer
    │   │   ├── __init__.py
    │   │   └── to_latex.py
    │   ├── mape_maker.py
    │   ├── results_plots.py
    │   ├── samples
    │   │   ├── 2012-2013_BPA_forecasts_actuals.csv
    │   │   └── wind_total_forecast_actual_070113_063015.csv
    │   └── utilities
    │       ├── ARMA_fit.py
    │       ├── curvature_correction.py
    │       ├── df_utilities.py
    │       ├── fitting_distribution.py
    │       ├── simulation.py
    │       ├── stored_ARTA_coef
    │       │   └── ar_coeffs.json
    │       └── stored_vectors
    │           └── wind_total_forecast_actual_070113_063015_toforecasts_parameters.pkl
    ├── output
    │   └── test.csv
    ├── requirements.txt
    ├── setup.py
    └──  slides
        └── slides_v1.pdf



Setup
########################

You can install the package with the setup.py file:

::

    python setup.py develop


Then you can use the package in command-line, for a quick-first run :

::

    python -m mape_maker "mape_maker/samples/wind_total_forecast_actual_070113_063015.csv"

This is real data from CAISO with negative values that mape_maker treats as zero. The
presence of many low power values makes it difficult to exactly hit a target MAPE.

Options
########################

The options of the package are :

::

    python mape_maker --help
    Options:
      -t, --target_mape FLOAT         desired mape otherwise will take
                                      a MAPE based on the dataset
      -st, --simulated_timeseries TEXT       feature you want to simulate 'actuals' or
                                      'forecasts'
      -bp, --base_process TEXT        base procees either 'iid' or 'ARMA'
      -a, --a FLOAT                   percent of data on the left and the right
                                      for the conditional estimation of beta parameters
      -o, --output_dir TEXT          path to dir to create for csv files
      -n, --number_simulations INTEGER
                                      number of simulations
      -is, --input_start_dt TEXT      start_date for the computation of the
                                  distributions, format='Y-m-d H:M:S '
      -ie, --input_end_dt TEXT        end_date for the computation of the
                                  distributions, format='Y-m-d H:M:S '

      -sd, --simulation_start_dt TEXT          start_date for the simulation,
                                      format='Y-m-d H:M:S '
      -ed, --simulation_end_dt TEXT            end_date for the simulation, format='Y-m-d H:M:S'
      -ti, --title TEXT               title for the plot
      -s, --seed INTEGER              random seed
      -lp, --load_pickle BOOLEAN      load the pickle file for the data file instead of estimation
      -c, --curvature TEXT            curvature
      -tl, --time_limit INTEGER       time limit for curvature optimization
      -ct, --curvature_target FLOAT   the target of the second difference
      -m, --mip_gap FLOAT                 the relative mip gap (for curvature)
      -so, --solver TEXT              solver
      -lo, --latex_output BOOLEAN     write results in latex file
      -sh, --show BOOLEAN             plot simulations
      -v, --verbosity                 verbosity level
      -vo --verbosity_output          the output file to save the verbosity
      --help                          Show this message and exit.


Options availables
**********************

* simulated_timeseries:

    - "actuals" : simulating actuals from forecasts
    - "forecasts" : simulating forecasts from actuals

* base_process :

    - "iid"
    - "ARMA"

* start_date and end_date :

    Format "Y-m-d"

By Default-options
**********************

* **target_mape** : the mape of the current dataset,
* **simulated_timeseries** : "actuals",
* **base_process** : "ARMA",
* **a** : 4
* **output_dir** : None, no output_file will be created,
* **number_simulations** : 1,
* **start_date** : None, will simulate over the whole dataset
* **end_date** : None, will simulate over the whole dataset
* **title** : None, no additionnal title will be added to the plot,
* **seed** : None.
* **load_pickle** : False.
* **curvature** : False.
* **time_limit** : 3600 seconds.
* **curvature_target** : mean of the second difference of the dataset.
* **mip** : 0.3.
* **solver** : gurobi.
* **latex_output** : False, not supported yet.
* **show** : True.
* **verbosity** : 2, which will set the logging level to INFO
* **verbosity_output** : None, the output will be shown on the terminal



Examples
########

The following command will take the data of the CAISO.csv file, will launch n=4 simulations
from actuals to forecasts for a target_mape of 50% using an IID Base Process.
It will simulate from "2014-1-1" to "2014-7-1", and  it will
write a plot file with title "first test" to the file mmFinalFig.png.

::

    python -m mape_maker "mape_maker/samples/wind_total_forecast_actual_070113_063015.csv" -st "actuals" -n 5 -bp "ARMA"

The next example runs a little faster, issues some warnings and creates a directory called `output`. If that directory
already exists, it will issue an error message. The directory will have a csv file with output.

::

    python -m mape_maker "mape_maker/samples/wind_total_forecast_actual_070113_063015.csv" -st "actuals" -n 5 -bp "ARMA" -is "2014-6-1 0:0:0" -ie "2014-6-30 23:0:0" --target_mape 30 --output_dir "output"


Percent Errors and MAPEs
########################

We denote f and a as respectively the timeseries of forecasts and actuals. From there we can define two MAPEs depending on the simulation you wish to accomplish.

Then if you are simulating **forecasts from actuals**,

.. math::
    mape = \frac{100}{n} \sum_{i=1}^n \frac{|f_i - a_i|}{a_i}

If you are simulating **actuals from forecasts**,

.. math::
    mape = \frac{100}{n} \sum_{i=1}^n \frac{|f_i - a_i|}{f_i}


Plausability criteria
#####################

A scenario set is said to be "plausible" if :
    - its distribution of errors is close to the empirical distribution of errors i.e its plausibility score is close to 1.
    - its auto-correlation coefficients are close the empirical values.
    - When the output is forecast scenarios, the second differences are close to the empirical values.


References
##########

[1] "Mape_Maker: A Scenario Creator"
Guillaume Goujard, Jean-Paul Watson, and David L. Woodruff,
 arXiv:1909.01919v1, 2019.


[2] "Fitting Time-Series Input Processes for Simulation", Bahar Biller, Barry L. Nelson, OPERATIONS RESEARCH
Vol. 53, No. 3, May–June 2005, pp. 549–559

Github action badge
###################

https://github.com/mape-maker/mape-maker/workflows/mape-maker/badge.svg
