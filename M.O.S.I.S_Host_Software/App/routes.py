from flask import render_template, url_for, Flask, request, Blueprint, redirect
from representations import MediaEntryInternalRepresentation
import os
from forms import return_study_profile_form, return_search_form, deletionForm
import json
import db
from cliArgs import args
import sshUtils
import pdfkit
import subprocess

path_wkhtmltopdf = None
config = None

if os.name == 'nt':
    path_wkhtmltopdf = 'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

website = Blueprint('website', __name__)
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
                           str=str,
                           os=os,
                           sei=serializeEntryIds)


def serializeEntryIds(mediaEntries: [MediaEntryInternalRepresentation]) -> str:
    IDs = list(map(lambda x: x.entryId, mediaEntries))
    ret = str()
    for ID in IDs:
        ret = ret + (str(ID) + ",")
    ret = ret[:-1]
    return ret


def decodeShutterSpeed(shutterSpeed: str) -> str:
    fraction = shutterSpeed.split("_")
    if len(fraction) == 2:
        return "{}/{}".format(fraction[0], fraction[1])
    else:
        return fraction[0]


@app.route("/list")
def listView():
    return render_template("listView.html",
                           MediaEntries=dbQuery.getAllMediaEntry(),
                           str=str,
                           round=round,
                           sei=serializeEntryIds,
                           decodeShutterSpeed=decodeShutterSpeed)


@app.route("/entry/<id>")
def entry(id=0):
    """Return render template for a specific entry."""
    return returnTemplateByEntryId(id)


def returnTemplateByEntryId(entryId: int):
    MediaEntry = dbQuery.getMediaEntry(entryId)
    if MediaEntry.shotType == "SINGLE":
        return render_template(
            "singleEntry.html",
            MediaMetadata=dbQuery.getAllMediaMetadataId(entryId)[0],
            str=str,
            round=round,
            url_for=url_for,
            os=os)
    elif MediaEntry.shotType == "BURST":
        return render_template(
            "burstEntry.html",
            MediaMetadata=dbQuery.getAllMediaMetadataId(entryId),
            enumerate=enumerate,
            str=str,
            round=round,
            url_for=url_for,
            os=os,
            folder=("Media" + "/" + str(dbQuery.getMediaEntry(entryId))))
    elif MediaEntry.shotType == "TIMELAPSE":
        return render_template(
            "timeLapseEntry.html",
            MediaMetadata=dbQuery.getAllMediaMetadataId(entryId),
            enumerate=enumerate,
            str=str,
            round=round,
            url_for=url_for,
            os=os,
            folder=("Media" + "/" + str(dbQuery.getMediaEntry(entryId))))
    elif MediaEntry.shotType == "TELESCOPIC":
        return render_template(
            "telescopicEntry.html",
            MediaMetadata=dbQuery.getAllMediaMetadataId(entryId),
            enumerate=enumerate,
            str=str,
            round=round,
            url_for=url_for,
            os=os,
            folder=("Media" + "/" + str(dbQuery.getMediaEntry(entryId))))
    elif MediaEntry.shotType == "VIDEO":
        return render_template(
            "videoEntry.html",
            MediaMetadata=dbQuery.getAllMediaMetadataId(entryId),
            enumerate=enumerate,
            str=str,
            round=round,
            url_for=url_for,
            os=os,
            folder=("Media" + "/" + str(dbQuery.getMediaEntry(entryId))))
    else:
        return render_template(
            "entry.html",
            MediaEntry=dbQuery.getMediaEntry(entryId),
            MediaMetadata=dbQuery.getAllMediaMetadataId(entryId),
            enumerate=enumerate,
            str=str,
            round=round,
            url_for=url_for,
            os=os)


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
    return render_template(form.filename,
                           form=form,
                           studies=remove_submit_and_csrf_toten(studies),
                           error=form.errors,
                           str=str,
                           enumerate=enumerate,
                           len=len,
                           range=range,
                           studyAdded=studyAdded)


