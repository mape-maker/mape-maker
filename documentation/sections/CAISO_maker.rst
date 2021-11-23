.. _CAISO_maker:

CAISO_maker
===========
The ``CAISO_maker.py`` program enables quick creation of scenario files based on wind data obtained from the 
*CAISO_wind_operational_data.csv* file. The options of this program is a subset of the options in ``Mape_Maker``.


Options
*******
|

* **\\-\\-output_dir TEXT**:
 Path to destination dir where the scenario are saved as csv file(s).

 The following are the two ways to specify that the output directory is called "output":

 ``--output_dir "output"``

 ``-o "output"``

 This option is required, and if this option is not given, a value error will be raised.
|
* **\\-\\-simulation_start_dt TEXT**:
 The start date of the simulation of scenarios, must be between the input file date range. (format = "Y-m-d H:M:S")

 ``--simulation_start_dt "2020-1-3 00:00:00"``

 ``-ss "2020-1-3 00:00:00"``


 If the simulation start date is not given, it will take the first date of the sid file as simulation start date (2013-07-01 00:00:00).
|
* **\\-\\-simulation_end_dt TEXT**:
 The end date of the simulation of scenarios, must be between the input file date range. (format = "Y-m-d H:M:S")

 ``--simulation_end_dt "2020-1-3 00:00:00"``

 ``-se "2020-1-3 00:00:00"``

 If the simulation end date is not given, it will take the last date of the sid file as simulation end date (2015-06-30 23:00:00).
|
* **\\-\\-target_mape FLOAT**:
 The target MAPE (Mean Absolute Percentage Error) sets the value of the desired MAPE for the simulated data.
 The MAPE will be computed based on capacity. 
 The following are the two ways to specify that the target MAPE should be 41.1:

 ``--target_mape 41.1``

 ``-t 41.1``

 If this option is not given, the target MAPE is the MAPE of the input data.
|
* **\\-\\-number_simulations INTEGER**:
 The number of scenarios to create.

 The following are the two ways to specify that the number of simulations is 4:

 ``--number_simulations 4``

 ``-n 4``

 If this option is not given, the number of simulations is assumed to be 1.
|
* **\\-\\-seed INTEGER**:
 The seed used for simulation. 

 The following are two ways to specify that the title if the seed is set as "1134":

 ``--seed 1134``

 ``-s 1134``

 In this option is not given, the seed used for simulation is 1234.
|
* **\\-\\-plot BOOLEAN**:
 True if the user wants to plot the results.

 The following are two ways to specify to plot the result:

 ``--plot``

 ``-p``

 If this option is not given, the option is assumed to be False
Example
*******

::

    python -m mape_maker.CAISO_maker -o "CAISO_maker_test_output" -n 3 -ss "2013-07-01 00:00:00" -se "2014-07-01 00:00:00" -p


* **-o "CAISO_maker_test_output"**:
 Create an output directory called "CAISO_maker_test_output", in which will store the simulation output file.
* **-n 3**:
 The number of simulations that we want to create is "3". This will create three simulation columns in the output file.
* **-ss "2013-07-01 00:00:00"**:
 The start time of the simulation is "2013-07-01 00:00:00".
* **-se "2014-07-01 00:00:00"**: 
 The end time of the simulation is "2014-07-01 00:00:00".  
* **-p**:
 Plot the output
|
Imutable Features
*****************
The following MapeMaker options cannot be changed from the command line in ``CAISO_maker``.

* **\\-\\-input_sid_file "mape_maker/samples/CAISO_wind_operational_data.csv"**:
 The csv file containing CAISO data.
* **\\-\\-sid_feature "actuals"**:
 Set up the the target of the simulation as "actuals". So the ``CAISO_maker`` will simulate the "actuals" data
 according to the "forecasts" data in the input file.
* **\\-\\-input_start_dt None**:
 Start date for the computation of the distributions is the first date of the input xyid file.
* **\\-\\-input_end_dt None**:
 End date for the computation of the distributions is the last date of the input xyid file.
* **\\-\\-time_limit 3600**:
 Time limit for curvature optimization is 3600 seconds.
* **\\-\\-curvature_target "None"**:
 The target of the second difference is assumed to be the mean of the second difference of the dataset.
* **\\-\\-verbosity_output "None"**:
 The verbosity output will be shown on terminal.
* **\\-\\-base_process "ARMA"**:
 Use "ARMA" as the base process. The default base process is set as "ARMA".
* **\\-\\-mip_gap "0.3"**:
 Mip gap for curvature optimization is set to 0.3
* **\\-\\-a 4**:
 When estimating the conditional beta distribution parameters over a sample, 4% of data on the left and 4% on the right is used.
* **\\-\\-verbosity 2**:
 The verbosity level will set logging.INFO as default (will output info, error, and warning messages).
* **\\-\\-load_pickle False**:
 The parameters for the beta distributions are computed (no saved pickle file of the estimated parameters).
* **\\-\\-curvature False**:
 Do not optimize the scenarios curvature.
* **\\-\\-show_curv_model False**:
 Do not show the model for curvature. 
* **\\-\\-solver "gurobi"**:
 The name of the software that is used to perform the curvature optimization process is "gurobi".
* **\\-\\-scale_by_capacity 0**:
 Scale by capacity, which is the maximum of the observation data.
* **\\-\\-target_scaled_capacity None**:
 Simulated data is not scaled. 
