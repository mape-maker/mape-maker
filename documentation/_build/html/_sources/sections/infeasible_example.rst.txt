Infeasible_example
===================

For any requested MAPE, the distributions of errors computed should be close enough to the input
error distributions while meeting the target MAPE. During the process, we compute the mean absolute error of
a conditional beta distribution with fixed alpha and beta to satisfy the target MAPE so that it keeps the same shape
parameters(denoted by alpha and beta) as the original distribution. If it's hard to meet the target MAPE, then it
will throw the error, saying that it's infeasible to meet the target MAPE.

Example 1
^^^^^^^^^^

::

    python -m mape_maker -xf "mape_maker/samples/wind_total_forecast_actual_070113_063015.csv" -f "actuals" -n 5 -bp "ARMA" -ss "2014-6-17 01:00:00" -se "2014-6-30 00:00:00" -s 1234

This command line will fail with an error, showing the following output:

::

    RuntimeError:  < 1, there is a prevalence of high power input in the SID
    The requested r_tilde is too high
         => Either change your requested mape to be less than 21.473508488457284
         => Or change your SID so the e_score increases



The plausibility score should be close to 1, meaning that the error distribution for the set is close to the empirical distribution of errors.
In this example, we can see that the maximum mare is less than the target mare.
In order to make the program run successfully, the user can either change the target mape or adjust the input dataset.


Example 2
^^^^^^^^^^

::

    python -m mape_maker -xf "mape_maker/samples/wind_total_forecast_actual_070113_063015.csv" -f "actuals" -n 5 -bp "ARMA" -o "wind_actuals_ARMA_1" -is "2014-6-1 00:00:00" -ie "2014-6-30 00:00:00" -ss "2014-6-15 01:00:00" -se "2014-6-29 00:00:00" -s 1234

This command line will fail with an error, showing the following output during the running process:
******* WARNING!! **********
 beta rvs failed at i=684,x=3314.9; a=-0.05177452493780477, b=-0.3897512549813409, l_=-292.78035, s_=359.6603500000001
 Using last good beta parameters.

This error occurs when the program is trying to estimate the maximum target mean absolute error function(called as m_max).
It fails because the shape parameters(alpha and beta) are negative values.
.. note:: If there have not been any good beta parameters, the program will terminate, but otherwise, it will continue.




