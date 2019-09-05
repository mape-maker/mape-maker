Sukhman
#######
to do:

Y check the f+last row, last col
S func outputs f+last number of the file

1. check the first and last number with saved values SAME
2. run twice with seed and check the first and last values SAME
3. run test twice without seed and check if the first and last values DIFF
4. check dates, raise error before calling mape
    simulation_start_dt has to be after input_start_dt
    not both dates, raise good error check
    sim before input, raise good error

better
missing value error


operational:



Document flow chart

- FOR LATER: utility help fill in missing data*
- pickle the conditional dis and ARMA para


BACKUP
******

**sample command 2:**

---------------------------------------------
The following command will take the data from *Load_forecasts_actuals.csv*,
and launch the simulations with with n = 3, target mape = ?, and seed = 1234 from actuals to forecasts
using an ARMA Base Process. It will simulate from 2020-6-1 to 2020-6-30. Finally, it will return a
plot of simulations, and create an output dir called "load_data_command_2".

::

    python mape_maker "mape_maker/samples/rts_gmlc/Load_forecasts_actuals.csv" -st "forecasts" -n 3 -bp "ARMA" -is "2020-6-10 1:0:0" -is "2020-6-20 0:0:0 -sd "2020-6-1 1:0:0" -ed "2020-6-30 23:0:0" -o "load_data_command_2" -s 1234
This command will first call the __main__.py, which will create a MapeMaker class and
call the simulate function. You should see a plot similar to this:

* **"mape_maker/samples/rts_gmlc/Load_forecasts_actuals.csv"**:
 The csv file containing forecasts and actuals for specified datetimes.
* **-st "forecasts"**:
 Set up the the target of the simulation as "forecasts". So the MapeMaker will simulate the "forecasts" data
 according to the "actuals" data in the input file.
* **-n 3**:
 The number of simulations that we want to create is "3". This will create three simulation columns in the output file.
* **-bp "ARMA"**:
 Use "ARMA" as the base process. The default base process is set as "ARMA".
* **-sd "2020-6-1"**:
 The start date of the simulation is "2020-6-1"
* **-ed "2020-6-30"**:
 The end date of the simulation is "2020-6-30"
* **-t**:
 (find mape)
* **-s 1234**:
 Set the seed as "1234", so it won't randomly choose a number as the seed.
* **-o "load_data_command_2"**:
 Create an output directory called "load_data_command_2", in which will store the simulation output file.

After running the command line, you should see a similar plot like this:

Additional examples
--------------------

sample command 3:
+++++++++++++++++

The following command will take the data from *Load_forecasts_actuals.csv*,
and launch the simulations with n = 3 and seed = 1234 from forecasts to actuals using an ARMA
Base Process. It will simulate all the dates in the input files. Finally, it will return a
plot of simulations, and create an output dir called "load_data_command_3".

::

    python -m mape_maker "mape_maker/samples/rts_gmlc/Load_forecasts_actuals.csv" -st "actuals" -n 3 -bp "ARMA" -o "load_data_command_3" -s 1234

This command will first call the __main__.py, which will create a MapeMaker class and
call the simulate function. You should see a plot similar to this:

* **"mape_maker/samples/rts_gmlc/Load_forecasts_actuals.csv"**:
 The csv file containing forecasts and actuals for specified datetimes.
* **-st "actuals"**:
 Set up the the target of the simulation as "actuals". So the MapeMaker will simulate the "actuals" data
 according to the "forecasts" data in the input file.
* **-n 3**:
 The number of simulations that we want to create is "3". This will create three simulation columns in the output file.
* **-bp "ARMA"**:
 Use "ARMA" as the base process, which is also the default base process.
* **-s 1234**:
 Set the seed as "1234", so it won't randomly choose a number as the seed.
* **-o "load_data_command_3"**:
 Create an output directory called "load_data_command_3", in which will store the simulation output file.

After running the command line, you should see a similar plot like this:


sample command 4:
+++++++++++++++++

The following command will take the data from *Load_forecasts_actuals.csv*,
and launch the simulations with n = 3, target mape = ?, and seed = 1234 from actuals to forecasts using an IID
Base Process. It will simulate from 2014-6-1 to 2014-6-30. Finally, it will return a
plot of simulations, and create an output dir called "load_data_command_4".

::

    python -m mape_maker "mape_maker/samples/rts_gmlc/Load_forecasts_actuals.csv" -st "forecasts" -n 3 -bp "iid" -is "2020-6-10 1:0:0" -is "2020-6-20 0:0:0 -sd "2020-6-1 1:0:0" -ed "2020-6-30 23:0:0" -o "load_data_command_4" -s 1234

This command will first call the __main__.py, which will create a MapeMaker class and
call the simulate function. You should see a plot similar to this:

* **"mape_maker/samples/rts_gmlc/Load_forecasts_actuals.csv"**:
 The csv file containing forecasts and actuals for specified datetimes.
* **-st "forecasts"**:
 Set up the the target of the simulation as "forecasts". So the MapeMaker will simulate the "forecasts" data
 according to the "actuals" data in the input file.
* **-n 3**:
 The number of simulations that we want to create is "3". This will create three simulation columns in the output file.
* **-bp "iid"**:
 Use "iid" as the base process. The default base process is set as "ARMA".
* **-sd "2020-6-1"**:
 The start date of the simulation is "2020-6-1"
* **-ed "2020-6-30"**:
 The end date of the simulation is "2020-6-30"
* **-t**:
 (find mape)
* **-s 1234**:
 Set the seed as "1234", so it won't randomly choose a number as the seed.
* **-o "load_data_command_4"**:
 Create an output directory called "load_data_command_4", in which will store the simulation output file.

After running the command line, you should see a similar plot like this: