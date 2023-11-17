import serial
from time import sleep


class ReadResult:
    """
    class for handling readings from sensorHub.readline()
    parses the incoming message string
    """

    def __init__(self, incomingMessage: str):
        """
        Handles return result from sensorHub.readline()
        Args:
            incomingMessage (str): incoming decoded string message from sensor hub
        Attributes:
            phReading (float): ph Reading from sensor hub
            tempReading (float): temp reading from sensor hub
            DOreading (float): Dissolved Oxygen reading from sensor hub
            baroReading (float): Baro reading from sensor hub
        Methods:
            Get methods for all attributes of the reading and __repr__ to facilitate tesing
        """
        incomingMessage = incomingMessage.strip()
        parsedSensorHubResponse = incomingMessage.split(sep="&")
        print(f" incoming message: {parsedSensorHubResponse}")
        self.phReading = float(parsedSensorHubResponse[0])
        self.tempReading = float(parsedSensorHubResponse[1])
        self.DOreading = float(parsedSensorHubResponse[2])
        self.baroReading = float(parsedSensorHubResponse[3])

    def __repr__(self) -> str:
        return f"""
        Reading Result:
        
        Ph: {self.phReading} 
        Temperature : {self.tempReading} celcius
        Dissolved Oxygen: {self.DOreading}
        Pressure (barometric sensor): {self.baroReading} mbar"""

    def getPh(self) -> float:
        """
        Get Ph reading from sensor result message

        Returns:
            float: Ph level measured by hub
        """
        return self.phReading

    def getTemp(self) -> float:
        """
        Get temperature reading from sensor hub message

        Returns:
            float: temperature reading in Celcius from sensor hub
        """
        return self.tempReading

    def getDO(self) -> float:
        """
        Get Dissolved Oxygen reading from sensor hub message

        Returns:
            float: Dissolved Oxygen (0-100)
        """
        return self.DOreading

    def getPressure(self) -> float:
        """
        Get Barometric Reading from sensor hub message

        Returns:
            float: barometric reading in mbars
        """
        return self.baroReading


class SensorHubStatus:
    """
    Captures incoming bit sequence from SysCheck command.

    bit sequence breakdown:

    1 represents it works and 0 represents its faulty.
    bit sequence [abcd]:

        a = pH sensor
        b = Thermometer
        c = Dissolved oxygen sensor
        d = Barometer

    This class checks these values using bitwise masking technique
    """

    def __init__(self, incomingBin: bytes) -> None:
        self.statusCode = int(incomingBin.decode("ascii").strip(), 2)

    def isPhWorking(self) -> bool:
        """
        Checks if Ph sensor is returning valid values

        Returns:
            bool: True if working False if not working
        """
        return (self.statusCode & 0b1000) == 0b1000

    def isTempWorking(self) -> bool:
        """
        Checks if Thermotmeter is returning valid values

        Returns:
            bool: True if working False if not working
        """
        return (self.statusCode & 0b0100) == 0b0100

    def isDOWorking(self) -> bool:
        """
        Checks if Dissolved Oxygen Sensor is returning valid values

        Returns:
            bool: True if working False if not working
        """
        return (self.statusCode & 0b0010) == 0b0010

    def isBaroWorking(self) -> bool:
        """
        Checks if Barometer is returning valid values

        Returns:
            bool: True if working False if not working
        """
        return (self.statusCode & 0b0001) == 0b0001


