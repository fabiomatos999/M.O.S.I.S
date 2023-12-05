"""Classes and functions for study profile configuration forms."""
from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField, SelectField, StringField, \
    BooleanField, HiddenField
from wtforms.validators import InputRequired, NumberRange, ValidationError
import decimal
from enums import shotType, illuminationType
from typing import Type
import re


class BaseShotTypeForm(FlaskForm):
    """Contain all elements that all shot types have in common."""

    whiteBalance = DecimalField(
        'White Balance (K)',
        places=0,
        rounding=decimal.ROUND_UP,
        default=3200,
        validators=[InputRequired(), NumberRange(3200, 6500)])

    illuminationType = SelectField('Illumination Type',
                                   choices=[
                                       (illuminationType.NONE.name, "None"),
                                       (illuminationType.WHITE.name, "White"),
                                       (illuminationType.RED.name, "Red"),
                                       (illuminationType.ULTRAVIOLET.name,
                                        "Ultraviolet")
                                   ])

    gain = DecimalField('Gain (dB)',
                        places=2,
                        default=0,
                        validators=[InputRequired(),
                                    NumberRange(0, 24)])
    saturation = DecimalField(
        'Saturation (%)',
        places=0,
        default=100,
        validators=[InputRequired(), NumberRange(0, 200)])

    shutterSpeed = SelectField('Shutter Speed (s)',
                               choices=[("1/2000", "1/2000"),
                                        ("1/1000", "1/1000"),
                                        ("1/500", "1/500"), ("1/250", "1/250"),
                                        ("1/125", "1/125"), ("1/60", "1/60"),
                                        ("1/30", "1/30"), ("1/15", "1/15"),
                                        ("1/8", "1/8"), ("1/4", "1/4"),
                                        ("1/2", "1/2"), ("1", "1"),
                                        ("2", "2")])

    submit = SubmitField('Submit Study')


class ShotTypeSingleForm(BaseShotTypeForm):
    """Inherits from BaseShotTypeForm, Specifies shot type."""

    filename = "shotTypeSingleForm.html"
    shotType = HiddenField(shotType.SINGLE.name, default=shotType.SINGLE.name)


class ShotTypeBurstForm(BaseShotTypeForm):
    """Inherits from BaseShotTypeForm, specifies shot type and burst count."""

    filename = "shotTypeBurstForm.html"
    shotType = HiddenField(shotType.BURST.name, default=shotType.BURST.name)
    shotCount = DecimalField('Shot Count',
                             places=0,
                             default=5,
                             validators=[InputRequired(),
                                         NumberRange(2)])


class ShotTypeTelescopicForm(BaseShotTypeForm):
    """Inherits from BaseShotTypeForm, specifies shot type and zoomOutCount."""

    filename = "shotTypeTelescopicForm.html"
    shotType = HiddenField(shotType.TELESCOPIC.name,
                           default=shotType.TELESCOPIC.name)
    zoomOutCount = DecimalField('Zoom Out Count',
                                places=0,
                                default=5,
                                validators=[InputRequired(),
                                            NumberRange(2)])


class ShotTypeTimeLapseForm(BaseShotTypeForm):
    """Inherits from BaseShotTypeForm, specifies shot type,time, photoCount."""

    filename = "shotTypeTimeLapseForm.html"
    shotType = HiddenField(shotType.TIMELAPSE.name,
                           default=shotType.TIMELAPSE.name)
    time = DecimalField('Time (m)',
                        places=0,
                        default=60,
                        validators=[InputRequired(),
                                    NumberRange(0.1)])
    photoCount = DecimalField('Amount of Pictures',
                              places=0,
                              default=5,
                              validators=[InputRequired(),
                                          NumberRange(2)])


class ShotTypeVideoForm(BaseShotTypeForm):
    """Inherits from BaseShotTypeForm, specifies shot type and video length."""

    filename = "shotTypeVideoForm.html"
    shotType = HiddenField(shotType.VIDEO.name, default=shotType.VIDEO.name)
    videoLength = DecimalField('Video Length (s)',
                               places=0,
                               default=60,
                               validators=[InputRequired(),
                                           NumberRange(2)])


def return_study_profile_form(class_string: str) -> Type[BaseShotTypeForm]:
    """Return Study Profile form based on string.

    It will raise a ValueError exception if class_string is not either:
    'single', 'burst', 'telescopic', 'timeLapse', 'video'
    """
    if (class_string == "single"):
        return ShotTypeSingleForm()
    elif (class_string == "burst"):
        return ShotTypeBurstForm()
    elif (class_string == "telescopic"):
        return ShotTypeTelescopicForm()
    elif (class_string == "timeLapse"):
        return ShotTypeTimeLapseForm()
    elif (class_string == "video"):
        return ShotTypeVideoForm()
    else:
        raise ValueError("Cannot serve form.")


class baseSearchForm(FlaskForm):
    listView = BooleanField("List View")
    submit = SubmitField('Search')


class idSearchForm(baseSearchForm):
    search = StringField("Search", validators=[InputRequired()])


class shotTypeSearchForm(baseSearchForm):
    search = SelectField('Shot Type',
                         choices=[("SINGLE", "Single"), ("BURST", "Burst"),
                                  ("TELESCOPIC", "Telescopic"),
                                  ("TIMELAPSE", "Time Lapse"),
                                  ("VIDEO", "Video")])


class dateSearchForm(baseSearchForm):
    search = StringField("Search", validators=[InputRequired()])


class illuminationTypeSearchForm(baseSearchForm):
    search = SelectField('Illumination Type',
                         choices=[("WHITE", "White"), ("RED", "Red"),
                                  ("ULTRAVIOLET", "Ultraviolet"),
                                  ("NONE", "None")])


def return_search_form(searchBy: str) -> baseSearchForm:
    if searchBy == "id":
        return idSearchForm()
    elif searchBy == "shotType":
        return shotTypeSearchForm()
    elif searchBy == "date":
        return dateSearchForm()
    elif searchBy == "illuminationType":
        return illuminationTypeSearchForm()
    else:
        raise ValueError("Invalid search category.")


class deletionForm(FlaskForm):
    delete = BooleanField("Do you want to delete the Raspberry Pi Media?")
    confirmation = BooleanField("Are you sure?")
    submit = SubmitField('Delete Raspberry Pi Media')
