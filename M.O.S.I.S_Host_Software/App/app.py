#!/usr/bin/env python3
"""Launches app.py using python3 without calling interpreter explicitly."""
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.sqlite import TEXT, REAL, INTEGER
from sqlalchemy import select
import os
import json
from datetime import datetime
from enum import Enum, verify, UNIQUE, CONTINUOUS

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
    illuminationType = db.Column(TEXT, nullable=False)
    iso = db.Column(INTEGER, nullable=False)
    apertureSize = db.Column(REAL, nullable=False)
    shutterSpeed = db.Column(REAL, nullable=False)
    whiteBalance = db.Column(INTEGER, nullable=False)

    def __repr__(self):
        """Return MediaEntry.entryId when inserting into database."""
        return '<Task %r>' % self.entryId


class MediaEntryInternalRepresentation():
    """Internal representation for MediaEntry."""

    entryId = int()
    shotType = None
    time = str()
    illuminationType = None
    iso = int()
    apertureSize = float()
    shutterSpeed = float()
    whiteBalance = float()

    def __init__(self, entryId: int, shotType: shotType, time: str,
                 illuminationType: illuminationType, iso: int,
                 apertureSize: float, shutterSpeed: float, whiteBalance: int):
        """Construct MediaEntryInternalRepesentation."""
        self.entryId = entryId
        self.shotType = shotType
        self.time = time
        self.illuminationType = illuminationType
        self.iso = iso
        self.apertureSize = apertureSize
        self.shutterSpeed = shutterSpeed
        self.whiteBalance = whiteBalance


def getCurrentTime() -> str:
    """Return current time in 'yyyy-MM-ddTHH:mm:ss.zzz' format."""
    date = datetime.now()
    return date.strftime('%Y-%m-%-dT%H:%M:%S.%f')


def insertMediaEntry(db, shotType, illuminationType, iso, apertureSize,
                     shutterSpeed, whiteBalance):
    """Insert a MediaEntry into the database."""
    new_entry = MediaEntry(shotType=str(shotType),
                           time=getCurrentTime(),
                           illuminationType=str(illuminationType),
                           iso=iso,
                           apertureSize=apertureSize,
                           shutterSpeed=shutterSpeed,
                           whiteBalance=whiteBalance)
    db.session.add(new_entry)
    db.session.commit()


def getMediaEntry(db, id: int) -> MediaEntryInternalRepresentation:
    """Get MediaEntry where entryId == id."""
    ret = db.session.execute(
        select(MediaEntry).where(MediaEntry.entryId == id)).first()
    return MediaEntryInternalRepresentation(ret[0].entryId, ret[0].shotType,
                                            ret[0].time,
                                            ret[0].illuminationType,
                                            ret[0].iso, ret[0].apertureSize,
                                            ret[0].shutterSpeed,
                                            ret[0].whiteBalance)


def getAllMediaEntryIDs(db):
    """Get all entryId from database."""
    dbReturn = list(db.session.execute(select(MediaEntry.entryId)))
    return list(map(lambda x: x[0], dbReturn))


def getAllMediaEntry(db) -> list[MediaEntryInternalRepresentation]:
    """Get all Media Entries from a database."""
    ret = list(db.session.execute(select(MediaEntry)))
    ret = list(
        map(
            lambda x: MediaEntryInternalRepresentation(x[0].entryId, x[
                0].shotType, x[0].time, x[0].illuminationType, x[0].iso, x[
                    0].apertureSize, x[0].shutterSpeed, x[0].whiteBalance),
            ret))
    return ret


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


class MediaMetadataInternalRepresentation:
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
                 ph: float, dissolvedOxygen: float, pressure: float):
        """Construct MediaMetadataInternalRepresentation."""
        self.metadataId = metadataId
        self.entryId = entryId
        self.leftCameraMedia = leftCameraMedia
        self.rightCameraMedia = rightCameraMedia
        self.time = time
        self.temperature = temperature
        self.ph = ph
        self.dissolvedOxygen = dissolvedOxygen
        self.pressure = pressure


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


def getAllMediaMetadataId(
        db, entryId: int) -> list[MediaMetadataInternalRepresentation]:
    """Get all MediaMetadata with a specific entry ID from a database."""
    ret = list(
        db.session.execute(
            select(MediaMetadata).where(MediaMetadata.entryId == entryId)))
    ret = list(
        map(
            lambda x: MediaMetadataInternalRepresentation(
                x[0].metadataId, x[0].entryId, x[0].leftCameraMedia, x[0].
                rightCameraMedia, x[0].time, x[0].temperature, x[0].ph, x[
                    0].dissolvedOxygen, x[0].pressure), ret))
    return ret


def getAllMediaMetadata(db) -> list[MediaMetadataInternalRepresentation]:
    """Get all MediaMetadata entries from a database."""
    ret = list(db.session.execute(select(MediaMetadata)))
    ret = list(
        map(
            lambda x: MediaMetadataInternalRepresentation(
                x[0].metadataId, x[0].entryId, x[0].leftCameraMedia, x[0].
                rightCameraMedia, x[0].time, x[0].temperature, x[0].ph, x[
                    0].dissolvedOxygen, x[0].pressure), ret))
    return ret


class MediaEntryJSONRepresentation():
    """Class to convert MediaEntry with metadata to JSON."""

    def __init__(self, id: int):
        """Construct MediaEntry JSON representation."""
        self.MediaEntry = getMediaEntry(db, id).__dict__
        self.MediaMetadata = list(
            map(lambda x: x.__dict__, getAllMediaMetadataId(db, id)))

    def intoJSON(self) -> str:
        """Return JSON representation of self."""
        return json.dumps(self.__dict__, indent=4)


def fromJSON(path: str) -> MediaEntryJSONRepresentation:
    jf = openMediaEntryJSON(path)
    jf = json.loads(jf)
    return MediaEntryJSONRepresentation(jf["MediaEntry"]["entryId"])


def writeMediaEntryJSON(json: str, path: str):
    f = open(path, "w")
    f.write(json)
    f.close()


def openMediaEntryJSON(path: str) -> str:
    f = open(path, "r")
    ret = f.read()
    f.close()
    return ret


@verify(UNIQUE, CONTINUOUS)
class shotType(Enum):
    """Shot Type for the type of study to be performed."""

    SINGLE = 1
    BURST = 2
    TELESCOPIC = 3
    TIMELAPSE = 4
    VIDEO = 5


@verify(UNIQUE, CONTINUOUS)
class illuminationType(Enum):
    """Illumination Type."""

    NONE = 1
    VISIBLESPECTRUM = 2
    INFRARED = 3
    ULTRAVIOLET = 4


@app.route("/")
def index():
    """Return index.html to the / route."""
    return render_template("index.html",
                           MediaEntries=getAllMediaEntry(db),
                           db=db,
                           getAllMediaMetadataId=getAllMediaMetadataId,
                           enumerate=enumerate,
                           str=str)


@app.route("/entry/<id>")
def entry(id=0):
    """Return render template for a specific entry."""
    return render_template("entry.html",
                           MediaEntry=getMediaEntry(db, id),
                           MediaMetadata=getAllMediaMetadataId(db, id),
                           enumerate=enumerate,
                           str=str,
                           round=round)


if __name__ == "__main__":
    app.run(debug=True)
