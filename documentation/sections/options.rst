.. _Options:

Options
=======
The options of the package are :

::

    python mape_maker --help

.. list-table::
   :widths: 25 25 25 50
   :header-rows: 1

   * - Options
     - Full Name
     - Types
     - Details
   * - -t
     - --target_mape
     - FLOAT
     - desired mape otherwise will take the mape of the dataset
   * - -st
     - --simulated_timeseries
     - TEXT
     - feature you want to simulate 'actuals' or 'forecasts'
   * - -bp
     - --base_process
     - TEXT
     - base procees either 'iid' or 'ARMA'
   * - -a
     - --a
     - FLOAT
     - percent of data on the left or on the right for the estimation
   * - -o
     - --output_dir
     - TEXT
     - path to dir to create for csv files
   * - -n
     - --number_simulations
     - INTEGER
     - number of simulations
   * - -is
     - --input_start_dt
     - TEXT
     - start date for the computation of the distributions, format='Y-m-d H:M:S'
   * - -ie
     - --input_end_dt
     - TEXT
     - end date for the computation of the distributions, format='Y-m-d H:M:S'
   * - -sd
     - --simulation_start_dt
     - TEXT
     - start date for the simulation, format='Y-m-d H:M:S'
   * - -ed
     - --simulation_end_dt
     - TEXT
     - end date for the simulation, format='Y-m-d H:M:S'
   * - -ti
     - --title
     - TEXT
     - title for the plot
   * - -s
     - --seed
     - INTEGER
     - random seed
   * - -lp
     - --load_pickle
     - BOOLEAN
     - load the pickle file for the data file instead of estimation
   * - -c
     - --curvature
     - TEXT
     - curvature
   * - -tl
     - --time_limit
     - INTEGER
     - time limit for the computation of smoothness
   * - -ct
     - --curvature_target
     - FLOAT
     - the target of the second difference
   * - -m
     - --mip_gap
     - FLOAT
     - the mip gap
   * - -so
     - --solver
     - TEXT
     - solver
   * - -fd
     - --full_dataset
     - BOOLEAN
     - simulation over all the dataset
   * - -lo
     - --latex_output
     - BOOLEAN
     - write results in latex file
   * - -sh
     - --show
     - BOOLEAN
     - plot simulations
   * -
     - --help
     -
     - Show this message and exit.
|
|

Options with More Details
-------------------------
|
* **--target_mape FLOAT**:
 The target MAPE (Mean Absolute Percentage Error) gives the value of the MAPE for the simulated data.

 The following are the two ways to specify that the target MAPE should be 41.1:

 ``--target_mape 41.1``

 ``-t 41.1``

 If this option is not given, the target MAPE is the MAPE of the input data.
|
* **--simulated_timeseries TEXT**:
 If the user wants to simulate actuals from forecasts, then the simulated timeseries will be "actuals".
 On the other hands, if the user wants to simulate forecasts from actuals, then the simulated timeseries
 will be "forecasts".

 The following are the two ways to specify that simulated timeseries is "actuals":

 ``--simulated_timeseries "actuals"``

 ``-st "actuals"``

 If this option is not given, the simulated timeseries is assumed to be "actuals".
|
* **--base_process TEXT**:
 The base process is either "iid" or "ARMA".
 When "iid" is selected, then the forecast errors are assumed to be independent and identically distributed.
 When "ARMA" is selected, then an autoregressive time series is used as a base process in simulations
 so the forecast errors are correlated.

 The following are the two ways to specify that base process is iid:

 ``--base_process "iid"``

 ``-bp "iid"``

 If this option is not given, the base process is assumed to be "ARMA"
|
* **--a FLOAT**:
 Estimate over a sample with a% of data on the left and a% on the right.

 The following are the two ways to specify that the percent of data is 4.3:

 ``--a 4.3``

 ``-a 4.3``

 If this option is not given, the percent of data on the left and on the right for the estimation is assumed to be 4.
|
* **--output_dir TEXT**:
 Path to dir to create the simulation output files

 The following are the two ways to specify that the output directory is called "output":

 ``--output_dir "output"``

 ``-o "output"``

 If this option is not given, the output directory is assumed to be None. No output directory
 will be created.

.. note:: If the output directory is not given, then the only output will be a png fir showing the scenarios.
.. warning:: If the output directory already exists, the program will terminate and issue messages. It won't overwrite an existing directory.
|
* **--number_simulations INTEGER**:
 The number of scenarios created.

 The following are the two ways to specify that the number of simulations is 4:

 ``--number_simulations 4``

 ``-n 4``

 If this option is not given, the number of simulations is assumed to be 1.
|
* **--simulation_start_dt TEXT**:
 The start date of the simulation, must be between the input file date range. (format= Y-m-d H:M:S)

 The following are two ways to specify that the start date for the simulation is 2020-1-3 00:00:00 :

 ``--simulation_start_dt "2020-1-3 00:00:00"``

 ``-sd "2020-1-3 00:00:00"``

.. note:: The user need to set both "simulation_start_dt" and "simulation_end_dt" to make it work.
 If this option is not given, then it will use "input_start_dt" as the simulation start date.
 If "input_start_dt" is None, then it will use the first date of the input file as the simulation start date.
 The "simulation_start_dt" must be on or after the input start date for the simulations.
