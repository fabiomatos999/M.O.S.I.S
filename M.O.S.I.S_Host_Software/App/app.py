#!/usr/bin/env python3
"""Launches app.py using python3 without calling interpreter explicitly."""
import rsyncCopy
from cliArgs import args
from flask import render_template, url_for, Flask, request
from representations import MediaEntryInternalRepresentation
import os
from forms import return_study_profile_form, return_search_form
import json
import webbrowser
from datetime import datetime
import db

dbQuery = db.DatabaseQuery()

basedir = os.path.abspath(os.path.dirname(__file__))

studies = list()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
           'sqlite:///' + os.path.join(basedir, 'test.db')
app.config['SECRET_KEY'] = "M.O.S.I.S"


@app.route("/")
def index():
    """Return index.html to the / route."""
    return render_template("index.html",
                           MediaEntries=dbQuery.getAllMediaEntry(),
                           getAllMediaMetadataId=dbQuery.getAllMediaMetadataId,
                           enumerate=enumerate,
                           str=str)


@app.route("/list")
def listView():
    return render_template("listView.html",
                           MediaEntries=dbQuery.getAllMediaEntry(),
                           str=str,
                           round=round)


@app.route("/entry/<id>")
def entry(id=0):
    """Return render template for a specific entry."""
    MediaEntry = dbQuery.getMediaEntry(id)
    if MediaEntry.shotType == "SINGLE":
        return render_template("singleEntry.html",
                               MediaMetadata=dbQuery.getAllMediaMetadataId(id)[0],
                               str=str,
                               round=round,
                               url_for=url_for)
    elif MediaEntry.shotType == "BURST":
        return render_template("burstEntry.html",
                               MediaMetadata=dbQuery.getAllMediaMetadataId(id),
                               enumerate=enumerate,
                               str=str,
                               round=round,
                               url_for=url_for)
    elif MediaEntry.shotType == "TIMELAPSE":
        return render_template("timeLapseEntry.html",
                               MediaMetadata=dbQuery.getAllMediaMetadataId(id),
                               enumerate=enumerate,
                               str=str,
                               round=round,
                               url_for=url_for)
    elif MediaEntry.shotType == "VIDEO":
        return render_template("videoEntry.html",
                               MediaMetadata=dbQuery.getAllMediaMetadataId(id),
                               enumerate=enumerate,
                               str=str,
                               round=round,
                               url_for=url_for)
    else:
        return render_template("entry.w",
                               MediaEntry=dbQuery.getMediaEntry(id),
                               MediaMetadata=dbQuery.getAllMediaMetadataId(id),
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
    studyAdded = False
    if form.is_submitted():
        if form.validate():
            studies.append(request.form)
            studyAdded = True
    return render_template(
        form.filename,
        form=form,
        studies=remove_submit_and_csrf_toten(studies),
        error=form.errors,
        str=str,
        enumerate=enumerate,
        len=len,
        range=range,
        studyAdded=studyAdded
    )


@app.route("/save", methods=["GET", "POST"])
def save():
    """Serve study profile preview and save page."""
    studySaved = False
    if request.method == "POST":
        writeStudyProfilesToJSON(remove_submit_and_csrf_toten(studies))
        if not args.nobackup:
            rsyncCopy.rsync_recursive_copy(
                os.path.realpath("studyProfile.json"),
                "pi@{}:/home/pi/Documents/".format(args.ipaddress))
        studySaved = True
    return render_template("saveStudyProfile.html",
                           studies=remove_submit_and_csrf_toten(studies),
                           enumerate=enumerate,
                           str=str,
                           len=len,
                           studySaved=studySaved)


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
                                   getAllMediaMetadataId=dbQuery.getAllMediaMetadataId,
                                   enumerate=enumerate,
                                   str=str,
                                   round=round)
        else:
            return render_template('index.html',
                                   MediaEntries=mediaEntries,
                                   getAllMediaMetadataId=dbQuery.getAllMediaMetadataId,
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
        return dbQuery.getMediaEntriesById(dbQuery.parseIdRange(searchQuery))
    elif searchBy == "date":
        return dbQuery.getMediaEntriesByTime(searchQuery)
    elif searchBy == "shotType":
        return dbQuery.getMediaEntriesByShotType(searchQuery)
    elif searchBy == "illuminationType":
        return dbQuery.getMediaEntriesByIlluminationType(searchQuery)
    else:
        raise ValueError("Invalid Search By Input")


def getCurrentTime() -> str:
    """Return current time in 'yyyy-MM-ddTHH:mm:ss.zzz' format."""
    date = datetime.now()
    return date.strftime('%Y-%m-%-dT%H:%M:%S.%f')


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
