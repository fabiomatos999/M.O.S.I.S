#!/usr/bin/env python3
"""Call python3 interpreter from within python script."""

import os
import random
from enums import shotType, illuminationType
from app import insertMediaEntry, insertMediaMetadata, getAllMediaEntryIDs
from enum import Enum
import math

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
    return random.random() * 14


def randTemp() -> float:
    """Return a random floating point number between -2 and 32."""
    return (random.random() * 32) - 2


def randPressure() -> float:
    """Return random floating point number between 1,013.25 and 1040."""
    return (random.random() * 9026.75) + 1013.25


def randDissolvedOxygen() -> float:
    """Return a random floating point number between 0 and 100."""
    return (random.random() * 100)


def randShotType() -> Enum:
    """Return a random shotType."""
    return random.choice(list(shotType)).name


def randIluminationType() -> Enum:
    """Return a random iluminationType."""
    return random.choice(list(illuminationType)).name


def randGain() -> float:
    """Return a random float between 0 and 24."""
    return random.random() * 24


def randSaturation() -> int:
    """Return a random integer between 0 and 200."""
    return random.randint(0, 200)


def randShutterSpeed() -> float:
    """Return a random floating point number of common shutter speeds."""
    return random.choice([
        1 / 2000, 1 / 1000, 1 / 500, 1 / 250, 1 / 125, 1 / 60, 1 / 30, 1 / 15,
        1 / 8, 1 / 4, 1 / 2, 1.0, 2.0
    ])


def randWhiteBalance() -> int:
    """Return a random integer between 3,200 and 6,500."""
    return math.floor(random.random() * 3300) + 3200


def insertRandomMediaEntry(db):
    """Insert a MediaEntry into a database with random valid data."""
    insertMediaEntry(db, randShotType(), randIluminationType(),
                     randSaturation(), randGain(), randShutterSpeed(),
                     randWhiteBalance())


def getRandomMediaEntryEntryId(db) -> int:
    """Return a random entryId from MediaEntry table."""
    return random.choice(getAllMediaEntryIDs(db))


def insertRandomMediaMetadata(db):
    """Insert a MediaMetadata entry into a database with random valid data."""
    randImages = randImage()
    insertMediaMetadata(db, getRandomMediaEntryEntryId(db), randImages[0],
                        randImages[1], randTemp(), randPressure(), randPh(),
                        randDissolvedOxygen())
