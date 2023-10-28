#!/usr/bin/env python3
"""Launches app.py using python3 without calling interpreter explicitly."""
import rsyncCopy
from cliArgs import args
from flask import render_template, url_for, Flask, request
from flask_sqlalchemy import SQLAlchemy
from representations import MediaEntryInternalRepresentation
import os
from forms import return_study_profile_form, return_search_form
import json
from sqlalchemy.dialects.sqlite import TEXT, REAL, INTEGER
import webbrowser
from representations import MediaMetadataInternalRepresentation
from sqlalchemy import select, desc, asc
from datetime import datetime
import re

basedir = os.path.abspath(os.path.dirname(__file__))

studies = list()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
           'sqlite:///' + os.path.join(basedir, 'test.db')
app.config['SECRET_KEY'] = "M.O.S.I.S"

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy(app)


class MediaEntry(db.Model):
    """Create media_entry database table.

    Contains:
    entryId (PRIMARY KEY INTEGER),
    shotType (TEXT NOT NULLABLE) an enum,
    time (TEXT NOT NULLABLE) format (yyyy-MM-ddTHH:mm:ss.zzz),
    illumination_type (TEXT NOT NULLABLE) an enum,
    saturation (INTEGER NOT NULLABLE),
    gain (REAL NOT NULLABLE),
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
    saturation = db.Column(INTEGER, nullable=False)
    gain = db.Column(REAL, nullable=False)
    shutterSpeed = db.Column(REAL, nullable=False)
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


@app.route("/")
def index():
    """Return index.html to the / route."""
    return render_template("index.html",
                           MediaEntries=getAllMediaEntry(db),
                           db=db,
                           getAllMediaMetadataId=getAllMediaMetadataId,
                           enumerate=enumerate,
                           str=str)


@app.route("/list")
def listView():
    return render_template("listView.html",
                           MediaEntries=getAllMediaEntry(db),
                           str=str,
                           round=round)


@app.route("/entry/<id>")
def entry(id=0):
    """Return render template for a specific entry."""
    MediaEntry = getMediaEntry(db, id)
    if MediaEntry.shotType == "SINGLE":
        return render_template("singleEntry.html",
                               MediaMetadata=getAllMediaMetadataId(db, id)[0],
                               str=str,
                               round=round,
                               url_for=url_for)
    elif MediaEntry.shotType == "BURST":
        return render_template("burstEntry.html",
                               MediaMetadata=getAllMediaMetadataId(db, id),
                               enumerate=enumerate,
                               str=str,
                               round=round,
                               url_for=url_for)
    elif MediaEntry.shotType == "TIMELAPSE":
        return render_template("timeLapseEntry.html",
                               MediaMetadata=getAllMediaMetadataId(db, id),
                               enumerate=enumerate,
                               str=str,
                               round=round,
                               url_for=url_for)
    elif MediaEntry.shotType == "VIDEO":
        return render_template("videoEntry.html",
                               MediaMetadata=getAllMediaMetadataId(db, id),
                               enumerate=enumerate,
                               str=str,
                               round=round,
                               url_for=url_for)
    else:
        return render_template("entry.html",
                               MediaEntry=getMediaEntry(db, id),
                               MediaMetadata=getAllMediaMetadataId(db, id),
                               enumerate=enumerate,
                               str=str,
                               round=round,
                               url_for=url_for)


def remove_submit_and_csrf_toten(studies: list) -> list:
    """Remove submit form field from studies."""
    ret = list()
    for study in studies:
        filtered_keys = list(
            filter(lambda x: x != 'submit' and x != "csrf_token",
                   study.keys()))
        temp_dict = dict()
        for key in filtered_keys:
            temp_dict[key] = study[key]
        ret.append(temp_dict)
    return ret


@app.route("/study/<st>", methods=['GET', 'POST'])
def single(st="single"):
    """Serve shot type study profile template configuration page."""
    form = return_study_profile_form(st)
    if form.is_submitted():
        if form.validate():
            studies.append(request.form)
            return index()
    return render_template(
        form.filename,
        form=form,
        studies=remove_submit_and_csrf_toten(studies),
        error=form.errors,
    )


@app.route("/save", methods=["GET", "POST"])
def save():
    """Serve study profile preview and save page."""
    if request.method == "POST":
        writeStudyProfilesToJSON(remove_submit_and_csrf_toten(studies))
        if not args.nobackup:
            rsyncCopy.rsync_recursive_copy(
                os.path.realpath("studyProfile.json"),
                "pi@{}:/home/pi/Documents/".format(args.ipaddress))
        return index()
    else:
        return render_template("saveStudyProfile.html",
                               studies=remove_submit_and_csrf_toten(studies))


@app.route("/search/<category>", methods=['GET', 'POST'])
def search(category: str):
    """Serve search form if GET or serve search results if post."""
    form = return_search_form(category)
    if form.is_submitted():
        print(form)
        ret = request.form
        searchBy = category
        searchQuery = ret["search"]
        mediaEntries = getMediaEntriesBySearchBy(searchBy, searchQuery)
        if ret.get("listView"):
            return render_template('listView.html',
                                   MediaEntries=mediaEntries,
                                   db=db,
                                   getAllMediaMetadataId=getAllMediaMetadataId,
                                   enumerate=enumerate,
                                   str=str,
                                   round=round)
        else:
            return render_template('index.html',
                                   MediaEntries=mediaEntries,
                                   db=db,
                                   getAllMediaMetadataId=getAllMediaMetadataId,
                                   enumerate=enumerate,
                                   str=str)

    def prettyCategory(searchBy: str) -> str:
        if searchBy == "id":
            return "ID"
        elif searchBy == "shotType":
            return "Shot Type"
        elif searchBy == "date":
            return "Date"
        elif searchBy == "illuminationType":
            return "Illumination Type"
        else:
            raise ValueError("Invalid search category.")

    return render_template('searchForm.html',
                           form=form,
                           searchBy=prettyCategory(category))


def writeStudyProfilesToJSON(studies: [dict]):
    """Write study profiles to JSON at app dir with name studyprofile.json."""
    jsonObject = json.dumps(studies, indent=4)
    jsonFile = open("studyProfile.json", "w")
    jsonFile.write(jsonObject)
    jsonFile.close()


def getMediaEntriesBySearchBy(
        searchBy: str, searchQuery: str) -> [MediaEntryInternalRepresentation]:
    if searchBy == "id":
        return getMediaEntriesById(db, parseIdRange(db, searchQuery))
    elif searchBy == "date":
        return getMediaEntriesByTime(db, searchQuery)
    elif searchBy == "shotType":
        return getMediaEntriesByShotType(db, searchQuery)
    elif searchBy == "illuminationType":
        return getMediaEntriesByIlluminationType(db, searchQuery)
    else:
        raise ValueError("Invalid Search By Input")


def getCurrentTime() -> str:
    """Return current time in 'yyyy-MM-ddTHH:mm:ss.zzz' format."""
    date = datetime.now()
    return date.strftime('%Y-%m-%-dT%H:%M:%S.%f')


def insertMediaEntry(db, shotType, illuminationType, saturation, gain,
                     shutterSpeed, whiteBalance):
    """Insert a MediaEntry into the database."""
    new_entry = MediaEntry(shotType=str(shotType),
                           time=getCurrentTime(),
                           illuminationType=str(illuminationType),
                           gain=gain,
                           saturation=saturation,
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
                                            ret[0].saturation, ret[0].gain,
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
                0].shotType, x[0].time, x[0].illuminationType, x[
                    0].saturation, x[0].gain, x[0].shutterSpeed, x[0].
                                                       whiteBalance), ret))
    return ret


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


def getFirstMediaEntry(db) -> int:
    """Get the minimum entryId from a database."""
    ret = db.session.execute(
        select(MediaEntry.entryId).order_by(asc(
            MediaEntry.entryId)).limit(1)).first()
    return int(ret[0])


def getLastMediaEntry(db) -> int:
    """Get the maximum entryId from a database."""
    ret = db.session.execute(
        select(MediaEntry.entryId).order_by(desc(
            MediaEntry.entryId)).limit(1)).first()
    return int(ret[0])


def getMediaEntriesById(db,
                        entryIDs: [int]) -> [MediaEntryInternalRepresentation]:
    """Get a list of media entries given a list of entry IDs."""
    returnMediaEntries = []
    for id in entryIDs:
        returnMediaEntries.append(getMediaEntry(db, id))
    return returnMediaEntries


def getMediaEntriesByShotType(
        db, shotType: str) -> [MediaEntryInternalRepresentation]:
    """Get a list of media entries given a shot type."""
    ret = db.session.execute(
        select(MediaEntry).where(MediaEntry.shotType == shotType))
    ret = list(
        map(
            lambda x: MediaEntryInternalRepresentation(x[0].entryId, x[
                0].shotType, x[0].time, x[0].illuminationType, x[
                    0].saturation, x[0].gain, x[0].shutterSpeed, x[0].
                                                       whiteBalance), ret))
    return ret


def getMediaEntriesByTime(db, time: str) -> [MediaEntryInternalRepresentation]:
    """Get a list of media entries by Time stamp."""
    ret = db.session.execute(
        select(MediaEntry).where(MediaEntry.time.like("%{}%".format(time))))
    ret = list(
        map(
            lambda x: MediaEntryInternalRepresentation(x[0].entryId, x[
                0].shotType, x[0].time, x[0].illuminationType, x[
                    0].saturation, x[0].gain, x[0].shutterSpeed, x[0].
                                                       whiteBalance), ret))
    return ret


def getMediaEntriesByIlluminationType(
        db, illuminationType: str) -> [MediaEntryInternalRepresentation]:
    """Get a list of media entries given a illumination type."""
    ret = db.session.execute(
        select(MediaEntry).where(
            MediaEntry.illuminationType == illuminationType))
    ret = list(
        map(
            lambda x: MediaEntryInternalRepresentation(x[0].entryId, x[
                0].shotType, x[0].time, x[0].illuminationType, x[
                    0].saturation, x[0].gain, x[0].shutterSpeed, x[0].
                                                       whiteBalance), ret))
    return ret


dualEndedRangeRegex = r'^\d+-\d+$'
leftEndedRangeragex = r'^\d+-$'
rightEndedRangeRegex = r'^-\d+$'
commaSeparatedValueRegex = r'^(\d+,)+\d+$'
singleValueRagex = r'^\d+$'


def parseIdRange(db, searchQuery: str) -> [int]:
    dbMin = getFirstMediaEntry(db)
    dbMax = getLastMediaEntry(db)
    entries = set()
    left = int()
    right = int()
    for query in searchQuery.split(" "):
        if bool(re.search(dualEndedRangeRegex, query)):
            left = int(query.split('-')[0])
            right = int(query.split('-')[-1])
            for i in returnRange(left, right, dbMin, dbMax):
                entries.add(int(i))
        elif bool(re.search(leftEndedRangeragex, query)):
            left = int(query.split('-')[0])
            right = dbMax
            for i in returnRange(left, right, dbMin, dbMax):
                entries.add(int(i))
        elif bool(re.search(rightEndedRangeRegex, query)):
            left = dbMin
            right = int(query.split('-')[-1])
            for i in returnRange(left, right, dbMin, dbMax):
                entries.add(int(i))
        elif bool(re.search(commaSeparatedValueRegex, query)):
            values = query.split(',')
            for i in values:
                entries.add(int(i))
        elif bool(re.search(singleValueRagex, query)):
            entries.add(int(query))
    entries = list(filter(lambda x: x >= dbMin and x <= dbMax, entries))
    entries.sort()
    return entries


def returnRange(left: int, right: int, dbMin: int, dbMax: int) -> [int]:
    if left > right:
        temp = left
        left = right
        right = temp
    if left < dbMin:
        left = dbMin
    if right > dbMax:
        right = dbMax
    return list(range(left, right + 1, 1))


if __name__ == "__main__":
    if not args.nobackup:
        try:
            rsyncCopy.rsync_recursive_copy(
                "pi@{}:/home/pi/".format(args.ipaddress), args.output)
        except Exception:
            raise ValueError("Invalid IP Address or Hostname was inputted.")
    from waitress import serve
    webbrowser.open("http://127.0.0.1:5000", new=2, autoraise=True)
    #serve(app, host="0.0.0.0", port=5000)
    app.run(debug=True)