class sensorHub:
    """This class is an abstraction of the TIs MCU TM4C1294XL
    that is connected to the raspberry pi. This class serves as
    an interface. The methods implemented in this class will trigger
    the functions programmed in the MCU.
    """

    # reference attribute
    _UARTPort = "/dev/ttyS0"
    channel = None
    encoding = "ascii"
    decoding = "ascii"

    def __init__(self):
        try:
            self.channel = serial.Serial(self._UARTPort, baudrate=9600, timeout=8)
            print(self.channel)
        except serial.SerialException as e:
            raise Exception("Error opening serial port: " + str(e))

    def Read(self) -> ReadResult:
        """
        Reads all sensor data from hub

        Raises:
            Exception: if error obtaining sensor data

        Returns:
            result (ReadResult): ReadResult object with sensor data as attributes

        TODO:
            -determine units of all readings
            -determine length of incoming byte read after encode
            -include timeout of function if no result is returned or throw error
        """

        # sends command to MCU through UART port to fetch all sensor readings
        try:
            # sends command to MCU through UART port to fetch all sensor readings
            command = "read".encode(encoding=self.encoding)
            self.channel.write(command)

            # read result from command
            received = self.channel.read(size=24)
            data_left = self.channel.inWaiting()  # check for remaining bytes
            received += self.channel.read(data_left)

            received = received.decode(encoding=self.decoding)
            result = ReadResult(received)
            print(result)
            return result
        except (serial.SerialException, UnicodeDecodeError) as e:
            raise Exception("Error reading sensor data: " + str(e))

    def SysCheck(self) -> SensorHubStatus:
        try:
            command = "SysCheck".encode(encoding=self.encoding)
            self.channel.write(command)

            received = self.channel.read(size=4)
            result = SensorHubStatus(received)
            return result

        except (serial.SerialException, UnicodeDecodeError) as e:
            raise Exception("Error obtaining information  from sensor: " + str(e))

    def getPh(self) -> float:
        """
        sends command to MCU to get Ph readings readings every second
        returns the first response but the MCU will continue to transmit
        """

        try:
            command = "PhCal".encode(encoding=self.encoding)
            self.channel.write(command)

            received = self.channel.read(size=8).decode(encoding=self.decoding)
            print(f"Ph readings: {received}")
            return float(received)

        except (serial.SerialException, UnicodeDecodeError) as e:
            raise Exception("Error obtaining ph reading from sensor: " + str(e))

    def PhLowCal(self) -> float:
        """
        Performs low point callibration of ph sensor
        TODO: determine return value type
        """

        try:
            command = "PhLowCal".encode(encoding=self.encoding)
            self.channel.write(command)

            received = self.channel.read(size=8).decode(encoding=self.decoding)
            print(f" PhLowCal : {received}")
            return float(received)
        except (serial.SerialException, UnicodeDecodeError) as e:
            raise Exception("Error performing Ph lowpoint calibration: " + str(e))

    def PhMidCal(self) -> float:
        """
        Performs mid point calibration of Ph sensor
        """
        try:
            command = "PhMidCal".encode(encoding=self.encoding)
            self.channel.write(command)

            # read result from command
            received = self.channel.read(size=8)
            # debug this value
            received = received.decode(encoding=self.decoding)
            print(f" PhMidCal : {received}")
            return float(received)

        except (serial.SerialException, UnicodeDecodeError) as e:
            raise Exception("Error performing Ph MidPoint calibration: " + str(e))

    def PhHighCal(self):
        """
        Performs high point callibration of ph sensor
        """
        try:
            command = "PhHighCal".encode(encoding=self.encoding)
            self.channel.write(command)

            # read result from command
            received = self.channel.read(size=8)
            # debug this value
            received = received.decode(encoding=self.decoding)
            print(f" PhHighCal:  {received}")
            return received
        except (serial.SerialException, UnicodeDecodeError) as e:
            raise Exception("Error performing Ph Highpoint calibration: " + str(e))

    def getDO(self) -> float:
        """
        Get D.O readings every second
        returns first DO reading but the MCU will continue to transmit readings
        every second

        """
        try:
            command = "DoCal".encode(encoding=self.encoding)
            self.channel.write(command)

            # read result from command
            received = self.channel.read(size=8)
            # debug this value
            received = received.decode(encoding=self.decoding)
            print(f" Dissolved Oxygen: {received}")

            return float(received)
        except (serial.SerialException, UnicodeDecodeError) as e:
            raise Exception("Error getting Dissolved Oxygen Reading: " + str(e))

    def DoAtmoCal(self):
        """
        Calibrate # The `Dissolved Oxygen` function in the `sensorHub` class is used to obtain the
        # dissolved oxygen reading from the sensor hub. It sends a command to the MCU to get
        # the dissolved oxygen readings, and then returns the first response received. The
        # MCU will continue to transmit readings every second, but this function only
        # returns the first reading.
        Dissolved Oxygen Sensor to atmospheric oxygen content
        TODO: determine return value type
        """
        try:
            command = "DoAtmoCal".encode(encoding=self.encoding)
            self.channel.write(command)

            # read result from command
            received = self.channel.read(size=8)
            # debug this value
            received = received.decode(encoding=self.decoding)
            print(f"DoAtmoCal: {received}")
        except (serial.SerialException, UnicodeDecodeError) as e:
            raise Exception(
                "Error performing Dissolved Oxygen to atmespheric oxygen calibration: "
                + str(e)
            )

    def DoZeroCal(self):
        """
        Calibrate Dissolved Oxygen to zero oxygen content
        TODO: determine return value type
        """
        try:
            command = "DoZeroCal".encode(encoding=self.encoding)
            self.channel.write(command)

            # read result from command
            received = self.channel.read(size=8)
            # debug this value
            received = received.decode(encoding=self.decoding)
            print(f"DoZeroCal: {received}")
            return received
        except (serial.SerialException, UnicodeDecodeError) as e:
            raise Exception(
                "Error performing Dissolved Oxygen sensor to zero oxygen content calibration: "
                + str(e)
            )

    def DoCalClear(self):
        """

        Clears calibration values from Dissolved Oxygen Sensor

        Raises:
            Exception: catches serial exception error from UART port
        """
        try:
            command = "clear".encode(encoding=self.encoding)
            self.channel.write(command)

        except serial.SerialException as e:
            raise Exception("Error clearing DO calibration: " + str(e))

    def getTemp(self) -> float:
        """
        Fetches temperature reading every second
        Returns only first reading but MCU will continue to transmit
        """
        try:
            command = "TempCal".encode(encoding=self.encoding)
            self.channel.write(command)

            # read result from command
            received = self.channel.read(size=8)
            # debug this value
            received = received.decode(encoding=self.decoding)
            print(f"TempCal: {received}")

            return float(received)
        except (serial.SerialException, UnicodeDecodeError) as e:
            raise Exception("Error getting Temperature Reading: " + str(e))

    def TempNewCal(self):
        """
        Calibrates sensor using a specific temp value
        TODO: determine return value type
        """
        try:
            command = "DoAtmoCal".encode(encoding=self.encoding)
            self.channel.write(command)

            # read result from command
            received = self.channel.read(size=8)
            # debug this value
            received = received.decode(encoding=self.decoding)
            print(f"TempNewCal: {received}")

            return received
        except (serial.SerialException, UnicodeDecodeError) as e:
            raise Exception(
                "Error callibrating temperature sensor with specific temp value: "
                + str(e)
            )

    def calibrateAll(self):
        """
        Calibrate all of the sensors
        to be used in the constructor if functions all work properly
        """
        self.PhHighCal()
        self.PhMidCal()
        self.PhLowCal()

        self.DoAtmoCal()
        self.DoZeroCal()

    def exit(self):
        """
        Manually exit from calibration process
        """

        try:
            command = "exit".encode(encoding=self.encoding)
            self.channel.write(command)
        except serial.SerialException as e:
            raise Exception("Error exiting calibration: " + str(e))
