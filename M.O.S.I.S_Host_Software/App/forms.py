from flask_wtf import FlaskForm
from wtforms import FloatField, DecimalField, SubmitField, SelectField, StringField
from wtforms.validators import InputRequired, NumberRange


class ShotTypeSingleForm(FlaskForm):
    shotType = SelectField('Shot Type', choices=[("SINGLE", "Single")])
    whiteBalance = DecimalField('White Balance', default=3200, validators=[InputRequired(), NumberRange(3200, 6500)])
    shutterSpeed = FloatField('Shutter Speed', validators=[InputRequired(), validate_shutter()], default=0.0167)
    illuminationType = SelectField('Illumination Type',
                                   choices=[("NONE", "None"), ("VISIBLESPECTRUM", "Visible Spectrum"),
                                            ("INFRARED", "Infrared"), ("ULTRAVIOLET", "Ultraviolet")])
    submit = SubmitField('Download Study')


def validate_shutter(form, field):
    if not field.data >= 0.00002 and not field.data <= 120:
        ValidationError("Please input a shutter speed from 0.00002 to 120.")
