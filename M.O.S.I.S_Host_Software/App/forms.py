from flask_wtf import FlaskForm
from wtforms import FloatField, DecimalField, SubmitField, SelectField
from wtforms.validators import InputRequired, NumberRange
from wtforms import ValidationError
import decimal


class ShotTypeSingleForm(FlaskForm):
    shotType = SelectField('Shot Type', choices=[("SINGLE", "Single")])
    whiteBalance = DecimalField(
        'White Balance',
        places=0,
        rounding=decimal.ROUND_UP,
        default=3200,
        validators=[InputRequired(), NumberRange(3200, 6500)])
    shutterSpeed = DecimalField(
        'Shutter Speed',
        places=5,
        default=0.0167,
        validators=[InputRequired(),
                    NumberRange(0.00002, 120.0)])
    illuminationType = SelectField('Illumination Type',
                                   choices=[("NONE", "None"),
                                            ("VISIBLESPECTRUM",
                                             "Visible Spectrum"),
                                            ("INFRARED", "Infrared"),
                                            ("ULTRAVIOLET", "Ultraviolet")])
    submit = SubmitField('Download Study')
