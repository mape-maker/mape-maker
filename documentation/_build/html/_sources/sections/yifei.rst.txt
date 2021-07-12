Yifei
######

Options
########

The options of the package are :

::

    python mape_maker --help
    Options   Options Full Name        Types       Details
      -t,     --target_mape            FLOAT       desired mape otherwise will take the mape of the dataset
      -st,    --simulated_timeseries   TEXT        feature you want to simulate 'actuals' or 'forecasts'
      -bp,    --base_process           TEXT        base procees either 'iid' or 'ARMA'
      -a,     --a                      FLOAT       percent of data on the left or on the right for the estimation
      -o,     --output_dir             TEXT        path to dir to create for csv files
      -n,     --number_simulations     INTEGER     number of simulations
      -sd,    --start_date             TEXT        start_date for the simulation, format='Y-m-d'
      -ed,    --end_date               TEXT        end_date for the simulation, format='Y-m-d'
      -ti,    --title                  TEXT        title for the plot
      -s,     --seed                   INTEGER     random seed
      -c,     --curvature              TEXT        curvature
      -tl,    --time_limit             INTEGER     time limit for the computation of smoothness
      -ct,    --curvature_target       FLOAT       the target of the second difference
      -m,     --mip                    FLOAT       the mip gap
      -so,    --solver                 TEXT        solver
      -fd,    --full_dataset           BOOLEAN     simulation over all the dataset
      -lo,    --latex_output           BOOLEAN     write results in latex file
      -sh,    --show                   BOOLEAN     plot simulations
      --help                                    Show this message and exit.

Options with More Details
****************************

* **--target_mape FLOAT**:
 The target MAPE(Mean Absolute Percentage Error) gives the value of the MAPE for the simulated data.

 The following are the two ways to specify that the target MAPE should be 41.1:

 ``--target_mape 41.1``

 ``-t 41.1``

 If this option is not given, the target MAPE is the MAPE of the input dataset.

* **simulated_timeseries(TEXT)**:
 If the user wants to simulate actuals from forecasts, then the simulated timeseries will be "actuals".
 On the other hands, if the user wants to simulate forecasts from actuals, then the simulated timeseries
 will be "forecasts".

 The following are the two ways to specify that simulated timeseries is "actuals":

 ``--simulated_timeseries "actuals"``

 ``-st "actuals"``

 If this option is not given, the simulated timeseries is assumed to be "actuals".

* **base_process(TEXT)**:
 The base process is either "iid" or "ARMA". When "iid" then the forecast errors
 are assumed to be independent and identically distributed. When "ARMA" is selected
 than an autoregressive time series it used as a base process in simulations
 so the forecast errors are correlated.

 The following are the two ways to specify that base process is iid:

 ``--base_process "iid"``

 ``-bp "iid"``

 If this option is not given, the base process is assumed to be "ARMA"

* **a(FLOAT)**:
 Estimate over a sample with a% of data on the left and a% on the right.

 The following are the two ways to specify that the percent of data is 4.3:

 ``--a 4.3``

 ``-a 4.3``

 If this option is not given, the percent of data on the left and on the right for the estimation is assumed to be 4.

* **output_dir(TEXT)**:
 Path to dir to create the simulation output files

 The following are the two ways to specify that the output directory is called "output":

 ``--output_dir "output"``

 ``-o "output"``

 If this option is not given, the output directory is assumed to be None. No output directory
 will be created.

* **--number_simulations INTEGER**:
 The number of simulations

 The following are the two ways to specify that the number of simulations is 4:

 ``--number_simulations 4``

 ``-n 4``

 If this option is not given, the number of simulations is assumed to be 1.

* **--start_date TEXT**:
 The start date of the simulation, must be between the input file date range.

 The following are two ways to specify that the start date is 2020-1-3:

 ``--start_date 2014-6-30``

 ``-sd 2014-6-30``

 If this option is not given, the start date is assumed to be None, which will simulate the whole dataset.

