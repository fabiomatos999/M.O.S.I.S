#!/usr/bin/env python3
"""Launches app.py using python3 without calling interpreter explicitly."""
from flask import render_template, url_for, Flask, request
from flask_sqlalchemy import SQLAlchemy
from query import getAllMediaEntry, getAllMediaMetadataId, getMediaEntry
import os
from forms import return_form

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
                           str=str)


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


@app.route("/study/<st>", methods=['GET', 'POST'])
def single(st="single"):
    """Serve shot type study profile template configuration page."""
    form = return_form(st)

    if form.is_submitted():
        studies.append(request.form)
        return index()
    return render_template(form.filename, form=form)


if __name__ == "__main__":
    app.run(debug=True)
