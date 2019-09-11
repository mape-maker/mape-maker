Infeasible_example
===================

Example
^^^^^^^

Sometimes when the user may receive an error showing "
This command line will fail with an error because the simulation date range is too small, which will cause the error become very big. Therefore, it's infeasible to meet the target mape.
.. note:: If the user set the date range greater than a month, then the command line will run successfully without giving an error.

::

python -m mape_maker "mape_maker/samples/wind_total_forecast_actual_070113_063015.csv" -st "actuals" -n 5 -bp "ARMA" -o "wind_actuals_ARMA_1" -is "2014-6-1 00:00:00" -ie "2014-6-30 00:00:00" -sd "2014-6-27 01:00:00" -ed "2014-6-29 00:00:00" -s 1234