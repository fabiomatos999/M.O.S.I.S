import RPi.GPIO as GPIO
from typing import Callable


class HallEffectSensor:
    """
    Inteface for controlling the hall effect sensors connected to the raspberry pi
    NOTE: the callback is executed using interrupts; the callback also executes on a separate thread
    """

    def __init__(self, pin: int, callback: Callable):
        """
        Create a new Hall Effect Sensor object

        Args:
            pin (int): GPIO pin sensor is connected to
            callback (Callable): function to be executed upon interrupt form pin
        """
        self.pin = pin
        self.callback = callback

        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(
            self.pin, GPIO.FALLING, callback=self.callback, bouncetime=200
        )

    def changeCallback(self, newCallback: Callable) -> None:
        """Change callback function set for pin

        Args:
            newCallback (Callable): new callback function to be executed upon interrupt
        """
        GPIO.remove_event_detect(self.pin)
        self.callback = newCallback
        GPIO.add_event_detect(
            self.pin, GPIO.FALLING, callback=self.callback, bouncetime=200
        )

    def __repr__(self):
        return f"""HallEffectSensor Object:
                    pin: {self.pin}
                    callback function on press: {self.callback.__name__}"""
