from models import app, db
from flask import render_template, url_for
from query import getAllMediaEntry, getAllMediaMetadataId, getMediaEntry


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
