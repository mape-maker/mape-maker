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


Setup
########################

You can install the package with the setup.py file:

::

    python setup.py develop


Then you can use the package in command-line, for a quick-first run :

::

    python -m mape_maker -xf "mape_maker/samples/wind_total_forecast_actual_070113_063015.csv"

This is real data from CAISO with negative values that mape_maker treats as zero. The
presence of many low power values makes it difficult to exactly hit a target MAPE.

Options
########################

The options of the package are :

::

    python mape_maker --help
    Options:
      -sf, --input_sid_file TEXT        path to a simulation input dataset with one or two timeseries (e.g. actuals),
                                        from which scenarios for the other timeseries are generated (e.g. forecasts)
      -o, --output_dir TEXT             path to destination dir where the scenario csv file(s) are saved
      -vo, --verbosity_output TEXT      the name of the verbosity output file
      -is, --input_start_dt TEXT        start date for the estimation of the distributions, format = 'Y-m-d H:M:S'
      -ie, --input_end_dt TEXT          end date for the estimation of the distributions, format = 'Y-m-d H:M:S'

      -ss, --simulation_start_dt TEXT   start date for the simulation of scenarios, format='Y-m-d H:M:S'
      -se, --simulation_end_dt TEXT     end date for the simulation of scenarios, format='Y-m-d H:M:S'
      -t, --target_mape FLOAT           desired mape, otherwise will take the mape based on the input dataset
      -a, --a FLOAT                     percent of data on the left and/or on the right for the estimation
                                        of conditional beta distribution parameter
      -ct, --curvature_target FLOAT     the target of the second difference for curvature optimization
      -m, --mip_gap FLOAT               mip gap for curvature optimization
      -bp, --base_process TEXT          base process - 'iid' or 'ARMA'
      -n, --number_simulations INTEGER  number_simulations
      -tl, --time_limit INTEGER         time limit for curvature optimization
      -ps, --plot_start_date INTEGER    start date for plot(if 0, the start date is the first date of the simulations)
      -s, --seed INTEGER                seed for the pseudo-random seed
      -v, --verbosity INTEGER           verbosity level
      -f, --sid_feature TEXT            feature you want to simulate - 'actuals' or 'forecasts'
      -lp, --load_pickle BOOLEAN        load the pickle file for the dataset instead of estimation
      -c, --curvature BOOLEAN           optimize the curvature for the simulated scenarios
      -p, --plot BOOLEAN                plot scenarios
      -sv, --solver TEXT                name of the solver (e.g. "gurobi")
      -tt, --title TEXT                 title for the plot
      -xl, --x_legend TEXT              legend for x in plot
      --help                            show this message and exit.


Options availables
**********************

* sid_feature:

    - "actuals" : simulating actuals from forecasts
    - "forecasts" : simulating forecasts from actuals

* base_process :

    - "iid"
    - "ARMA"

* start_date and end_date :

    Format "Y-m-d"

By Default-options
**********************

* **input_sid_file**        : None, will take the input dataset as sid
* **output_dir**            : None, no output_file will be created while a plot will be outputted
* **verbosity_output**      : None, no verbosity_output will be created while a plot will be outputted
* **input_start_dt**        : None, will use the whole dataset for the computation of the distributions
* **input_end_dt**          : None, will use the whole dataset for the computation of the distributions
* **simulation_start_dt**   : None, will simulate over the whole dataset
* **simulation_end_dt**     : None, will simulate over the whole dataset
* **target_mape**           : the mape of the current dataset
* **a**                     : 4
* **curvature_target**      : mean of the second difference of the dataset
* **mip_gap**               : 0.3
* **number_simulations**    : 1
* **time_limit**            : 3600 seconds
* **plot_start_date**       : 0
* **seed**                  : 1234
* **verbosity**             : 2
* **sid_feature**           : "actuals"
* **base_process**          : "ARMA"
* **load_pickle**           : False
* **curvature**             : False
* **show_curv_model**       : False
* **plot**                  : True
* **solver**                : gurobi
* **title**                 : None, no additional title will be added to the plot
* **x_legend**              : None, will use the feature of curves (actuals or forecasts)



Examples
########

The following command will take the data of the CAISO.csv file, will launch n=4 simulations
from actuals to forecasts for a target_mape of 30% using an IID Base Process.
It will simulate from "2014-7-2" to "2014-7-30", and  it will
write a plot file with title "first test" to the file mmFinalFig.png.

::

    python -m mape_maker -xf "mape_maker/samples/wind_total_forecast_actual_070113_063015.csv" -n 4 -f "forecasts"  -bp "iid" -t 30 -ss "2014-7-2 00:00:00" -se "2014-7-31 00:00:00" -tt "first test"

The next example issues some errors about the bounds when finding simulation parameters and creates a directory called `output`. If that directory
already exists, it will issue an error message. The directory will have a csv file with output.

::

    python -m mape_maker -xf "mape_maker/samples/wind_total_forecast_actual_070113_063015.csv" -f "actuals" -n 4 -bp "ARMA" -is "2014-6-1 0:0:0" -ie "2014-6-30 23:0:0" --target_mape 30 --output_dir "output"


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

Github test status is |githubaction|

.. |githubaction| image:: https://github.com/mape-maker/mape-maker/workflows/mape-maker/badge.svg
