# tSensor

#### Summary

A simple Raspberry Pi temperature sensor located in my room. A python scripts queries the sensor and runs as a  background process. The data is pushed to an external github respository as a javascript [file](https://rawgit.com/mmihira2/tData/data/data.js). The js file when executed by the browser creates a global variable called tData which contains the latest data.

A live demo which displays the data in a nice chart is located [here](https://mmihira.github.io/tSensor).

