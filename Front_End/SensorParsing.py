"""Sensor hub parsing module."""


class SensorString():
    """Wrapper class for SensorString module."""

    # Separates the raw data from the sensors into different variables the
    # format is '9.657&25.761&8.3400&1234567NULL'
    @staticmethod
    def sensor_string(data: str) -> (str, str, str, str):
        """Parse sensor string from sensor hub."""
        # Replaces NULL from the string with empty space
        data = data.replace('NULL', '')

        # Separates the data into different variables
        data_string = data.split('&')

        # Assign the values into different variables
        pH_data = data_string[0]
        temp_data = data_string[1]
        dissolved_oxygen_data = data_string[2]
        barometer_data = data_string[3]

        return pH_data, temp_data, dissolved_oxygen_data, barometer_data
