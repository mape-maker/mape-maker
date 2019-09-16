Infeasible_example
===================

For any requested MAPE, the distributions of errors computed should be as close as possible to the original
error distributions while satisfying the target MAPE. During the process, we compute the mean absolute error of
a beta distribution with fixed alpha and beta to hit the target MAPE so that it keeps the same parameters as the
original distribution.
If it's hard to meet the target MAPE, then it will throw
the error, saying that it's infeasible to meet the target MAPE.

Example 1
^^^^^^^^^^

::

python -m mape_maker "mape_maker/samples/wind_total_forecast_actual_070113_063015.csv" -st "actuals" -n 5 -bp "ARMA" -o "wind_actuals_ARMA_1" -is "2014-6-1 00:00:00" -ie "2014-6-30 00:00:00" -sd "2014-6-27 01:00:00" -ed "2014-6-29 00:00:00" -s 1234


This command line will fail with an error because the simulation date range is too small, which will cause the error become very big. Therefore, it's infeasible to meet the target mape.
.. note:: If the user set the date range greater than a month, then the command line will run successfully without giving an error.

::

python -m mape_maker "mape_maker/samples/wind_total_forecast_actual_070113_063015.csv" -st "actuals" -n 5 -bp "ARMA" -o "wind_actuals_ARMA_1" -is "2014-6-1 00:00:00" -ie "2014-6-30 00:00:00" -sd "2014-6-27 01:00:00" -ed "2014-6-29 00:00:00" -s 1234