#!/usr/bin/env python3
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
           'sqlite:///' + os.path.join(basedir, 'test.db')
db = SQLAlchemy(app)

class media_entry(db.Model):
    __tablename__ = "media_entry"
    entry_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    shot_type = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.entry_id

class media_metadata(db.Model):
    __tablename__ = "media_metadata"
    metadata_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    entry_id = db.Column(db.Integer, db.ForeignKey(media_entry.entry_id))
    left_camera_media = db.Column(db.String(200), nullable=False)
    right_camera_media = db.Column(db.String(200), nullable=False)
    time = db.Column(db.String(40), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    pressure = db.Column(db.Float, nullable=False)
    ph = db.Column(db.Float, nullable=False)
    dissolved_oxygen = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return '<Task %r>' % self.metadata_id
    
@app.route("/")
def index():
    return render_template("entry.html")

if __name__ == "__main__":
    app.run(debug=True)
