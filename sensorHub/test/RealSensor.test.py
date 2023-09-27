import src.sensor


def main():
    """
    Debugging file for when the sensor is actually connected
    """
    sensor = sensor.sensorHub()

    sensor.calibrateAll()
    sensor.getPh()
    sensor.getDOreading()
    sensor.getTemp()

    sensor.Read()


if __name__ == "__main__":
    main()
