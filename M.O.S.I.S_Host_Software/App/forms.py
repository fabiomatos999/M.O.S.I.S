"""Classes and functions for study profile configuration forms."""
from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField, SelectField
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

    submit = SubmitField('Download Study')


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


def return_form(class_string: str) -> Type[BaseShotTypeForm]:
    """Return shot type based on string.

    Warning: If a BaseShotTypeForm class is given as a parameter,
    it will raise a ValueError exception..
    """
    if (class_string == "single"):
        return ShotTypeSingleForm()
    elif (class_string == "burst"):
        return ShotTypeBurstForm()
    else:
        raise ValueError("Cannot serve form from base class.")
