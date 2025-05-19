from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

class FormulaireClient(FlaskForm):
    nom = StringField('Nom complet', validators=[DataRequired()])
    telephone = StringField('Téléphone')
    email = StringField('Email', validators=[Email()])
    adresse = StringField('Adresse')
    notes = TextAreaField('Notes')
    soumettre = SubmitField('Enregistrer')