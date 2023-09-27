import unittest

from sensorCopy import sensorHub, ReadResult


class TestSensorHub(unittest.TestCase):
    sensorHub = sensorHub()

    def testRead(self):
        readResult = self.sensorHub.Read()

        self.assertIsInstance(readResult, ReadResult)
        self.assertTrue(0 <= readResult.getPh() <= 7)
        self.assertTrue(-100 <= readResult.getTemp() <= 150)
        self.assertTrue(0 <= readResult.getDO() <= 100)
        self.assertTrue(0 <= readResult.getPressure() <= 10000)

    def testGetPh(self):
        ph = self.sensorHub.GetPh()

        self.assertIsInstance(ph, float)
        self.assertTrue(0 <= ph <= 7)

    def testGetDOreading(self):
        do = self.sensorHub.getDOreading()

        self.assertIsInstance(do, float)
        self.assertTrue(0 <= do <= 100)

    def testGetTemp(self):
        temp = self.sensorHub.GetTemp()

        self.assertIsInstance(temp, float)
        self.assertTrue(-100 <= temp <= 150)


if __name__ == "__main__":
    unittest.main()
