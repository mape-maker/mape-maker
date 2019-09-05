Operational Example
===================

The following command will take the data from *caiso_wind_forecast_missing_actual.csv*,
and can be used to find the simulation from forecasts to actuals for the date(s) that do not have actuals.

It will simulate all the dates in the input files, and can use the date(s) with missing actuals for simulation dates.
In order to fit the process well, we need to simulate for a few additional hours before the day
we are interested in as the ARMA process can be a little imprecise for the first few hours.
For convenience/efficiency, we will add the preceding day to the desired simulation start date.
Here, for example, we are interested in 2015-6-30, but we will use 2015-6-29 as the simulation start date.
Finally, it will return a plot of simulations, and create an output dir called "operations_example".

::

    python -m mape_maker "mape_maker/samples/operations_example.csv" -st "actuals" -n 3 -bp "ARMA" -is "2013-7-1 00:00:00" -ie "2014-2-14 23:00:00" -sd "2014-2-15 00:00:00" -ed "2014-2-16 23:00:00" -o "operations_example" -s 1234

* **"mape_maker/samples/rts_gmlc/Load_forecasts_actuals.csv"**:
 The csv file containing forecasts and actuals for specified datetimes.
* **-st "actuals"**:
 Set up the the target of the simulation as "actuals". So the MapeMaker will simulate the "actuals" data
 according to the "forecasts" data in the input file.
* **-n 3**:
 The number of simulations that we want to create is "3". This will create three simulation columns in the output file.
* **-bp "ARMA"**:
 Use "ARMA" as the base process. The default base process is set as "ARMA".
* **-is "2013-7-1 00:00:00"**:
 The start date for the computation of the distributions is "2013-7-1 00:00:00"
* **-ie "2014-2-14 23:00:00"**:
 The end date for the computation of the distributions is "2014-2-14 23:00:00"
* **-sd "2014-2-15 00:00:00"**:
 The start date of the simulation is "2014-2-15 00:00:00"
* **-ed "2014-2-16 23:00:00"**:
 The end date of the simulation is ""2014-2-16 23:00:00"
* **-o "operations_example"**:
 Create an output directory called "operations_example", in which will store the simulation output file.
* **-s 1234**:
 Set the seed as "1234", so it won't randomly choose a number as the seed.

After running the command line, you should see a similar plot like this:

.. figure::  ../_static/operations_example.png
   :align:   center