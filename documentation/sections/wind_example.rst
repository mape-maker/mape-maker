CAISO wind data file examples
=============================

**sample command 1:**

---------------------------------------------

The following command will take the data from *wind_total_forecast_actual_070113_063015.csv*
, and launch the simulations with n=5 and target mape=30 from forecasts to actuals using an ARMA
Base Process. It will simulate from 2014-6-27 01:00:00 to 2014-6-30 00:00:00. Finally, it will return a
plot of simulations, and create an output dir called "wind_actuals_ARMA_1".

::

    python -m mape_maker "mape_maker/samples/wind_total_forecast_actual_070113_063015.csv" -st "actuals" -n 5 -bp "ARMA" -o "wind_actuals_ARMA_1" -is "2014-6-1 00:00:00" -ie "2014-6-30 00:00:00" -sd "2014-6-27 01:00:00" -ed "2014-6-30 00:00:00" -t 30 -s 1234

This command will first call the __main__.py, which will create a MapeMaker class and
call the simulate function. You should see a plot similar to this:

* **"mape_maker/samples/wind_total_forecast_actual_070113_063015.csv"**:
 The csv file containing forecasts and actuals for specified datetimes.
* **-st "actuals"**:
 Set up the the target of the simulation as "actuals". So the MapeMaker will simulate the "actuals" data
 according to the "forecasts" data in the input file.
* **-n 5**:
 The number of simulations that we want to create is "5". This will create three simulation columns in the output file.
* **-bp "ARMA"**:
 Use "ARMA" as the base process. The default base process is set as "ARMA".
* **-sd "2014-6-27 01:00:00"**:
 The start date of the simulation is "2014-6-27 01:00:00"
* **-ed "2014-6-30 00:00:00"**:
 The end date of the simulation is "2014-6-30 00:00:00"
* **-is "2014-6-1 00:00:00"**:
 The start date for the computation of the distributions is "2014-6-1 00:00:00"
* **-ie "2014-6-30 00:00:00"**:
 The end date for the computation of the distributions is "2014-6-30 00:00:00"
* **-t 30**:
 The mape that you want to return is 30
* **-s 1234**:
 Set the seed as "1234", so it won't randomly choose a number as the seed.
 * **-o "wind_actuals_ARMA_1"**:
 Create an output directory called "wind_actuals_ARMA_1", in which will store the simulation output file.

After running the command line, you should see a similar plot like this:

.. figure::  ../_static/wind_command_line2.png
   :align:   center
|
|
**sample command 2:**

---------------------------------------------

The following command will take the data from *wind_total_forecast_actual_070113_063015.csv*
, and launch the simulations with n=3 and seed=1234 from forecasts to actuals using an IID
Base Process. It will simulate all the dates in the input files. Finally, it will return a
plot of simulations, and create an output dir called "wind_actuals_iid".

::

    python -m mape_maker "mape_maker/samples/wind_total_forecast_actual_070113_063015.csv" -st "actuals" -n 3 -bp "iid" -o "wind_actuals_iid" -s 1234

* **"mape_maker/samples/wind_total_forecast_actual_070113_063015.csv"**:
 The csv file containing forecasts and actuals for specified datetimes.
* **-st "actuals"**:
 Set up the the target of the simulation as "actuals". So the MapeMaker will simulate the "actuals" data
 according to the "forecasts" data in the input file.
* **-n 3**:
 The number of simulations that we want to create is "3". This will create three simulation columns in the output file.
* **-bp "iid"**:
 Use "iid" as the base process. The default base process is "ARMA".
* **-s 1234**:
 Set the seed as "1234", so it won't randomly choose a number as the seed.
* **-o "wind_actuals_iid"**:
 Create an output directory called "wind_actuals_iid", in which will store the simulation output file.

After running the command line, you should see a similar plot like this:

.. figure::  ../_static/wind_command_line1.png
   :align:   center

