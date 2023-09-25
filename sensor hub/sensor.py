import serial
from time import sleep


class ReadResult:
    def __init__(self, parsedSensorHubResponse: list[str]):
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

    def tempReading(self) -> float:
        """
        Get temperature reading from sensor hub message

        Returns:
            float: temperature reading in Celcius from sensor hub
        """
        return self.tempReading

    def getDOreading(self) -> float:
        """
        Get Dissolved Oxygen reading from sensor hub message

        Returns:
            float: Dissolved Oxygen (0-100)
        """
        return self.DOreading

    def getBaroReading(self) -> float:
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
        self.uart = serial.Serial("/dev/ttyS0", baudrate=115200)

        print("created sensor hub object")

    def Read(self) -> ReadResult:
        """
        Reads all sensor data
        returns =ReadResult object with all sensor readings



        TODO:
            -determine units of all readings
            -determine length of incoming byte read after encode
            -include timeout of function if no result is returned or throw error
        """

        # sends command to MCU through UART port to fetch all sensor readings
        command = r"\rRead"
        self.uart.write(command)

        # read result from command
        received = self.uart.read(size=24)
        data_left = self.uart.inWaiting()  # check for remaining byte
        received += self.uart.read(data_left)

        # debug this value
        received = received.decode(encoding="utf-8")
        # parse the string and store values in result variable
        parsed = received.split(sep="&")

        result = ReadResult(parsed)

        return result

    def PhCal(self) -> float:
        """
        sends command to MCU to get Ph readings readings every second
        returns the first response but the MCU will continue to transmit
        """

        command = r"\rPhCal"
        self.uart.write(command)

        # read result from command
        received = self.uart.read()
        # debug this value
        received = received.decode(encoding="utf-8")
        print(received)

        return received

    def PhMidCal(self):
        """
        Performs mid point calibration of Ph sensor
        """

        command = r"\rPhMidCal"
        self.uart.write(command)

        # read result from command
        received = self.uart.read()
        # debug this value
        received = received.decode(encoding="utf-8")
        print(f" PhMidCal : {received}")

    def PhLowCal(self):
        """
        Performs low point callibration of ph sensor
        """

        command = r"\rPhLowCal"
        self.uart.write(command)

        # read result from command
        received = self.uart.read()

        print(f"PhLowCal: {received}")

    def PhHighCal(self):
        """
        Performs high point callibration of ph sensor
        """
        command = r"\rPhHighCal"
        self.uart.write(command)

        # read result from command
        received = self.uart.read()
        # debug this value
        received = received.decode(encoding="utf-8")
        print(f" PhHighCal:  {received}")

    def DoCal(self) -> float:
        """
        Get D.O readings every second
        returns first DO reading but the MCU will continue to transmit readings
        every second
        """
        command = r"\DoCal"
        self.uart.write(command)

        # read result from command
        received = self.uart.read()
        # debug this value
        received = received.decode(encoding="utf-8")
        print(f" DoCal: {received}")

        return received

    def DoAtmoCal(self):
        """
        Calibrate to atmospheric oxygen content

        """
        command = r"\rDoAtmoCal"
        self.uart.write(command)

        # read result from command
        received = self.uart.read()
        # debug this value
        received = received.decode(encoding="utf-8")
        print(f"DoAtmoCal: {received}")

    def DoZeroCal(self):
        """
        Calibrate to zero oxygen content

        """
        command = r"\rDoZeroCal"
        self.uart.write(command)

        # read result from command
        received = self.uart.read()
        # debug this value
        received = received.decode(encoding="utf-8")
        print(f"DoZeroCal: {received}")

    def TempCal(self) -> float:
        """
        Fetches temperature reading every second
        Returns only first reading but MCU will continue to transmit

        """

        command = r"\rTempCal"
        self.uart.write(command)

        # read result from command
        received = self.uart.read()
        # debug this value
        received = received.decode(encoding="utf-8")
        print(f"TempCal: {received}")

        return received

    def TempNewCal(self):
        """
        Calibrates sensor using a specific temp value
        """
        command = r"\rDoAtmoCal"
        self.uart.write(command)

        # read result from command
        received = self.uart.read()
        # debug this value
        received = received.decode(encoding="utf-8")
        print(f"TempNewCal: {received}")

    def exit(self):
        """
        Manually exit from calibration process
        """
        command = r"\rexit"
        self.uart.write(command)
