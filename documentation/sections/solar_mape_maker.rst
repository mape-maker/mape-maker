.. _solar_mape_maker:

solar_mape_maker
================
The ``solar_mape_maker.py`` program enables creation of scenario files using solar data.
It calculates the difference between the input data and upper bound of solar energy generation at the same time 
as the input data. The upper bound uses the maximum of clear-sky POA from the location parameters users put in,
and the algorithm is described in *Constructing probabilistic scenarios for wide-area solar power generation* by
Professor David Woodruff et al. 
This difference is used to feed in ``Mape_Maker`` to generate scenarios. Then the output of ``Mape_Maker`` is added
to the upper bound to create the final solar scenarios. 

Required Argument
*****************
|
* **\\-\\-input_solar_file TEXT**:
 The path to input solar dataset that contains date time, forecasts and actuals (the same format as the input
  of ``Mape_Maker``).

 The following specify "solar_data.csv" as the input file:

 ``--input_solar_file "solar_data.csv"``

 ``-isf "solar_data.csv"``

|
* **\\-\\---location_coor int**:
 The coordinates of the location where the input solar data is collected.
 It can be either a pair of coordinates for data collected from an individual site, or several pairs of coordinates
 that are the extreme points (northernmost/southernmost/easternmost/westernmost) of the group of sites from which
 the data is collected. Use space to separate numbers and enter in the sequence of latitude_1 longitude_1 latitude_2 longitude_2

 The following specify the location as (37N 103W):

 ``--location_coor 37 -103``

 ``-lc 37 -103``

 The following specify the rage of generation site location is within (37N 103W), (31N 94W) and (32N 107W)
 
 ``--location_coor 37 -103 31 -94 26 -98 32 -107``

 ``-lc 37 -103 31 -94 26 -98 32 -107``

Options
*******
|
* **\\-\\-input_sid_file TEXT**:
 The path to a simulation input dataset (sid) with one or two timeseries (e.g. actuals), from which scenarios for the other timeseries are generated (e.g. forecasts)

 The following loads "sid.csv" located under the current directory :

 ``--input_sid_file "sid.csv"``

 ``-sf "sid.csv"``

 If this option is not given, the sid will be taken as a subset of the input dataset, specified by a simulation_start_dt and simulation_end_dt.
* **\\-\\-solar_output TEXT**:
 Path to destination dir where the scenario are saved as csv file(s).

 The following are the two ways to specify that the output directory is called "output":

 ``--solar_output "output"``

 ``-so "output"``

 If this option is not given, the output directory is assumed to be None. No output directory
 will be created.

 .. note:: If the output directory is not given, then the only output will be a png image of the plot showing the scenarios and saved under the current directory.
 .. warning:: If the output directory already exists, the program will terminate and issue messages. It won't overwrite an existing directory.
|
* **\\-\\-verbosity_output TEXT**:
 The name of the verbosity output file

 The following are two ways to specify the verbosity level:

 ``--verbosity_output "output.log"``

 ``-vo "output.log"``

 If this option is not given, the output will be shown on terminal.

|
* **\\-\\-input_end_dt TEXT**:
  The end date for the computation of the distributions, must be between the input file date range. (format = "Y-m-d H:M:S")

  The following are two ways to specify that the end date for the computation of the distributions is 2020-1-3 00:00:00 :

  ``--input_end_dt "2020-1-3 00:00:00"``

  ``-ie "2020-1-3 00:00:00"``

  .. note:: If input end date is not given, it will take the last date of the input xyid file as input end date.
|
* **\\-\\-simulation_start_dt TEXT**:
 The start date of the simulation of scenarios, must be between the input file date range. (format = "Y-m-d H:M:S")

 The following are two ways to specify that the start date for the simulation is 2020-1-3 00:00:00 :

 ``--simulation_start_dt "2020-1-3 00:00:00"``

 ``-ss "2020-1-3 00:00:00"``

 .. note:: If the simulation start date is not given, it will take the first date of the sid file as simulation start date.
|
* **\\-\\-simulation_end_dt TEXT**:
 The end date of the simulation of scenarios, must be between the input file date range. (format = "Y-m-d H:M:S")

 The following are two ways to specify that the end date for the simulation is 2020-1-3 00:00:00 :

 ``--simulation_end_dt "2020-1-3 00:00:00"``

 ``-se "2020-1-3 00:00:00"``

 .. note:: If the simulation end date is not given, it will take the last date of the sid file as simulation end date.
|
* **\\-\\-target_mape FLOAT**:
 The target MAPE (Mean Absolute Percentage Error) sets the value of the desired MAPE for the simulated data.

 The following are the two ways to specify that the target MAPE should be 41.1:

 ``--target_mape 41.1``

 ``-t 41.1``

 If this option is not given, the target MAPE is the MAPE of the input data.
|
* **\\-\\-a FLOAT**:
 When estimating the conditional beta distribution parameters over a sample,
 a% of data on the left and a% on the right is used.

 The following are the two ways to specify that the percent of data is 4.3:

 ``--a 4.3``

 ``-a 4.3``

 If this option is not given, the percent of data on the left and on the right for the estimation is assumed to be 4.
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
* **\\-\\-number_simulations INTEGER**:
 The number of scenarios to create.

 The following are the two ways to specify that the number of simulations is 4:

 ``--number_simulations 4``

 ``-n 4``

 If this option is not given, the number of simulations is assumed to be 1.
