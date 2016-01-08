# tSensor

#### Summary

A simple rasberryPi temperature sensor located in my room. A python scripts runs as a background process query the sensor and uploading data. The data is pushed to an external git respository as a javascript file. Any website can access the data by placing linking to the js file. The js file when executed by the browser creates a global variable called tData which contains the latest data.

A live demo which displays the data in a nice chart is located [here](https://mmihira.github.io/tSensor).