@app.route("/save", methods=["GET", "POST"])
def save():
    """Serve study profile preview and save page."""
    studySaved = False
    if request.method == "POST":
        writeStudyProfilesToJSON(remove_submit_and_csrf_toten(studies))
        if not args.nobackup:
            sshUtils.scp_recursive_copy(
                os.path.realpath("studyProfile.json"),
                "pi@{}:/home/pi/M.O.S.I.S/Front_End/".format(args.ipaddress))
        studySaved = True
    return render_template("saveStudyProfile.html",
                           studies=remove_submit_and_csrf_toten(studies),
                           enumerate=enumerate,
                           str=str,
                           len=len,
                           studySaved=studySaved)


@app.route("/delete", methods=["GET", "POST"])
def delete():
    """Serve delete RPi media page."""
    form = deletionForm()
    mediaDeleted = False
    if args.nobackup:
        form.submit(disabled=True)
    if form.is_submitted():
        ret = request.form
        if ret.get("confirmation") and ret.get("delete"):
            sshUtils.ssh_delete("pi@{}".format(args.ipaddress),
                                "~/Media_Storage/*")
            mediaDeleted = True
        else:
            return redirect("/")
    return render_template('deletePiMedia.html',
                           form=form,
                           nobackup=args.nobackup,
                           mediaDeleted=mediaDeleted)


@app.route("/search/<category>", methods=['GET', 'POST'])
def search(category: str):
    """Serve search form if GET or serve search results if post."""

    def getMediaEntriesBySearchBy(
            searchBy: str,
            searchQuery: str) -> [MediaEntryInternalRepresentation]:
        if searchBy == "id":
            return dbQuery.getMediaEntriesById(
                dbQuery.parseIdRange(searchQuery))
        elif searchBy == "date":
            return dbQuery.getMediaEntriesByTime(searchQuery)
        elif searchBy == "shotType":
            return dbQuery.getMediaEntriesByShotType(searchQuery)
        elif searchBy == "illuminationType":
            return dbQuery.getMediaEntriesByIlluminationType(searchQuery)
        else:
            raise ValueError("Invalid Search By Input")

    form = return_search_form(category)
    if form.is_submitted():
        ret = request.form
        searchBy = category
        searchQuery = ret["search"]
        mediaEntries = getMediaEntriesBySearchBy(searchBy, searchQuery)
        if ret.get("listView"):
            return render_template(
                'listView.html',
                MediaEntries=mediaEntries,
                getAllMediaMetadataId=dbQuery.getAllMediaMetadataId,
                enumerate=enumerate,
                str=str,
                round=round,
                sei=serializeEntryIds,
                decodeShutterSpeed=decodeShutterSpeed)
        else:
            return render_template(
                'index.html',
                MediaEntries=mediaEntries,
                getAllMediaMetadataId=dbQuery.getAllMediaMetadataId,
                enumerate=enumerate,
                str=str,
                os=os,
                sei=serializeEntryIds)

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


@app.route("/export/<IDs>", methods=["GET"])
def export(IDs: str):
    IDsList = []
    for ID in IDs.split(","):
        IDsList.append(int(ID))
    mediaEntries = dbQuery.getMediaEntriesById(IDsList)
    return render_template("export.html",
                           MediaEntries=mediaEntries,
                           getAllMediaMetadataId=dbQuery.getAllMediaMetadataId,
                           enumerate=enumerate,
                           str=str,
                           round=round,
                           url_for=url_for,
                           os=os)


@app.route("/exportPrompt/<IDs>", methods=["POST"])
def exportPrompt(IDs: str):
    path = "test.pdf"
    output = os.path.join(args.output, "report.pdf")
    if os.name == 'nt':
        pdfkit.from_url("127.0.0.1:5000/export/{}".format(IDs),
                        path,
                        configuration=config)
        subprocess.Popen([
            "powershell",
            os.path.join(os.getcwd(), "compressPDF.ps1"), "-I", path, "-O",
            output
        ])
    else:
        pdfkit.from_url("127.0.0.1:5000/export/{}".format(IDs), path)
        subprocess.call([
            "gs", "-sDEVICE=pdfwrite", "-dPDFSETTINGS=/ebook", "-q", "-o",
            output, path
        ])
        os.remove(path)

    return redirect("/")


def writeStudyProfilesToJSON(studies: [dict]):
    """Write study profiles to JSON at app dir with name studyprofile.json."""
    jsonObject = json.dumps(studies, indent=4)
    jsonFile = open("studyProfile.json", "w")
    jsonFile.write(jsonObject)
    jsonFile.close()
