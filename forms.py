from email.policy import default
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, BooleanField
from wtforms.validators import InputRequired, Optional, NumberRange, URL


class AddPetForm(FlaskForm):
    """Form to add new pet to db"""
    name = StringField("Pet's name",
                       validators=[InputRequired()])
    species = SelectField("Species",
                          choices=[('cat', 'Cat'), ('dog', 'Dog'),
                                   ('porcupine', 'Porcupine')],
                          validators=[InputRequired()])
    photo_url = StringField("Photo URL (optional)",
                            validators=[Optional(),
                                        URL(require_tld=True,
                                        message='Please enter a valid image URL')])
    age = IntegerField("Age (optional)",
                       validators=[Optional(), NumberRange(min=None, max=30, message='Age must be between 0 and 30')])
    notes = StringField("Notes (optional)",
                        validators=[Optional()])


class EditPetForm(FlaskForm):
    """Form to add new pet to db"""
    photo_url = StringField("Photo URL",
                            validators=[Optional(),
                                        URL(require_tld=True,
                                        message='Please enter a valid image URL')])
    notes = StringField("Notes",
                        validators=[Optional()])

    available = BooleanField("Available")
