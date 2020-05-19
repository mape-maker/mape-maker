.. _Options:

Options
=======
The options of the package are :

::

    python mape_maker --help

.. list-table::
   :widths: 20 35 15 50
   :header-rows: 1

   * - Options
     - Full Name
     - Types
     - Details
   * - -t
     - \\-\\-target_mape
     - FLOAT
     - desired mape, otherwise will take the mape based on the input dataset
   * - -sf
     - \\-\\-second_file
     - TEXT
     - path to a simulation input dataset with one or two timeseries (e.g. actuals), from which scenarios for the other timeseries are generated (e.g. forecasts)
   * - -st
     - \\-\\-simulated_timeseries
     - TEXT
     - feature you want to simulate - 'actuals' or 'forecasts'
   * - -bp
     - \\-\\-base_process
     - TEXT
     - base process - 'iid' or 'ARMA'
   * - -a
     - \\-\\-a
     - FLOAT
     - percent of data on the left and/or on the right for the estimation of conditional beta distribution parameters
   * - -o
     - \\-\\-output_dir
     - TEXT
     - path to destination dir where the scenario csv file(s) are saved
   * - -n
     - \\-\\-number_simulations
     - INTEGER
     - number of simulations (scenarios)
   * - -is
     - \\-\\-input_start_dt
     - TEXT
     - start date for the estimation of the distributions, format = 'Y-m-d H:M:S'
   * - -ie
     - \\-\\-input_end_dt
     - TEXT
     - end date for the estimation of the distributions, format = 'Y-m-d H:M:S'
   * - -sd
     - \\-\\-simulation_start_dt
     - TEXT
     - start date for the simulation of scenarios, format='Y-m-d H:M:S'
   * - -ed
     - \\-\\-simulation_end_dt
     - TEXT
     - end date for the simulation of scenarios, format='Y-m-d H:M:S'
   * - -ti
     - \\-\\-title
     - TEXT
     - title for the plot
   * - -s
     - \\-\\-seed
     - INTEGER
     - seed for the pseudo-random seed
   * - -lp
     - \\-\\-load_pickle
     - BOOLEAN
     - load the pickle file for the dataset instead of estimation
   * - -c
     - \\-\\-curvature
     - BOOLEAN
     - optimize the curvature for the simulated scenarios
   * - -tl
     - \\-\\-time_limit
     - INTEGER
     - time limit for curvature optimization
   * - -ct
     - \\-\\-curvature_target
     - FLOAT
     - target of the second difference for curvature optimization
   * - -m
     - \\-\\-mip_gap
     - FLOAT
     - mip gap for curvature optimization
   * - -so
     - \\-\\-solver
     - TEXT
     - name of the solver (e.g. "gurobi")
   * - -sh
     - \\-\\-show
     - BOOLEAN
     - plot simulations
   * - -v
     - \\-\\-verbosity
     - INTEGER
     - verbosity level
   * - -vo
     - \\-\\-verbosity_output
     - TEXT
     - the output file to save the verbosity
   * -
     - \\-\\-help
     -
     - Show this message and exit.
|
|

Options with More Details
-------------------------
|
* **\\-\\-target_mape FLOAT**:
 The target MAPE (Mean Absolute Percentage Error) sets the value of the desired MAPE for the simulated data.

 The following are the two ways to specify that the target MAPE should be 41.1:

 ``--target_mape 41.1``

 ``-t 41.1``

 If this option is not given, the target MAPE is the MAPE of the input data.
|
* **\\-\\-second_file TEXT**:
 The path to a simulation input dataset (sid) with one or two timeseries (e.g. actuals), from which scenarios for the other timeseries are generated (e.g. forecasts)

 The following loads "sid.csv" located under the current directory :

 ``--second_file "sid.csv"``

 ``-sf "sid.csv"``

 If this option is not given, the sid will be taken as a subset of the input dataset, specified by a simulation_start_dt and simulation_end_dt.
|

* **\\-\\-simulated_timeseries TEXT**:
 If the user wants to simulate actuals from forecasts, then the simulated timeseries will be "actuals".
 On the other hands, if the user wants to simulate forecasts from actuals, then the simulated timeseries
 will be "forecasts".

 The following are the two ways to specify that simulated timeseries is "actuals":

 ``--simulated_timeseries "actuals"``

 ``-st "actuals"``

 If this option is not given, the simulated timeseries is assumed to be "actuals".