* **--end_date TEXT**:
 The end date of the simulation, must be between the input file date range.

 The following are two ways to specify that the end date is 2020-1-3:

 ``--end_date 2014-6-30``

 ``-ed 2014-6-30``

 If this option is not given, the end date is assumed to be None, which will simulate the whole dataset.

* **--title TEXT**:
 The title of the simulation plot.

 The following are two ways to specify that the title if the simulation plot is called "plot":

 ``--title "plot"``

 ``-ti "plot"``

 If this option is not given, the title of the simulation plot is assumed to be None. Therefore, no additional title will be added to the plot.

* **--seed INTEGER**:
 The seed used for simulation. If none, the seed will be random.

 The following are two ways to specify that the title if the seed is set as "1234":

 ``--seed 1234``

 ``-s 1234``

 If this option is not given, the seed is assume to be 1234.

* **--curvature BOOLEAN**:
 Whether the user wants to set the curvature or not.

 Curvature is the second difference of the time series of output.
 (If you are not sure whether to use the curvature, you can set it as False)

 The following are two ways to specify that the curvature is True:

 ``--curvature True``

 ``-c True``

 If this option is not given, the curvature is assumed to be False

* **--time_limit INTEGER**:
 Time limit of the computation of curvature.

 The following are two ways to specify that the time limit is 40 seconds:

 ``--time_limit 40``

 ``-tl 40``

 If this option is not given, the time limits is assumed to be 3600 seconds.

* **--curvature_target FLOAT**:
 The target of the second difference.

 The following are two ways to specify that the target of the second difference is 3.1:

 ``--curvature_target 3.1``

 ``-ct 3.1``

 If this option is not given, the target of the second difference is assumed to be the mean of the second difference of the dataset.

* **--mip FLOAT**:
 the mip gap

 The following are two ways to specify that the mip gap is 3.2:

 ``--mip 3.2``

 ``-m 3.2``

 If this option is not given, the mip gap is assumed to be 0.3.

* **--solver TEXT**:
 The software that is used during the optimization process.

 The following are two ways to specify that the solver is "gurobi":

 ``--solver "gurobi"``

 ``-so "gurobi"``

 If this option is not given, the solver is assumed to be "gurobi".

* **--full_dataset BOOLEAN**:
 simulation over the entire input dataset

 The following are two ways to specify that the full dataset is True:

 ``--full_dataset True``

 ``-fd True``

 If this option is not given, the full dataset is assumed to be False.

* **--latex_output BOOLEAN**:
 Write your result in the latex output(latex output is not available for now).

 The following are two ways to specify that the latex output is set as True:

 ``--latex_output True``

 ``-lo True``

 If this option is not given, the latex output is assumed to be False since it is not supported yet.

* **--show BOOLEAN**:
 show and save the simulation plot

 The following are two ways to specify that the user wants to show and save the simulation plot:

 ``--show True``

 ``-sh True``

 If this option is not given, it will show and save the simulation plot by default.

Wind data file examples
************************

Examples
---------

sample command 1:
+++++++++++++++++

The following command will take the data from *wind_total_forecast_actual_070113_063015.csv*
, and launch the simulations with n=3 and seed=1234 from forecasts to actuals using an IID
Base Process. It will simulate all the dates in the input files. Finally, it will return a
plot of simulations, and create an output dir called "wind_data_command_1".

::

    python mape_maker "mape_maker/samples/wind_total_forecast_actual_070113_063015.csv" -st "actuals" -n 3 -bp "iid" -o "wind_data_command_1" -s 1234

This command will first call the __main__.py, which will create a MapeMaker class and
call the simulate function. You should see a plot similar to this:

* **"mape_maker/samples/wind_total_forecast_actual_070113_063015.csv"**:
 The csv file containing forecasts and actuals for specified datetimes.
* **-st "actuals"**:
 Set up the the target of the simulation as "actuals". So the MapeMaker will simulate the "actuals" data
 according to the "forecasts" data in the input file.
* **-n 3**:
 The number of simulations that we want to create is "3". This will create three simulation columns in the output file.
* **-bp "iid"**:
 Use "iid" as the base process. The default base process is set as "ARMA".
