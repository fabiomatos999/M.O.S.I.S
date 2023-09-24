#!/usr/bin/env python3
"""Call python3 interpreter from within python script."""

import os
import random
from app import shotType, illuminationType
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
    return random.choice(list(shotType))


def randIluminationType() -> Enum:
    """Return a random iluminationType."""
    return random.choice(list(illuminationType))


def randISO() -> int:
    """Return a random integer of either 100,200,400,800,1600,3200,6400."""
    return random.choice([100, 200, 400, 800, 1600, 3200, 6400])


def randApertureSize() -> float:
    """Return a random float of either 1.4,2.0,2.8,4.0,5.6,8.0,11,16.0,22.0."""
    return random.choice([1.4, 2.0, 2.8, 4.0, 5.6, 8.0, 11.0, 16.0, 22.0])


def randShutterSpeed() -> float:
    """Return a random floating point number of common shutter speeds."""
    return random.choice([
        1 / 2000, 1 / 1000, 1 / 500, 1 / 250, 1 / 125, 1 / 60, 1 / 30, 1 / 15,
        1 / 8, 1 / 4, 1 / 2, 1.0, 2.0, 4.0, 8.0, 15.0, 30.0
    ])


def randWhiteBalance() -> int:
    """Return a random integer between 1000 and 10,000."""
    return math.floor(random.random() * 9000) + 1000


def insertRandomMediaEntry(db):
    """Insert a MediaEntry into a database with random valid data."""
    insertMediaEntry(db, randShotType(), randIluminationType(), randISO(),
                     randApertureSize(), randShutterSpeed(),
                     randWhiteBalance())


def getRandomMediaEntryEntryId(db) -> int:
    "Return a random entryId from MediaEntry table."
    return random.choice(getAllMediaEntryIDs(db))


def insertRandomMediaMetadata(db):
    """Insert a MediaMedata entry into a database with random valid data."""
    randImages = randImage()
    insertMediaMetadata(db, getRandomMediaEntryEntryId(db), randImages[0],
                        randImages[1], randTemp(), randPressure(), randPh(),
                        randDissolvedOxygen())
