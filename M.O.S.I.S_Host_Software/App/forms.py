from flask_wtf import FlaskForm
from wtforms import FloatField, DecimalField, SubmitField, SelectField, StringField
from wtforms.validators import InputRequired

class ShotTypeSingleForm(FlaskForm):
    shotType = SelectField('Shot Type', choices=[("SINGLE", "Single")])
    whiteBalance = DecimalField('White Balance', default=3200, validators=[InputRequired()])
    shutterSpeed = FloatField('Shutter Speed', validators=[InputRequired()], default=0.0167)
    illuminationType = SelectField('Illumination Type', choices=[("NONE", "None"), ("VISIBLESPECTRUM", "Visible Spectrum") , ("INFRARED", "Infrared"), ("ULTRAVIOLET", "Ultraviolet")])
    submit = SubmitField('Download Study')