|
* **\\-\\-base_process TEXT**:

 The base process is a timeseries of random variables with marginal law following a normal law of mean 0 and variance 1.
 We then apply a transformation to the base process to retrieve the simulated errors. The base process can either be independent and identically distributed ("iid"), or simulated via an ARMA process ("ARMA"). In the last case, the base process will be correlated, hence the errors will have a stronger correlation than with an "iid" base process.

 The following are the two ways to specify that base process is iid:

 ``--base_process "iid"``

 ``-bp "iid"``

 If this option is not given, the base process is assumed to be "ARMA"
|
* **\\-\\-a FLOAT**:
 When estimating the conditional beta distribution parameters over a sample,
 a% of data on the left and a% on the right is used.

 The following are the two ways to specify that the percent of data is 4.3:

 ``--a 4.3``

 ``-a 4.3``

 If this option is not given, the percent of data on the left and on the right for the estimation is assumed to be 4.
|
* **\\-\\-output_dir TEXT**:
 Path to destination dir where the scenario are saved as csv file(s).

 The following are the two ways to specify that the output directory is called "output":

 ``--output_dir "output"``

 ``-o "output"``

 If this option is not given, the output directory is assumed to be None. No output directory
 will be created.

 .. note:: If the output directory is not given, then the only output will be a png image of the plot showing the scenarios and saved under the current directory.
 .. warning:: If the output directory already exists, the program will terminate and issue messages. It won't overwrite an existing directory.
|
* **\\-\\-number_simulations INTEGER**:
 The number of scenarios to create.

 The following are the two ways to specify that the number of simulations is 4:

 ``--number_simulations 4``

 ``-n 4``

 If this option is not given, the number of simulations is assumed to be 1.
|
* **\\-\\-simulation_start_dt TEXT**:
 The start date of the simulation of scenarios, must be between the input file date range. (format = "Y-m-d H:M:S")

 The following are two ways to specify that the start date for the simulation is 2020-1-3 00:00:00 :

 ``--simulation_start_dt "2020-1-3 00:00:00"``

 ``-sd "2020-1-3 00:00:00"``

 .. note:: The user need to set both "simulation_start_dt" and "simulation_end_dt".
 If this option is not given, then it will use "input_start_dt" as the simulation start date.
 If "input_start_dt" is None, then it will use the first date of the input file as the simulation start date.
 The "simulation_start_dt" must be on or after the input start date for the simulations.
|
* **\\-\\-simulation_end_dt TEXT**:
 The end date of the simulation of scenarios, must be between the input file date range. (format = "Y-m-d H:M:S")

 The following are two ways to specify that the end date for the simulation is 2020-1-3 00:00:00 :

 ``--simulation_end_dt "2020-1-3 00:00:00"``

 ``-ed "2020-1-3 00:00:00"``

 .. note:: The user need to set both "simulation_start_dt" and "simulation_end_dt".
 If this option is not given, then it will use "input_end_dt" as the simulation end date.
 If "input_end_dt" is None, then it will use the last date of the input file as the simulation end date.
|
* **\\-\\-input_start_dt TEXT**:
  The start date for the computation of the distributions, must be between the input file date range. (format = "Y-m-d H:M:S")

  The following are two ways to specify that the start date for the computation of the distributions is 2020-1-3 00:00:00 :

  ``--input_start_dt "2020-1-3 00:00:00"``

  ``-is "2020-1-3 00:00:00"``

  .. note:: The user need to set both "input_start_dt" and "input_end_dt"..
 If this option is not given, then it will use the first date of the input file as the start date for the computation of the distributions.
|
* **\\-\\-input_end_dt TEXT**:
  The end date for the computation of the distributions, must be between the input file date range. (format = "Y-m-d H:M:S")

  The following are two ways to specify that the end date for the computation of the distributions is 2020-1-3 00:00:00 :

  ``--input_end_dt "2020-1-3 00:00:00"``

  ``-ie "2020-1-3 00:00:00"``

  .. note:: The user need to set both "input_start_dt" and "input_end_dt".
 If this option is not given, then it will use the last date of the input file as the end date for the computation of the distributions.
|
* **\\-\\-title TEXT**:
 The title of the simulation plot.

 The following are two ways to specify the title of the simulation plot as "my plot":

 ``--title "my plot"``

 ``-ti "my plot"``

 If this option is not given, the title of the simulation plot is assumed to be None. Therefore, no additional title will be added to the plot.
