Processing RTS-GMLC data using threshold
========================================

Modifying data to change forecasts values where relative error

	RE = abs((actuals-forecasts)/forcasts)

Is greater than a specified threshold.
We modify the forecast value so that the re becomes equal to the threshold.