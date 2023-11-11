"""Random sensor data generation module."""
from DataClass import MediaEntry, MediaMetadata
import random
from SensorParsing import SensorString


class RandomEntry:
    """Wrapper class for RandomEntry module."""

    @staticmethod
    def random_sensor_string() -> str:
        """Create random sensor string as if it was received from sensorHub."""
        # Creates the pH sensor String with a format of X.XXX where X
        # is a random digit
        ph_sensor_decimal = random.randint(0, 9)
        ph_sensor_hundred = random.randint(100, 999)
        ph_sensor = f"{ph_sensor_decimal}.{ph_sensor_hundred:03d}"

        # Creates the temp sensor String with a format of XX.XXX where X is a
        # random digit
        temp_sensor_decimal = random.randint(10, 99)
        temp_sensor_hundred = random.randint(100, 999)
        temp_sensor = f"{temp_sensor_decimal}.{temp_sensor_hundred:03d}"

        # Creates the do sensor String with a format of X.XXXX where X
        # is a random digit
        do_sensor_decimal = random.randint(0, 9)
        do_sensor_hundred = random.randint(1000, 9999)
        do_sensor = f"{do_sensor_decimal}.{do_sensor_hundred:03d}"

        # Creates the baro sensor String with a format of XXXXXX where X
        # is a random digit
        baro_sensor = random.randint(100000, 999999)

        sensor_string = (str(ph_sensor) + "&" + str(temp_sensor) + "&" +
                         str(do_sensor) + "&" + str(baro_sensor) + "NULL")
        return sensor_string

    @staticmethod
    def random_timestamp_string() -> str:
        """Generate random time stamp."""
        year = random.randint(2000, 2022)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        millisecond = random.randint(0, 999)

        timestampnum = f"""{year:04d}-{month:02d}-
        {day:02d}T{hour:02d}:{minute:02d}:{second:02d}.{millisecond:03d}"""
        timestamp = str(timestampnum)
        return timestamp

    # Creates a media entry with some random variables
    @staticmethod
    def rand_media_entry() -> MediaEntry.media_entry:
        """Create random media entry internal representation."""
        # List of ShotType to be chosen at random
        shottypelist = ["SINGLE", "BURST", "TELESCOPIC", "TIMELAPSE", "VIDEO"]
        shottype = random.choice(shottypelist)

        timestamp = RandomEntry.random_timestamp_string()
        # List of illumination type to be chosen at random
        illuminationtypelist = ["NONE", "WHITE", "RED", "ULTRAVIOLET"]
        illuminationtype = random.choice(illuminationtypelist)

        iso = (random.randint(1000, 9999))

        saturation = (random.randint(1000, 9999))

        shutterspeed = (random.randint(1000, 9999))

        whitebalance = (random.randint(1000, 9999))

        return MediaEntry.media_entry(shottype, timestamp, illuminationtype,
                                      iso, saturation, shutterspeed,
                                      whitebalance)

    # Creates a media metadata entry with random variables
    @staticmethod
    def rand_media_metadata():
        """Generate random media metadata internal representation."""
        left_camera_media = "left camera"

        right_camera_media = "right camera"

        time = RandomEntry.random_timestamp_string()

        sensor_data = RandomEntry.random_sensor_string()
        pH_data, temp_data, dissolved_oxygen_data, barometer_data = \
            SensorString.sensor_string(sensor_data)
        return MediaMetadata.mediadata(left_camera_media, right_camera_media,
                                       time, pH_data, temp_data,
                                       dissolved_oxygen_data, barometer_data)
