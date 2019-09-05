Demand data file examples
=======================

The following command will take the data from *Load_forecasts_actuals.csv*,
and launch the simulations with n = 3 and seed = 1234 from forecasts to actuals using an ARMA
Base Process. It will simulate all the dates in the input files. Finally, it will return a
plot of simulations, and create an output dir called "load_data_command_1".

::

    python -m mape_maker "mape_maker/samples/rts_gmlc/Load_forecasts_actuals.csv" -st "actuals" -n 3 -bp "ARMA" -o "load_data_command_1" -s 1234


* **"mape_maker/samples/rts_gmlc/Load_forecasts_actuals.csv"**:
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
* **-o "load_data_command_1"**:
 Create an output directory called "load_data_command_1", in which will store the simulation output file.

After running the command line, you should see a similar plot like this:

.. figure::  ../_static/load_data_command_1.png
   :align:   center