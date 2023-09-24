#!/usr/bin/env python3
"""Call python3 interpreter from within python script."""

import os
import random

sterioscopicImageDirectory = os.path.realpath("static")
sterioscopicImageSeletection = ["Geology", "Island", "Mountains"]


def randImage() -> (str, str):
    """Return random sterioscopic images from sterioscopicImageSelection."""
    image = random.choice(sterioscopicImageSeletection)
    imageLeft = "L-{}.png".format(image)
    imageLeft = os.path.join(sterioscopicImageDirectory, imageLeft)
    imageRight = "R-{}.png".format(image)
    imageRight = os.path.join(sterioscopicImageDirectory, imageRight)
    return (imageLeft, imageRight)


def randPh() -> float:
    """Return a random floating point number between 0 and 14."""
    return random.random()*14


def randTemp() -> float:
    """Return a random floating point number between -2 and 32."""
    return (random.random()*32) - 2


def randPressure() -> float:
    """Return random floating point number between 1,013.25 and 1040."""
    return (random.random()*9026.75)+1013.25


def randDissolvedOxygen() -> float:
    """Return a random floating point number between 0 and 100."""
    return (random.random()*100)