|
* **\\-\\-seed INTEGER**:
 The seed used for simulation. If none, the seed will be random.

 The following are two ways to specify that the title if the seed is set as "1134":

 ``--seed 1134``

 ``-s 1134``

 If this option is not given, the seed is assumed to be 1234.
|
* **\\-\\-load_pickle**:

 This will load the pickle file of the estimated parameters for the input dataset and the output feature instead of re-estimating the parameters for the conditional beta distributions.

 This command can be used to improve the speed of the program by skipping the estimation part. However, it can only happen if a previous run was made for the same input dataset and for the same output feature.

 The following are two ways to specify that mape-maker should load the estimated parameters if they exist:

 ``--load_pickle True``

 ``-lp True``

 .. note:: Every run of mape-maker will create a new pickle file or update the existing one for that specific input dataset and output feature. The file is stored in the stored_vectors subdirectory in the utilities directory.
 If the pickle file does not exist or if this option is not given, then the parameters for the beta distributions are computed.
|
* **\\-\\-curvature BOOLEAN**:
 True if the user wants to optimize the scenarios curvature.

 Curvature is the second difference of the time series of output.
 (If you are not sure whether to use the curvature, you should set it as False)

 The following are two ways to specify that the curvature is True:

 ``--curvature True``

 ``-c True``

 If this option is not given, the curvature is assumed to be False
|
* **\\-\\-time_limit INTEGER**:
 Time limit for curvature optimization.

 The following are two ways to specify that the time limit is 40 seconds:

 ``--time_limit 40``

 ``-tl 40``

 If this option is not given, the time limits is assumed to be 3600 seconds.
|
* **\\-\\-curvature_target FLOAT**:
 Target of the second difference when the user wants to optimize the scenarios curvature.

 The following are two ways to specify that the target of the second difference is 3.1:

 ``--curvature_target 3.1``

 ``-ct 3.1``

 If this option is not given, the target of the second difference is assumed to be the mean of the second difference of the dataset.
|
* **\\-\\-mip_gap FLOAT**:
 Mip gap for curvature optimization

 The following are two ways to specify that the mip gap is 0.1:

 ``--mip_gap 0.1``

 ``-m 0.1``

 If this option is not given, the mip gap is assumed to be 0.3.
|
* **\\-\\-solver TEXT**:
 The name of the software that is used to perform the curvature optimization process.

 The following are two ways to specify that the solver is "cplex":

 ``--solver "cplex"``

 ``-so "cplex"``

 If this option is not given, the solver is assumed to be "gurobi".
|

* **\\-\\-show BOOLEAN**:
 True if the user wants to show and save the simulation plot

 The following are two ways to specify that the user wants to save the simulation plot:

 ``--show True``

 ``-sh True``

 If this option is not given, it will save the simulation plot by default.
|
* **\\-\\-verbosity INTEGER**:
 We have 3 options to choose:
    - 2 (logging.INFO), will output info, error, and warning messages.
    - 1 (logging.WARNING), will output error and warning messages.
    - 0 (logging.ERROR), will only output error messages.

 The following are two ways to specify the verbosity level:

 ``--verbosity 2``

 ``-v 2``

 If this option is not given, the verbosity level will set logging.INFO as default.
|
* **\\-\\-verbosity_output TEXT**:
 The name of the verbosity output file

 The following are two ways to specify the verbosity level:

 ``--verbosity_output "output.log"``

 ``-vo "output.log"``

 If this option is not given, the output will be shown on terminal.


By Default-options
------------------

* **target_mape**           : the mape of the current dataset
* **second_file**           : None, will take the input dataset as sid
* **simulated_timeseries**  : "actuals"
* **base_process**          : "ARMA"
* **a**                     : 4
* **output_dir**            : None, no output_file will be created while a plot will be outputted
* **number_simulations**    : 1
* **simulation_start_dt**   : None, will simulate over the whole dataset
* **simulation_end_dt**     : None, will simulate over the whole dataset
* **input_start_dt**        : None, will use the whole dataset for the computation of the distributions
* **input_end_dt**          : None, will use the whole dataset for the computation of the distributions
* **title**                 : None, no additional title will be added to the plot
* **seed**                  : 1234
* **load_pickle**           : False.
* **curvature**             : False
* **time_limit**            : 3600 seconds
* **curvature_target**      : mean of the second difference of the dataset
* **mip_gap**               : 0.3
* **solver**                : gurobi
* **latex_output**          : False, not supported yet
* **show**                  : True