* **-s 1234**:
 Set the seed as "1234", so it won't randomly choose a number as the seed.
* **-o "wind_data_command_1"**：
 Create an output directory called "wind_data_command_1", in which will store the simulation output file.

After running the command line, you should see a similar plot like this:

.. figure::  ../_static/wind_command_line1.png
   :align:   center

sample command 2:
+++++++++++++++++

The following command will take the data from *wind_total_forecast_actual_070113_063015.csv*
, and launch the simulations with n=5 and target mape=30 from actuals to forecasts using an ARMA
Base Process. It will simulate from 2014-6-1 to 2014-6-30. Finally, it will return a
plot of simulations, and create an output dir called "wind_data_command_2".

::

    python mape_maker "mape_maker/samples/wind_total_forecast_actual_070113_063015.csv" -st "forecasts" -n 5 -bp "ARMA" -o "wind_data_command_2" -sd "2014-6-1" -ed "2014-6-30" -t 30 -s 1234

This command will first call the __main__.py, which will create a MapeMaker class and
call the simulate function. You should see a plot similar to this:

* **"mape_maker/samples/wind_total_forecast_actual_070113_063015.csv"**:
 The csv file containing forecasts and actuals for specified datetimes.
* **-st "forecasts"**:
 Set up the the target of the simulation as "forecasts". So the MapeMaker will simulate the "forecasts" data
 according to the "actuals" data in the input file.
* **-n 5**:
 The number of simulations that we want to create is "5". This will create three simulation columns in the output file.
* **-bp "ARMA"**:
 Use "ARMA" as the base process. The default base process is set as "ARMA".
* **-sd "2014-6-1"**:
 The start date of the simulation is "2014-6-1"
* **-ed "2014-6-30"**:
 The end date of the simulation is "2014-6-30"
* **-t 30**
 The mape that you want to return is 30
* **-s 1234**:
 Set the seed as "1234", so it won't randomly choose a number as the seed.

After running the command line, you should see a similar plot like this:


Additional examples
--------------------

sample command 3:
+++++++++++++++++

The following command will take the data from *wind_total_forecast_actual_070113_063015.csv*
, and launch the simulations with n=3 and seed=1234 from forecasts to actuals using an IID
Base Process. It will simulate all the dates in the input files. Finally, it will return a
plot of simulations, and create an output dir called "wind_data_command_1".

::

    python mape_maker "mape_maker/samples/wind_total_forecast_actual_070113_063015.csv" -st "actuals" -n 3 -bp "ARMA" -o "wind_data_command_3" -s 1234

This command will first call the __main__.py, which will create a MapeMaker class and
call the simulate function. You should see a plot similar to this:

* **"mape_maker/samples/wind_total_forecast_actual_070113_063015.csv"**:
 The csv file containing forecasts and actuals for specified datetimes.
* **-st "actuals"**:
 Set up the the target of the simulation as "actuals". So the MapeMaker will simulate the "actuals" data
 according to the "forecasts" data in the input file.
* **-n 3**:
 The number of simulations that we want to create is "3". This will create three simulation columns in the output file.
* **-bp "ARMA"**:
 Use "ARMA" as the base process. The default base process is set as "ARMA".
* **-s 1234**:
 Set the seed as "1234", so it won't randomly choose a number as the seed.
* **-o "wind_data_command_3"**：
 Create an output directory called "wind_data_command_3", in which will store the simulation output file.

After running the command line, you should see a similar plot like this:

.. figure::  ../_static/wind_command_line3.png
   :align:   center

sample command 4:
+++++++++++++++++

The following command will take the data from *wind_total_forecast_actual_070113_063015.csv*
, and launch the simulations with n=5 and target mape=30 from actuals to forecasts using an ARMA
Base Process. It will simulate from 2014-6-1 to 2014-6-30. Finally, it will return a
plot of simulations, and create an output dir called "wind_data_command_2".

::

    python mape_maker "mape_maker/samples/wind_total_forecast_actual_070113_063015.csv" -st "forecasts" -n 5 -bp "iid" -o "wind_data_command_4" -sd "2014-6-1" -ed "2014-6-30" -t 30 -s 1234

