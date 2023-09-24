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
    illuminationType = db.Column(TEXT, nullable=False)
    iso = db.Column(INTEGER, nullable=False)
    apertureSize = db.Column(REAL, nullable=False)
    shutterSpeed = db.Column(REAL, nullable=False)
    whiteBalance = db.Column(INTEGER, nullable=False)

    def __repr__(self):
        """Return MediaEntry.entryId when inserting into database."""
        return '<Task %r>' % self.entryId


def getCurrentTime() -> str:
    """Return current time in 'yyyy-MM-ddTHH:mm:ss.zzz' format."""
    return datetime.now().strftime('yyyy-MM-ddTHH:mm:ss.zzz')


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


shotType = Enum('shotType',
                ['SINGLE', 'BURST', 'TELESCOPIC', 'TIMELAPSE', 'VIDEO'])
iluminationType = Enum('iluminationType',
                       ['NONE', 'VISIBLESPECTRUM', 'INFRARED', 'ULTRAVIOLET'])


@app.route("/")
def index():
    """Return index.html to the / route."""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
