Using rts_gmlc data file as input for MapeMaker
===============================================
MapeMaker can be used with rts_gmlc data files found on their github website. The data files need to be
processed into the required 3 columns format - datetime, actuals, and forecasts.
We use "process_RTS_GMLC_data_s.py" file for this.
Here is a step-by-step explanation:

1. Git clone the rts_gmlc data files to your working directory. (The link might be updated, please modify it accordingly)

::

    git clone https://github.com/GridMod/RTS-GMLC.git

2. Now use the process_RTS_GMLC_data_s.py file to process the data in the required format for MapeMaker.
First, cd to the directory with the program:

::

    cd mape_maker/samples/rts_gmlc/

Then, you can run the python script as follows:

::

    python process_RTS_GMLC_data_s.py timeseries_path source_path write_path

where

* **timeseries_path**:
  location of the timeseries_data_files directory (e.g. "RTS-GMLC/RTS_Data/timeseries_data_files/")
* **source_path**:
  location of the SourceData directory (e.g. "RTS-GMLC/RTS_Data/SourceData/")
* **write_path**:
  location of an existing directory you want to store the processed files in (e.g. "my_rts_gmlc")

After running the python script, the write_path will contain all csv and txt files for all the timeseries data files processed by buses, zones, and aggregated together over all the zones.
The csv files can be used as input to MapeMaker to get the desired scenarios.

Here are some examples.

Example 1 - WIND_forecasts_actuals.csv
**************************************

The following command will take the data from *WIND_forecasts_actuals.csv*, and launch the
simulations with n = 5 and seed = 1234 from forecasts to actuals using an IID base process.
It will simulate all the dates in the input files. Finally, it will return a plot of simulations,
and create an output dir called "wind_forecasts_actuals".

::

    python -m mape_maker "test/rts_data/my_rts_gmlc/WIND_forecasts_actuals.csv" -st "actuals" -n 5 -bp "ARMA" -o "wind_forecasts_actuals" -s 1234

* **"test/rts_data/my_rts_gmlc/WIND_forecasts_actuals.csv"**:
 The csv file containing forecasts and actuals for specified datetimes.
* **-st "actuals"**:
 Set up the the target of the simulation as "actuals". So the MapeMaker will simulate the "actuals" data
 according to the "forecasts" data in the input file.
* **-n 5**:
 The number of simulations that we want to create is "5". This will create three simulation columns in the output file.
* **-bp "ARMA"**:
 Use "ARMA" as the base process.
* **-s 1234**:
 Set the seed as "1234", so it won't randomly choose a number as the seed.
* **-o "wind_forecasts_actuals"**:
 Create an output directory called "wind_forecasts_actuals", in which will store the simulation output file.


make sure forecast_error = True
After running the command line, you should see a similar plot like this:

.. figure::  ../_static/rts_wind_command1.png
   :align:   center

Example 2 - Bus_220_Load_zone2_forecasts_actuals.csv
*****************************************************

The following command will take the data from *Bus_220_Load_zone2_forecasts_actuals.csv*,
and launch the simulations with n = 5 and seed = 1234 from forecasts to actuals using an ARMA
base process. It will simulate all the dates in the input files. Finally, it will return a
plot of simulations, and create an output dir called "Bus_220_load".

::

    python -m mape_maker "test/rts_data/prescient_rts_gmlc/timeseries_data_files_noerror/Bus_220_Load_zone2_forecasts_actuals.csv" -st "actuals" -n 5 -bp "ARMA" -is "2020-1-10 1:0:0" -ie "2020-7-20 0:0:0" -sd "2020-6-1 0:0:0" -ed "2020-6-30 23:0:0" -o "Bus_220_load" -s 1234

* **"test/rts_data/prescient_rts_gmlc/timeseries_data_files_noerror/Bus_220_Load_zone2_forecasts_actuals.csv"**:
 The csv file containing forecasts and actuals for specified datetimes.
* **-st "actuals"**:
 Set up the the target of the simulation as "actuals". So the MapeMaker will simulate the "actuals" data
 according to the "forecasts" data in the input file.
* **-n 5**:
 The number of simulations that we want to create is "5". This will create three simulation columns in the output file.
* **-bp "ARMA"**:
 Use "ARMA" as the base process. The default base process is set as "ARMA".
* **-is "2020-1-10 1:0:0"**:
 The start date of the input data for processing is "2020-1-10 1:0:0"
* **-ie "2020-7-20 0:0:0"**:
 The end date of the input data for processing is "2020-7-20 0:0:0"
* **-sd "2020-6-1 0:0:0"**:
 The start date of the scenario simulation is "2020-6-1 0:0:0"
* **-ed "2020-6-30 23:0:0"**:
 The end date of the scenario simulation is "2020-6-1 0:0:0"
* **-s 1234**:
 Set the seed as "1234", so it won't randomly choose a number as the seed.
* **-o "Bus_220_load"**:
 Create an output directory called "Bus_220_load", in which will store the simulation output file.

After running the command line, you should see a similar plot like this:

.. figure::  ../_static/rts_bus_220_load_command1.png
   :align:   center