This command will first call the __main__.py, which will create a MapeMaker class and
call the simulate function. You should see a plot similar to this:

* **"mape_maker/samples/wind_total_forecast_actual_070113_063015.csv"**:
 The csv file containing forecasts and actuals for specified datetimes.
* **-st "forecasts"**:
 Set up the the target of the simulation as "forecasts". So the MapeMaker will simulate the "forecasts" data
 according to the "actuals" data in the input file.
* **-n 5**:
 The number of simulations that we want to create is "5". This will create three simulation columns in the output file.
* **-bp "iid"**:
 Use "iid" as the base process. The default base process is set as "ARMA".
* **-sd "2014-6-1"**:
 The start date of the simulation is "2014-6-1"
* **-ed "2014-6-30"**:
 The end date of the simulation is "2014-6-30"
* **-t 30**
 The mape that you want to return is 30
* **-s 1234**:
 Set the seed as "1234", so it won't randomly choose a number as the seed.

After running the command line, you should see a similar plot like this:

.. figure::  ../_static/wind_command_line4.png
   :align:   center


Unittest
---------

wind_quick_test.py
+++++++++++++++++++

* This test is used to see whether the above command lines will run successfully at once.
* You can run this unittest by typing "python wind_quick_test.py" in your terminal.
* wine_quick_test.py will first save the current working directory and change to a temporary directory. It will then run the above command lines and save the output dir to the folder where you run the tests. Finally, it will return back to the previous directory once the unittest is finished.
* Since command 3 and command 4 are similar to command 1 and command 2, if you want to save the running time, you can skip the last two tests by setting "skip_test"(line 16) to False.

.. figure::  ../_static/skip_test_line.png
   :align:   center


wind_slow_test.py
++++++++++++++++++

* The difference between wind_quick_test.py and wind_slow_test.py is that the second one will show more details. After running each above command line, it will find the difference between simulation 1 and simulation 2 in each row, then save the result to a csv file called "simulation_comparison". At the same time, it will also plot the simulation differences and save the graph called "simulation_plot".
* As you can see the picture below, "simulation_comparison" add a new column called "simulation_1_minus_2" comparing to the original output file.

.. figure::  ../_static/sample_simulation_diff.png
   :align:   center

* The "simulation_plot" will show a set of blue dots, where the y-axis represents the range of differences, and the x-axis stands for the dates(from start date to end date).

.. figure::  ../_static/sample_plot.png
   :align:   center



Setup
******

* Your python version should be at 3.x.x(i.e 3.7.1). You can check your current version by typing "python --version" in your terminal.
* If you want to initialize and use the curvature, you need to install a Quadratic MIP solver such as "Gurobi" first: www.gurobi.com/
(e.g Gurobi, Cplex, SCJP, etc.)

1. Click on "Clone or download" to copy the web URL.
2. Switch to a proper directory and then type:

::

    git clone + the web URL link that you copied

to clone the entire "mape_maker_v2" to your own directory

3. Install the package with the setup.py file:

::

    python setup.py develop


4. You can use the package in command-line, for a quick-first run :

::

    python -m mape_maker "mape_maker/samples/wind_total_forecast_actual_070113_063015.csv"


Input file format
*******************

If you want to use your own datafile as an input to run the mape_maker, then the input file format should be:

* Datetime as the first column, format as "year-month-day + time". i.e: 2017-1-3 00:00
* Forecast data as the second column, format as "float". i.e: 3264.59
* Actual data as the third column, format as "float". i.e: 3264.59


CAISO wind data file examples(Revised version)
===============================================
Examples
---------

**sample command 1:**

---------------------------------------------

The following command will take the data from *wind_total_forecast_actual_070113_063015.csv*
, and launch the simulations with n=3 and seed=1234 from forecasts to actuals using an IID
Base Process. It will simulate all the dates in the input files. Finally, it will return a
plot of simulations, and create an output dir called "wind_data_command_1".

::

    python mape_maker "mape_maker/samples/wind_total_forecast_actual_070113_063015.csv" -st "actuals" -n 3 -bp "iid" -o "wind_data_command_1" -s 1234

This command will first call the __main__.py, which will create a MapeMaker class and
call the simulate function. You should see a plot similar to this:

* **"mape_maker/samples/wind_total_forecast_actual_070113_063015.csv"**:
 The csv file containing forecasts and actuals for specified datetimes.
* **-st "actuals"**:
 Set up the the target of the simulation as "actuals". So the MapeMaker will simulate the "actuals" data
 according to the "forecasts" data in the input file.
* **-n 3**:
 The number of simulations that we want to create is "3". This will create three simulation columns in the output file.
* **-bp "iid"**:
 Use "iid" as the base process. The default base process is set as "ARMA".
* **-s 1234**:
 Set the seed as "1234", so it won't randomly choose a number as the seed.
* **-o "wind_data_command_1"**:
 Create an output directory called "wind_data_command_1", in which will store the simulation output file.

After running the command line, you should see a similar plot like this:

.. figure::  ../_static/wind_command_line1.png
   :align:   center

|
|

**sample command 2:**

---------------------------------------------

The following command will take the data from *wind_total_forecast_actual_070113_063015.csv*
, and launch the simulations with n=5 and target mape=30 from forecasts to actuals using an ARMA
Base Process. It will simulate from 2014-6-1 to 2014-6-30. Finally, it will return a
plot of simulations, and create an output dir called "wind_data_command_2".

::

    python mape_maker "mape_maker/samples/wind_total_forecast_actual_070113_063015.csv" -st "actuals" -n 5 -bp "ARMA" -o "wind_data_command_2" -is "2014-6-1 00:00:00" -ie "2014-6-30 00:00:00" -sd "2014-6-27 01:00:00" -ed "2014-6-30 00:00:00" -t 30 -s 1234

This command will first call the __main__.py, which will create a MapeMaker class and
call the simulate function. You should see a plot similar to this:

-is "2014-6-1 00:00:00" -ie "2014-6-30 00:00:00" -sd "2014-6-27 01:00:00" -ed "2014-6-30 00:00:00"

* **"mape_maker/samples/wind_total_forecast_actual_070113_063015.csv"**:
 The csv file containing forecasts and actuals for specified datetimes.
* **-st "actuals"**:
 Set up the the target of the simulation as "actuals". So the MapeMaker will simulate the "actuals" data
 according to the "forecasts" data in the input file.
* **-n 5**:
 The number of simulations that we want to create is "5". This will create three simulation columns in the output file.
* **-bp "ARMA"**:
 Use "ARMA" as the base process. The default base process is set as "ARMA".
* **-is "2014-6-1 00:00:00"**:
 Use "2014-6-1 00:00:00" as the starting datetime of the input dataset to compute distributions (default is all data).
* **-ie "2014-6-30 00:00:00"**
 Use "2014-6-1 00:00:00" as the ending datetime of the input dataset to compute distributions (default is all data).
* **-sd "2014-6-27 01:00:00"**:
 The start date of the simulation is "2014-6-27 01:00:00".
* **-ed "2014-6-30 00:00:00"**:
 The end date of the simulation is "2014-6-30 00:00:00".
* **-t 30**:
 The mape that you want to return is 30.
* **-s 1234**:
 Set the seed as "1234", so it won't randomly choose a number as the seed.

After running the command line, you should see a similar plot like this:

.. figure::  ../_static/wind_command_line1.png
   :align:   center


Unittest Examples for RTS WIND and BUS
=======================================
**RTS Wind Unittest Examples**

---------------------------------------------
.. raw:: html

   <b><i><u>RTS_wind_test.py</u></i></b>

* This test is used to see whether the above command lines will run successfully at once.
* You can run this unittest by typing "python RTS_wind_test.py" in your terminal.
* RTS_wind_test.py will first save the current working directory and change to a temporary directory. It will then run the above command lines and save the output dir to the folder where you run the tests. Finally, it will return back to the previous directory once the unittest is finished.

.. figure::  ../_static/skip_test_line.png
   :align:   center