|
* **--simulation_end_dt TEXT**:
 The end date of the simulation, must be between the input file date range. (format= Y-m-d H:M:S)

 The following are two ways to specify that the end date for the simulation is 2020-1-3 00:00:00 :

 ``--simulation_end_dt "2020-1-3 00:00:00"``

 ``-ed "2020-1-3 00:00:00"``

 .. note:: The user need to set both "simulation_start_dt" and "simulation_end_dt" to make it work.
 If this option is not given, then it will use "input_end_dt" as the simulation end date.
 If "input_end_dt" is None, then it will use the last date of the input file as the simulation end date.
|
* **--input_start_dt TEXT**:
  The start date for the computation of the distributions, must be between the input file date range. (format= Y-m-d %H:%M:%S)

  The following are two ways to specify that the start date for the computation of the distributions is 2020-1-3 00:00:00 :

  ``--input_start_dt "2020-1-3 00:00:00"``

  ``-is "2020-1-3 00:00:00"``

 .. note:: The user need to set both "input_start_dt" and "input_end_dt" to make it work.
 If this option is not given, then it will use the first date of the input file as the start date for the computation of the distributions.
|
* **--input_end_dt TEXT**:
  The end date for the computation of the distributions, must be between the input file date range. (format= Y-m-d %H:%M:%S)

  The following are two ways to specify that the end date for the computation of the distributions is 2020-1-3 00:00:00 :

  ``--input_end_dt "2020-1-3 00:00:00"``

  ``-ie "2020-1-3 00:00:00"``

  .. note:: The user need to set both "input_start_dt" and "input_end_dt" to make it work.
 If this option is not given, then it will use the last date of the input file as the start date for the computation of the distributions.
|
* **--title TEXT**:
 The title of the simulation plot.

 The following are two ways to specify that the title of the simulation plot is "my plot":

 ``--title "my plot"``

 ``-ti "my plot"``

 If this option is not given, the title of the simulation plot is assumed to be None. Therefore, no additional title will be added to the plot.
|
* **--seed INTEGER**:
 The seed used for simulation. If none, the seed will be random.

 The following are two ways to specify that the title if the seed is set as "1134":

 ``--seed 1134``

 ``-s 1134``

 If this option is not given, the seed is assumed to be 1234.
|
* **--load_pickle**:

This will load the pickle file for the data file instead of estimation.
Every run of the simulation using ARMA base process will update the pickle file
in the stored_vectors subdirectory in the utilities directory, and contains
the parameters for conditional beta distribution.
This command can be used to call the pickle file containing the values for the parameters
when we are using ARMA base process, the same subset of the dataset as the last run and
want the same target mape as the preceeding commands for that data file.

 ``--load_pickle``

 ``-lp``

 If this option is not given, then the parameters for the beta distribution are computed.
|
* **--curvature BOOLEAN**:
 Whether the user wants to set the curvature.

 Curvature is the second difference of the time series of output.
 (If you are not sure whether to use the curvature, you should set it as False)

 The following are two ways to specify that the curvature is True:

 ``--curvature True``

 ``-c True``

 If this option is not given, the curvature is assumed to be False
|
* **--time_limit INTEGER**:
 Time limit of the computation of curvature.

 The following are two ways to specify that the time limit is 40 seconds:

 ``--time_limit 40``

 ``-tl 40``

 If this option is not given, the time limits is assumed to be 3600 seconds.
|
* **--curvature_target FLOAT**:
 The target of the second difference. ADD

 The following are two ways to specify that the target of the second difference is 3.1:

 ``--curvature_target 3.1``

 ``-ct 3.1``

 If this option is not given, the target of the second difference is assumed to be the mean of the second difference of the dataset.
|
* **--mip_gap FLOAT**:
 the mip gap for the curvature optimization

 The following are two ways to specify that the mip gap is 0.1:

 ``--mip_gap 0.1``

 ``-m 0.1``

 If this option is not given, the mip gap is assumed to be 0.3.
|
* **--solver TEXT**:
 The software that is used during the curvature optimization process.

 The following are two ways to specify that the solver is "cpley":

 ``--solver "cpley"``

 ``-so "cpley"``

 If this option is not given, the solver is assumed to be "gurobi".
|
* **--full_dataset BOOLEAN**:
 simulation over the entire input dataset

 The following are two ways to specify that the full dataset is True:

 ``--full_dataset True``

 ``-fd True``

 If this option is not given, the full dataset is assumed to be False.
|
* **--latex_output BOOLEAN**:
 Write your result in the latex output(latex output is not available for now).

 The following are two ways to specify that the latex output is set as True:

 ``--latex_output True``

 ``-lo True``

 If this option is not given, the latex output is assumed to be False since it is not supported yet.
|
* **--show BOOLEAN**:
 show and save the simulation plot

 The following are two ways to specify that the user wants to save the simulation plot:

 ``--show True``

 ``-sh True``

 If this option is not given, it will save the simulation plot by default.
|
By Default-options
------------------

* **target_mape** : the mape of the current dataset
* **simulated_timeseries** : "actuals"
* **base_process** : "ARMA"
* **a** : 4
* **output_dir** : None, no output_file will be created
* **number_simulations** : 1
* **simulation_start_dt** : None, will simulate over the whole dataset
* **simulation_end_dt** : None, will simulate over the whole dataset
* **input_start_dt**: None, will use the whole dataset for the computation of the distributions
* **input_end_dt**: None, will use the whole dataset for the computation of the distributions
* **title** : None, no additional title will be added to the plot
* **seed** : 1234
* **load_pickle** : False.
* **curvature** : False
* **time_limit** : 3600 seconds
* **curvature_target** : mean of the second difference of the dataset
* **mip_gap** : 0.3
* **solver** : gurobi
* **full_dataset** : False
* **latex_output** : False, not supported yet
* **show** : True