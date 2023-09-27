import serial
from time import sleep


class ReadResult:
    """
    class for handling readings from sensorHub.Read()
    parses the incoming message string
    """

    def __init__(self, incomingMessage: str):
        """
        Handles return result from sensorHub.Read()
        Args:
            incomingMessage (str): incoming decoded string message from sensor hub
        Attributes:
            phReading (float): ph Reading from sensor hub
            tempReading (float): temp reading from sensor hub
            DOreading (float): Dissolved Oxygen reading from sensor hub
            baroReading (float): Baro reading from sensor hub
        Methods:
            Get methodss for all attributes of the reading and __repr__ to facilitate tesing
        """
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


class sensorHub:
    """This class is an abstraction of the TIs MCU TM4C1294XL
    that is connected to the raspberry pi. This class serves as
    an interface. The methods implemented in this class will trigger
    the functions programmed in the MCU.
    """

    # reference attribute
    _UARTPort = 14
    uart = None

    def __init__(self):
        try:
            self.uart = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=8)
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
            command = r"\rRead".encode()
            self.uart.write(command)

            # read result from command
            received = self.uart.read(size=24)
            data_left = self.uart.inWaiting()  # check for remaining bytes
            received += self.uart.read(data_left)

            received = received.decode(encoding="utf-8")
            result = ReadResult(received)
            print(result)
            return result
        except (serial.SerialException, UnicodeDecodeError) as e:
            raise Exception("Error reading sensor data: " + str(e))

    def getPh(self) -> float:
        """
        sends command to MCU to get Ph readings readings every second
        returns the first response but the MCU will continue to transmit
        """

        try:
            command = r"\rPhCal".encode()
            self.uart.write(command)

            received = self.uart.read(size=8).decode(encoding="utf-8")
            print(f"Ph readings: {received}")
            return float(received)

        except (serial.SerialException, UnicodeDecodeError) as e:
            raise Exception("Error obtaining ph reading from sensor: " + str(e))

    def PhLowCal(self):
        """
        Performs low point callibration of ph sensor
        TODO: determine return value type
        """

        try:
            command = r"\rPhLowCal".encode()
            self.uart.write(command)

            received = self.uart.read(size=8).decode(encoding="utf-8")
            print(f" PhLowCal : {received}")
            return received
        except (serial.SerialException, UnicodeDecodeError) as e:
            raise Exception("Error performing Ph lowpoint calibration: " + str(e))

    def PhMidCal(self):
        """
        Performs mid point calibration of Ph sensor
        TODO: determine return value type
        """
        try:
            command = r"\rPhMidCal".encode()
            self.uart.write(command)

            # read result from command
            received = self.uart.read(size=8)
            # debug this value
            received = received.decode(encoding="utf-8")
            print(f" PhMidCal : {received}")
            return received

        except (serial.SerialException, UnicodeDecodeError) as e:
            raise Exception("Error performing Ph MidPoint calibration: " + str(e))

    def PhHighCal(self):
        """
        Performs high point callibration of ph sensor
        TODO: determine return value type
        """
        try:
            command = r"\rPhHighCal".encode()
            self.uart.write(command)

            # read result from command
            received = self.uart.read(size=8)
            # debug this value
            received = received.decode(encoding="utf-8")
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
            command = r"\rDoCal".encode()
            self.uart.write(command)

            # read result from command
            received = self.uart.read(size=8)
            # debug this value
            received = received.decode(encoding="utf-8")
            print(f" Dissolved Oxygen: {received}")

            return float(received)
        except (serial.SerialException, UnicodeDecodeError) as e:
            raise Exception("Error getting Dissolved Oxygen Reading: " + str(e))

    def DoAtmoCal(self):
        """
        Calibrate Dissolved Oxygen Sensor to atmospheric oxygen content
        TODO: determine return value type
        """
        try:
            command = r"\rDoAtmoCal".encode()
            self.uart.write(command)

            # read result from command
            received = self.uart.read(size=8)
            # debug this value
            received = received.decode(encoding="utf-8")
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
            command = r"\rDoZeroCal".encode()
            self.uart.write(command)

            # read result from command
            received = self.uart.read(size=8)
            # debug this value
            received = received.decode(encoding="utf-8")
            print(f"DoZeroCal: {received}")
            return received
        except (serial.SerialException, UnicodeDecodeError) as e:
            raise Exception(
                "Error performing Dissolved Oxygen sensor to zero oxygen content calibration: "
                + str(e)
            )

    def getTemp(self) -> float:
        """
        Fetches temperature reading every second
        Returns only first reading but MCU will continue to transmit
        """
        try:
            command = r"\rTempCal".encode()
            self.uart.write(command)

            # read result from command
            received = self.uart.read(size=8)
            # debug this value
            received = received.decode(encoding="utf-8")
            print(f"TempCal: {received}")

            return received
        except (serial.SerialException, UnicodeDecodeError) as e:
            raise Exception("Error getting Temperature Reading: " + str(e))

    def TempNewCal(self):
        """
        Calibrates sensor using a specific temp value
        TODO: determine return value type
        """
        try:
            command = r"\rDoAtmoCal".encode()
            self.uart.write(command)

            # read result from command
            received = self.uart.read(size=8)
            # debug this value
            received = received.decode(encoding="utf-8")
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
            command = r"\rexit".encode()
            self.uart.write(command)
        except serial.SerialException as e:
            raise Exception("Error exiting callibration: " + str(e))
