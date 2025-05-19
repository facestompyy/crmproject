from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User

class FormulaireConnexion(FlaskForm):
    nom_utilisateur = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired()])
    se_souvenir = BooleanField('Se souvenir de moi')
    soumettre = SubmitField('Se connecter')

class FormulaireInscription(FlaskForm):
    nom_utilisateur = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', choices=[('admin', 'Admin'), ('sales', 'Commercial'), ('installer', 'Installateur')])
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired()])
    mot_de_passe2 = PasswordField('Repeter le mot de passe', validators=[DataRequired(), EqualTo('mot_de_passe')])
    soumettre = SubmitField('Enregistrer')

    def validate_nom_utilisateur(self, nom_utilisateur):
        utilisateur = User.query.filter_by(username=nom_utilisateur.data).first()
        if utilisateur is not None:
            raise ValidationError('Ce nom d\'utilisateur est deja pris.')

    def validate_email(self, email):
        utilisateur = User.query.filter_by(email=email.data).first()
        if utilisateur is not None:
            raise ValidationError('Cet email est deja utilise.')