|
* **\\-\\-time_limit INTEGER**:
 Time limit for curvature optimization.

 The following are two ways to specify that the time limit is 40 seconds:

 ``--time_limit 40``

 ``-tl 40``

 If this option is not given, the time limits is assumed to be 3600 seconds.

|
* **\\-\\-seed INTEGER**:
 The seed used for simulation. If none, the seed will be random.

 The following are two ways to specify that the title if the seed is set as "1134":

 ``--seed 1134``

 ``-s 1134``

 If this option is not given, the seed will be randomly chosen.
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
* **\\-\\-sid_feature TEXT**:
 If the user wants to simulate actuals from forecasts, then the simulated timeseries will be "actuals".
 On the other hands, if the user wants to simulate forecasts from actuals, then the simulated timeseries
 will be "forecasts".

 The following are the two ways to specify that simulated timeseries is "actuals":

 ``--sid_feature "actuals"``

 ``-f "actuals"``

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
* **\\-\\-load_pickle BOOLEAN**:

 This will load the pickle file of the estimated parameters for the input dataset and the output feature instead of re-estimating the parameters for the conditional beta distributions.

 This command can be used to improve the speed of the program by skipping the estimation part. However, it can only happen if a previous run was made for the same input dataset and for the same output feature.

 The following are two ways to specify that mape-maker should load the estimated parameters if they exist:

 ``--load_pickle``

 ``-lp``

 .. note:: Every run of mape-maker will create a new pickle file or update the existing one for that specific input dataset and output feature. The file is stored in the stored_vectors subdirectory in the mape_maker directory.
 If the pickle file does not exist or if this option is not given, then the parameters for the beta distributions are computed.
|
* **\\-\\-curvature BOOLEAN**:
 True if the user wants to optimize the scenarios curvature.

 Curvature is the second difference of the time series of output.
 (If you are not sure whether to use the curvature, you should set it as False)

 The following are two ways to specify that the curvature is True:

 ``--curvature``

 ``-c``

 If this option is not given, the curvature is assumed to be False
|
* **\\-\\-show_curv_model BOOLEAN**:
 True if the user wants to show the model for curvature.

 The following are two ways to specify to show the model:

 ``--show_curv_model``

 ``-sh``

 If this option is not given, the option is assumed to be False
|
* **\\-\\-solar_plot BOOLEAN**:
 True if the user wants to plot the results.

 The following are two ways to specify to plot the result:

 ``--solar_plot``

 ``-sp``

 If this option is not given, the option is assumed to be False
|
* **\\-\\-solver TEXT**:
 The name of the software that is used to perform the curvature optimization process.

 The following are two ways to specify that the solver is "cplex":

 ``--solver "cplex"``

 ``-sv "cplex"``

 If this option is not given, the solver is assumed to be "gurobi".

Example
*******

::

    python -m mape_maker.solar.solar_mape_maker -isf "mape_maker/solar/Solar_Taxes_2018.csv" -so "solar_test_output" -n 3 -is '2018-07-01 00:00:00' -ie '2018-12-01 00:00:00' -ss '2018-07-01 00:00:00' -se '2018-07-07 00:00:00' -n 2 -bp 'iid' -lc 37 -103 31 -94 26 -98 32 -107 -so 'test_output' -sp
* **-isf "mape_maker/solar/Solar_Taxes_2018.csv"**:
 The csv file containing forecasts and actuals for specified datetimes.
* **-so "solar_test_output"**:
 Create an output directory called "solar_test_output", in which will store the simulation output file.
* **-n 2**:
 The number of simulations that we want to create is "2". This will create two simulation columns in the output file.
* **-is "2018-07-01 00:00:00"**:
 The start time of the simulation is "2018-07-01 00:00:00".
* **-ie "2018-12-01 00:00:00"**: 
 The end time of the simulation is "2018-12-01 00:00:00". 
* **-ss "2018-07-01 00:00:00"**:
 The start time of the simulation is "2018-07-01 00:00:00".
* **-se "2018-07-07 00:00:00"**: 
 The end time of the simulation is "2013-07-07 00:00:00".  
* **-bp 'iid'**
 Use “iid” as the base process. The default base process is set as “ARMA”.
* **-lc 37 -103 31 -94 26 -98 32 -107**
  Specify the rage of generation site location is within (37N 103W), (31N 94W) and (32N 107W)
* **-sp**:
 Plot the output
|

By Default-options
------------------

* **input_sid_file**        : None, will take the input dataset as sid
* **solar_output**          : None, no output_file will be created while a plot will be outputted
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
* **seed**                  : 1234
* **verbosity**             : 2
* **sid_feature**           : "actuals"
* **base_process**          : "ARMA"
* **load_pickle**           : False
* **curvature**             : False
* **show_curv_model**       : False
* **solar_plot**            : False
* **solver**                : gurobi

Imutable Features
*****************
The following MapeMaker options cannot be changed from the command line in ``solar_mape_maker``.

* **\\-\\-scale_by_capacity 0**:
 Scale by capacity, which is the maximum of the observation data.
* **\\-\\-target_scaled_capacity None**:
 Simulated data is not scaled. 
