#!/usr/bin/env python3
"""Launches app.py using python3 without calling interpreter explicitly."""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.sqlite import TEXT, REAL, INTEGER
import os

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
    shutterSpeed (INTEGER NOT NULLABLE),
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
    shutterSpeed = db.Column(INTEGER, nullable=False)
    whiteBalance = db.Column(INTEGER, nullable=False)

    def __repr__(self):
        """Return MediaEntry.entryId when inserting into database."""
        return '<Task %r>' % self.entryId


class MediaMetadata(db.Model):
    """Create MediaMetadata database table.

    Contains:
    metadataId (PRIMARY KEY INTEGER),
    entryId (INTEGER, FOREIGN KEY (MediaEntry.entryId)),
    leftCameraMedia (TEXT NOT NULLABLE),
    rightCameraMedia (TEXT NOT NULLABLE),
    time (TEXT NOT NULLABLE) format (yyyy-MM-ddTHH:mm:ss.zzz),
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


@app.route("/")
def index():
    """Return index.html to the / route."""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
