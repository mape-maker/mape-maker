Unit Tests
==========

Unittest Examples for Wind and Load
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**CAISO Wind Unittest Examples**

-----------------------------------

**fast_CAISO_wind_tests.py**

* This test will run very fast because it only includes one sample command line.
|
|
**quick_CAISO_wind_tests.py**

* This test is used to check whether some sample command lines will run successfully at once.
|
|
**slow_CAISO_wind_tests.py**

* The difference between CAISO_wind_quick_test.py and CAISO_wind_slow_test.py is that the second one will compare the first simulation column and the second simulation column, then show the differences.
|
|
**Load Unittest Examples**

---------------------------------------------
**fast_load_tests.py**

* This test will run very fast because it only includes one sample command line.
|
|
**load_quick_test.py**

* This test is used to check whether some sample command lines will run successfully at once.
|
|
**load_slow_test.py**

* The difference between load_quick_test.py and load_slow_test.py is that the second one will compare the first simulation column and the second simulation column, then show the differences.
|
|

Unittest Examples for RTS WIND and BUS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**RTS Wind Unittest Examples**

---------------------------------------

**rts_wind_test.py**

* This test is used to see whether the sample command line for RTS Wind example will run successfully.
|
|
**Bus_220_Load_test.py**

* This test is used to see whether the sample command line for Load example will run successfully.
