"""Classes and functions for study profile configuration forms."""
from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField, SelectField, StringField
from wtforms.validators import InputRequired, NumberRange
import decimal
from enums import shotType, illuminationType
from typing import Type


class BaseShotTypeForm(FlaskForm):
    """Contain all elements that all shot types have in common."""

    whiteBalance = DecimalField(
        'White Balance (K)',
        places=0,
        rounding=decimal.ROUND_UP,
        default=3200,
        validators=[InputRequired(), NumberRange(3200, 6500)])

    illuminationType = SelectField(
        'Illumination Type',
        choices=[(illuminationType.NONE.name, "None"),
                 (illuminationType.VISIBLESPECTRUM.name, "Visible Spectrum"),
                 (illuminationType.INFRARED.name, "Infrared"),
                 (illuminationType.ULTRAVIOLET.name, "Ultraviolet")])

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

    shutterSpeed = DecimalField(
        'Shutter Speed (s)',
        places=5,
        default=0.0167,
        validators=[InputRequired(),
                    NumberRange(0.00002, 120.0)])

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
                                    NumberRange(1)])
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


def return_form(class_string: str) -> Type[BaseShotTypeForm]:
    """Return shot type form based on string.

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


class searchForm(FlaskForm):
    searchBy = SelectField('Search By',
                           choises=[("id", "ID"), ("shotType", "Shot Type"),
                                    ("date", "Date"),
                                    ("illuminationType", "Illumination Type")])
    search = StringField("Search")
    submit = SubmitField('Submit Study')
