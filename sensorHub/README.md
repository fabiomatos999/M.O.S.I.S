# Sensor Hub library Usage

#### This library is an abstraction of the TIs MCU TM4C1294XL that is connected to the raspberry pi. This library serves as an interface. The methods implemented in this library will trigger  the functions programmed in the MCU.

## Creating sensorHub object 
```py
# Once in the sensorHub directory import library; Depending on implementation might have to change import statement
import sensor 
sensor = sensor.sensorHub()
```

## Calibrating sensorHub
Before using the sensor hub in the field, we must ensure  all the sensors are properly calibrated. You can use the calibrate methods of the sensorHub object 

```py
#calibrates all sensors 
sensor.calibrateAll()

#Alternatively we can calibrate each sensor in isolation by doing each function call independently
sensor.PhHighCal()
sensor.PhMidCal()
sensor.PhLowCal()

sensor.DoAtmoCal()
sensor.DoZeroCal()
```


## Example of Read Method 

The most important method of the sensorHub class is the Read() method. This method outputs all the sensor meta data and is returned in the form of a ReadResult object. This ReadResult object has get methods for each of the sensors data.

```py

metaData: ReadResult = sensor.Read()

ph = metaData.getPh()
temp = metaData.getTemp()
do = metaData.getDO()
pressure = metaData.getPressure()
```
## Sensor Hub Status

To check each sensor is working properly we can call a system check method that will return the status of all the sensors. The return format is an object of class SensorHubStatus. This class has boolean methods that tell us if a sensor is working or 

```py
sensorsStatus: SensorHubStatus = sensor.SysCheck()

phWorking = sensorsStatus.isPhWorking()
tempWorking = sensorsStatus.isTempWorking()
doWorking = sensorsStatus.isDOWorking()
baroWorking = sensorsStatus.isBaroWorking()

print(f" Ph sensor is working = {phWorking}")
print(f" thermometer sensor is working = {tempWorking}")
print(f" DO sensor is working = {doWorking}")
print(f" barometer sensor is working = {baroWorking}")
```

