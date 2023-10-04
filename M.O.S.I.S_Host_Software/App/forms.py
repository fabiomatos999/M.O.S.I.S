from flask_wtf import FlaskForm
from wtforms import FloatField, DecimalField, SubmitField, SelectField

class ShotTypeSingleForm(FlaskForm):
    whiteBalance = DecimalField('White Balance')
    shutterSpeed = FloatField('Shutter Speed')
    illuminationType = SelectField('Illumination Type', choices=[("NONE", "None"), ("VISIBLESPECTRUM", "Visible Spectrum") , ("INFRARED", "Infrared"), ("ULTRAVIOLET", "Ultraviolet")])
    submit = SubmitField('Download Study')
