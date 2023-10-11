from flask import render_template, url_for, Flask, request, Blueprint
from flask_sqlalchemy import SQLAlchemy
from query import getAllMediaEntry, getAllMediaMetadataId, getMediaEntry
import os
from forms import return_form, searchForm
import json
import rsyncCopy
from cliArgs import args
website = Blueprint('website', __name__)
basedir = os.path.abspath(os.path.dirname(__file__))

studies = list()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
           'sqlite:///' + os.path.join(basedir, 'test.db')
app.config['SECRET_KEY'] = "M.O.S.I.S"
db = SQLAlchemy(app)


@app.route("/")
def index():
    """Return index.html to the / route."""
    return render_template("index.html",
                           MediaEntries=getAllMediaEntry(db),
                           db=db,
                           getAllMediaMetadataId=getAllMediaMetadataId,
                           enumerate=enumerate,
                           str=str,
                           search=searchForm)


@app.route("/entry/<id>")
def entry(id=0):
    """Return render template for a specific entry."""
    return render_template("entry.html",
                           MediaEntry=getMediaEntry(db, id),
                           MediaMetadata=getAllMediaMetadataId(db, id),
                           enumerate=enumerate,
                           str=str,
                           round=round,
                           url_for=url_for)


def remove_submit(studies: list) -> list:
    """Remove submit form field from studies."""
    ret = list()
    for study in studies:
        filtered_keys = list(filter(lambda x: x != 'submit', study.keys()))
        temp_dict = dict()
        for key in filtered_keys:
            temp_dict[key] = study[key]
        ret.append(temp_dict)
    return ret


@app.route("/study/<st>", methods=['GET', 'POST'])
def single(st="single"):
    """Serve shot type study profile template configuration page."""
    form = return_form(st)

    if form.is_submitted():
        studies.append(request.form)
        return index()
    return render_template(form.filename,
                           form=form,
                           studies=remove_submit(studies))


@app.route("/save", methods=["GET", "POST"])
def save():
    """Serve study profile preview and save page."""
    if request.method == "POST":
        writeStudyProfilesToJSON(remove_submit(studies))
        rsyncCopy.rsync_recursive_copy(
            os.path.realpath("studyProfile.json"),
            "pi@{}:/home/pi/Documents/".format(args.ipaddress))
        return index()
    else:
        return render_template("saveStudyProfile.html",
                               studies=remove_submit(studies))


def writeStudyProfilesToJSON(studies: [dict]):
    """Write study profiles to JSON at app dir with name studyprofile.json."""
    jsonObject = json.dumps(studies, indent=4)
    jsonFile = open("studyProfile.json", "w")
    jsonFile.write(jsonObject)
    jsonFile.close()
