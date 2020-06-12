.. _Input:

Input
=======
The input of the package is assumed to be a csv giving forecasts and actuals for specified datetimes as a csv file.

Notes about the Input File
**************************

1. If you want to use your own datafile as an input to run the mape_maker, then the input file format should be:

    * **"datetime"** as the first column, formatted as 'Y-M-D H:M:S'.  i.e: 2020-01-01 01:00:00
    * **"forecasts"** data as the second column, format as "float".  i.e: 3264.59
    * **"actuals"** data as the third column, format as "float".  i.e: 3264.59

2. If the forecasts and actuals throughout the dataset are the same numbers up to most of the decimal points, then the software will not run the scenarios. This is the case because then there is little to no relative error, which leads to invalid values for r_tilde.

3. If the input datafile has any missing values, then the program will terminate with a KeyError warning.

Example
**************************

We give an example as the first 10 rows of the csv located under mape_maker/samples/wind_total_forecast_actual_070113_063015.csv.


.. list-table::
   :widths: 25 25 25
   :header-rows: 1

   * - datetimes
     - forecasts
     - actuals
   * - 7/1/13 0:00
     - 2031.94
     - 1947.52095
   * - 7/1/13 1:00
     - 1969.84
     - 2074.72335
   * - 7/1/13 2:00
     - 1902.99
     - 2246.44718
   * - 7/1/13 3:00
     - 1768.13
     - 1978.91344
   * - 7/1/13 4:00
     - 1708.09
     - 1767.39892
   * - 7/1/13 5:00
     - 1656.86
     - 1635.56253
   * - 7/1/13 6:00
     - 1410.82
     - 1160.40714
   * - 7/1/13 7:00
     - 966.72
     - 489.04769
   * - 7/1/13 8:00
     - 665.22
     - 224.73994
   * - 7/1/13 9:00
     - 406.82
     - 196.72952
|
|
