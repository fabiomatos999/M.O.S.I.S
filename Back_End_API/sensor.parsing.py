class SensorString():

    # Separates the raw data from the sensors into different variables the format is '9.657&25.761&8.3400&1234567NULL'
    @staticmethod
    def sensor_string(data:str):
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


    def main(self):
        datas = self.sensor_string("9.657&25.761&8.3400&1234567NULL")
        for data in datas:
            print(data)

sensor = SensorString()
sensor.main()
