#!/usr/bin/env python3
"""Launches app.py using python3 without calling interpreter explicitly."""
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.sqlite import TEXT, REAL, INTEGER
from sqlalchemy import select
import os
from datetime import datetime
from enum import Enum

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
           'sqlite:///' + os.path.join(basedir, 'test.db')
db = SQLAlchemy(app)


class MediaEntry(db.Model):
    """Create media_entry database table.

    Contains:
    entryId (PRIMARY KEY INTEGER),
    shotType (TEXT NOT NULLABLE) an enum,
    time (TEXT NOT NULLABLE) format (yyyy-MM-ddTHH:mm:ss.zzz),
    illumination_type (TEXT NOT NULLABLE) an enum,
    iso (INTEGER NOT NULLABLE),
    apertureSize (REAL NOT NULLABLE),
    shutterSpeed (REAL NOT NULLABLE),
    whiteBalance (INTEGER NOT NULLABLE)
    """

    __tablename__ = "MediaEntry"
    entryId = db.Column(INTEGER,
                        primary_key=True,
                        autoincrement=True,
                        nullable=False)
    shotType = db.Column(TEXT, nullable=False)
    time = db.Column(TEXT, nullable=False)
    iluminationType = db.Column(TEXT, nullable=False)
    iso = db.Column(INTEGER, nullable=False)
    apertureSize = db.Column(REAL, nullable=False)
    shutterSpeed = db.Column(REAL, nullable=False)
    whiteBalance = db.Column(INTEGER, nullable=False)

    def __repr__(self):
        """Return MediaEntry.entryId when inserting into database."""
        return '<Task %r>' % self.entryId


class MediaEntryStruct():
    """Internal representation for MediaEntry."""

    entryId = int()
    shotType = None
    time = str()
    iluminationType = None
    iso = int()
    apertureSize = float()
    shutterSpeed = float()
    whiteBalance = float()

    def __init__(self, entryId: int, shotType: shotType, time: str,
                 iluminationType: iluminationType, iso: int,
                 apertureSize: float, shutterSpeed: float, whiteBalance: int):
        """Construct MediaEntryStruct."""
        self.entryId = entryId
        self.shotType = shotType
        self.time = time
        self.iluminationType = iluminationType
        self.iso = iso
        self.apertureSize = apertureSize
        self.shutterSpeed = shutterSpeed
        self.whiteBalance = whiteBalance


def getCurrentTime() -> str:
    """Return current time in 'yyyy-MM-ddTHH:mm:ss.zzz' format."""
    date = datetime.now()
    return date.strftime('%Y-%m-%-dT%H:%M:%S.%f')


def insertMediaEntry(db, shotType, iluminationType, iso, apertureSize,
                     shutterSpeed, whiteBalance):
    """Insert a MediaEntry into the database."""
    new_entry = MediaEntry(shotType=str(shotType),
                           time=getCurrentTime(),
                           illuminationType=str(iluminationType),
                           iso=iso,
                           apertureSize=apertureSize,
                           shutterSpeed=shutterSpeed,
                           whiteBalance=whiteBalance)
    db.session.add(new_entry)
    db.session.commit()


def getAllMediaEntryIDs(db):
    """Get all entryId from database."""
    dbReturn = list(db.session.execute(select(MediaEntry.entryId)))
    return list(map(lambda x: x[0], dbReturn))


class MediaMetadata(db.Model):
    """Create MediaMetadata database table.

    Contains:
    metadataId (PRIMARY KEY INTEGER),
    entryId (INTEGER, FOREIGN KEY (MediaEntry.entryId)),
    leftCameraMedia (TEXT NOT NULLABLE),
    rightCameraMedia (TEXT NOT NULLABLE),
    time (TEXT NOT NULLABLE) format (yyyy-MM-ddTHH:mm:ss.zzzzzz),
    temperature (REAL NOT NULLABLE),
    pressure (REAL NOT NULLABLE),
    ph (REAL NOT NULLABLE),
    dissolvedOxygen (REAL NOT NULLABLE),
    """

    __tablename__ = "MediaMetadata"
    metadataId = db.Column(INTEGER,
                           primary_key=True,
                           autoincrement=True,
                           nullable=False)
    entryId = db.Column(INTEGER, db.ForeignKey(MediaEntry.entryId))
    leftCameraMedia = db.Column(TEXT, nullable=False)
    rightCameraMedia = db.Column(TEXT, nullable=False)
    time = db.Column(TEXT, nullable=False)
    temperature = db.Column(REAL, nullable=False)
    pressure = db.Column(REAL, nullable=False)
    ph = db.Column(REAL, nullable=False)
    dissolvedOxygen = db.Column(REAL, nullable=False)

    def __repr__(self):
        """Return MediaMetadata.metadataId when inserting into database."""
        return '<Task %r>' % self.metadataId


class MediaMetadataStruct:
    """Internal representation for a MediaMetadata entry."""

    metadataId = int()
    entryId = int()
    leftCameraMedia = str()
    rightCameraMedia = str()
    time = str()
    temperature = float()
    pressure = float()
    ph = float()
    dissolvedOxygen = float()

    def __init__(self, metadataId: int, entryId: int, leftCameraMedia: str,
                 rightCameraMedia: str, time: str, temperature: float,
                 ph: float, dissolvedOxygen: float):
        """Construct MediaMetadataStruct."""
        self.metadataId = metadataId
        self.entryId = entryId
        self.leftCameraMedia = leftCameraMedia
        self.rightCameraMedia = rightCameraMedia
        self.time = time
        self.temperature = temperature
        self.ph = ph
        self.dissolvedOxygen = dissolvedOxygen


def insertMediaMetadata(db, entryId, leftCameraMedia, rightCameraMedia,
                        temperature, pressure, ph, dissolvedOxygen):
    """Insert MediaMetadata entry into database."""
    new_metadata = MediaMetadata(entryId=entryId,
                                 leftCameraMedia=leftCameraMedia,
                                 rightCameraMedia=rightCameraMedia,
                                 time=getCurrentTime(),
                                 temperature=temperature,
                                 pressure=pressure,
                                 ph=ph,
                                 dissolvedOxygen=dissolvedOxygen)
    db.session.add(new_metadata)
    db.session.commit()


class shotType(Enum):
    SINGLE = 1
    BURST = 2
    TELESCOPIC = 3
    TIMELAPSE = 4
    VIDEO = 5


class iluminationType(Enum):
    NONE = 1
    VISIBLESPECTRUM = 2
    INFRARED = 3
    ULTRAVIOLET = 4


@app.route("/")
def index():
    """Return index.html to the / route."""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
