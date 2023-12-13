import AtlasI2C
import AtlasOEM_RTD
import AtlasOEM_DO
import ms5837


class SensorHub:

    def __init__(self):
        self.pHSensor = AtlasI2C.AtlasI2C(address=0x63, bus=1)
        self.temperatureSensor = AtlasOEM_RTD.AtlasOEM_RTD(address=0x68, bus=1)
        self.dissolvedOxygenSensor = AtlasOEM_DO.AtlasOEM_DO(address=0x67,
                                                             bus=1)
        self.pressureSensor = ms5837.MS5837(model=ms5837.MODEL_30BA, bus=1)
        self.pressureSensor.init()
        self.pressureSensor.setFluidDensity(ms5837.DENSITY_SALTWATER)

    def getTemperature(self) -> float:
        return float(self.temperatureSensor.read_RTD_reading())

    def temperatureCal(self, temp: float):
        self.temperatureSensor.write_calibration_data(temp*1000)
        return self.temperatureSensor.write_calibration_request(2)

    def temperatureClearCal(self):
        return self.temperatureSensor.write_calibration_request(1)

    def getpH(self) -> float:
        return float(self.pHSensor.query("R").split(" ")[-1][:5])

    def pHLowCal(self) -> str:
        return self.pHSensor.query("Cal,low,4.00")

    def pHMidCal(self) -> str:
        return self.pHSensor.query("Cal,mid,7.00")

    def pHighCal(self) -> str:
        return self.pHSensor.query("Cal,high,10.00")

    def pHClearCal(self) -> str:
        return self.pHSensor.query("Cal,clear")

    def getDissolvedOxygen(self):
        return float(self.dissolvedOxygenSensor.read_DO_reading())

    def dissolvedOxygenAtmophericCalibration(self):
        return self.dissolvedOxygenSensor.write_calibration_request(2)

    def dissolvedOxygenZeroCalibration(self):
        return self.dissolvedOxygenSensor.write_calibration_request(3)

    def dissolvedOxygenClearCalibration(self):
        return self.dissolvedOxygenSensor.write_calibration_request(1)

    def getPressure(self):
        self.pressureSensor.read()
        return float(self.pressureSensor.pressure())
