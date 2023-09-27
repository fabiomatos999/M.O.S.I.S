from sensorCopy import sensorHub


def main():
    """
    Debugging file for when the sensor is actually connected
    """
    sensor = sensorHub()

    # sensor.calibrateAll()
    sensor.getPh()
    sensor.getDO()
    sensor.getTemp()

    sensor.Read()


if __name__ == "__main__":
    main()
