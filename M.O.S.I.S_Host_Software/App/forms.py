"""Classes and functions for study profile configuration forms."""
from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField, SelectField, StringField, \
    BooleanField
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

    shutterSpeed = StringField('Shutter Speed (s)',
                               default="1/60",
                               validators=[InputRequired()])

    def validate_shutterSpeed(form, field):
        shutterSpeed = field.data
        if re.match(r"^\d+\/\d+$", shutterSpeed):
            numerator = int(shutterSpeed.split("/")[0])
            denominator = int(shutterSpeed.split("/")[1])
            if not (0.00002 < numerator / denominator < 2):
                raise ValidationError(
                    "Please input a value between 0.00002 and 2.")
        elif re.match(r"^\d+$", shutterSpeed):
            if not (0.00002 < float(shutterSpeed) < 2):
                raise ValidationError(
                    "Please input a value between 0.00002 and 2.")
        else:
            raise ValidationError("Please Input a Valid Fraction.")

    submit = SubmitField('Submit Study')


class ShotTypeSingleForm(BaseShotTypeForm):
    """Inherits from BaseShotTypeForm, Specifies shot type."""

    filename = "shotTypeSingleForm.html"
    shotType = SelectField('Shot Type',
                           choices=[(shotType.SINGLE.name, "Single")])


class ShotTypeBurstForm(BaseShotTypeForm):
    """Inherits from BaseShotTypeForm, specifies shot type and burst count."""

    filename = "shotTypeBurstForm.html"
    shotType = SelectField('Shot Type',
                           choices=[(shotType.BURST.name, "Burst")])
    shotCount = DecimalField('Shot Count',
                             places=0,
                             default=5,
                             validators=[InputRequired(),
                                         NumberRange(2)])


class ShotTypeTelescopicForm(BaseShotTypeForm):
    """Inherits from BaseShotTypeForm, specifies shot type and zoomOutCount."""

    filename = "shotTypeTelescopicForm.html"
    shotType = SelectField('Shot Type',
                           choices=[(shotType.TELESCOPIC.name, "Telescopic")])
    zoomOutCount = DecimalField('Zoom Out Count',
                                places=0,
                                default=5,
                                validators=[InputRequired(),
                                            NumberRange(2)])


class ShotTypeTimeLapseForm(BaseShotTypeForm):
    """Inherits from BaseShotTypeForm, specifies shot type,time, photoCount."""

    filename = "shotTypeTimeLapseForm.html"
    shotType = SelectField('Shot Type',
                           choices=[(shotType.TIMELAPSE.name, "Time Lapse")])
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
    shotType = SelectField('Shot Type',
                           choices=[(shotType.VIDEO.name, "Video")])
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
    submit = SubmitField('Submit Study')


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
