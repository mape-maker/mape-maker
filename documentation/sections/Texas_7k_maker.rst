.. _Texas_7k_maker:

Texas_7k_maker
================
The ``Texas_7k_maker`` program enables quick creation of scenario files based on Texas7k data.
The options of this program is a subset of the options in ``Mape_Maker``, with additional
options for geographic scale (individual sites or sum of all sites) and data source.

Options
*******
|
* **\\-\\-data_source TEXT**:
 The source of simulation data (..._test contains smaller datasets for quick test).

 The options to choose from are: "Princeton", "Princeton_test", "NREL_ECMWF_PEFORM", and "NREL_ECMWF_PEFORM_test".

 The following are the two ways to specify that data source is "Princeton_test":

 ``--data_source "Princeton_test"``

 ``-ds "Princeton_test"``

 If the simulation start date is not given, it will use the "Princeton_test" data.
|
* **\\-\\-geographic_scale TEXT**:
 Simulation for each individual sites or the sum of all sites.
 
 Choose "sum" or "individual".

 The following are the two ways to specify that scenarios are created for each individual sites:

 ``--geographic_scale "individual"``

 ``-gc "individual"``

 If the geographic_scale is not given, it will create scenarios for the sum of all sites.
|
* **\\-\\-output_dir TEXT**:
 Path to destination dir where the scenario are saved as csv file(s).

 The following are the two ways to specify that the output directory is called "output":

 ``--output_dir "output"``

 ``-o "output"``

 This option is required if the user choose "sum" as geographic scale, and if this option is not given, a value error will be raised.
 
 For "individual" as geographic scale, the names of output directory are the names of sites. 
|
* **\\-\\-simulation_start_dt TEXT**:
 The start date of the simulation of scenarios, must be between the input file date range. (format = "Y-m-d H:M:S")

 The following are two ways to specify that the start date for the simulation is 2020-1-3 00:00:00 :

 ``--simulation_start_dt "2020-1-3 00:00:00"``

 ``-ss "2020-1-3 00:00:00"``

 If the simulation start date is not given, it will take the first date of the sid file as simulation start date.
|
* **\\-\\-simulation_end_dt TEXT**:
 The end date of the simulation of scenarios, must be between the input file date range. (format = "Y-m-d H:M:S")

 The following are two ways to specify that the end date for the simulation is 2020-1-3 00:00:00 :

 ``--simulation_end_dt "2020-1-3 00:00:00"``

 ``-se "2020-1-3 00:00:00"``

 If the simulation end date is not given, it will take the last date of the sid file as simulation end date.
|
* **\\-\\-target_mape FLOAT**:
 The target MAPE (Mean Absolute Percentage Error) sets the value of the desired MAPE for the simulated data.

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
 The seed used for simulation. If none, the seed will be random.

 The following are two ways to specify that the title if the seed is set as "1134":

 ``--seed 1134``

 ``-s 1134``

 If this option is not given, the seed will be randomly chosen.
|
* **\\-\\-t7k_plot BOOLEAN**:
 True if the user wants to plot the results.

 The following are two ways to specify to plot the result:

 ``--t7k_plot``

 ``-pl``

 If this option is not given, the option is assumed to be True

|
* **\\-\\-scale_by_capacity FLOAT**:
 Calculate MAPE relative to capacity instead of observations, i.e.
 
 .. math::
  mape = \frac{100}{n} \sum_{i=1}^n \frac{|f_i - a_i|}{cap}

 The following are the two ways to specify that the capacity is 2000:

 ``--scale_by_capacity 2000``

 ``-sb 2000``

 If this option is not given, scale by observation.

 If this option is given to be 0, capacity is set to be the maximum of the observation.
|
* **\\-\\-target_scaled_capacity FLOAT**:
 Optionally enter target capacity to scale all simulated data by target_capacity/capacity
 
 The following are the two ways to specify that the target capacity is 1000:

 ``--target_scaled_capacity 1000``

 ``-ts 1000``

 If this option is not given, simulated data is not scaled.

Example
*******

::

    python -m mape_maker.Texas_7k.Texas_7k_maker -ds "Princeton_test" -gs "individual" -n 2
* **-ds "Princeton_test"**:
 The data source is "Princeton_test".
* **-gs "individual"**:
 The geographic scale is "individual", meaning the scenarios will be created for each individual sites. 
* **-n 2**:
 The number of simulations that we want to create is "2". This will create two simulation columns in the output file.

Imutable Features
*****************
The following MapeMaker options cannot be changed from the command line in ``Texas_7k_maker``.

* **\\-\\-sid_feature "actuals"**:
 Set up the the target of the simulation as "actuals". So the ``Texas_7k_maker`` will simulate the "actuals" data
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

