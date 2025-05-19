from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import Utilisateur  # Changed from User

class LoginForm(FlaskForm):
    nom_utilisateur = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired()])
    se_souvenir_de_moi = BooleanField('Se souvenir de moi')
    submit = SubmitField('Connexion')

class RegistrationForm(FlaskForm):
    nom_utilisateur = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired()])
    mot_de_passe2 = PasswordField(
        'Répéter le mot de passe', validators=[DataRequired(), EqualTo('mot_de_passe')])
    submit = SubmitField('Inscription')

    def validate_nom_utilisateur(self, nom_utilisateur):
        user = Utilisateur.query.filter_by(nom_utilisateur=nom_utilisateur.data).first()
        if user is not None:
            raise ValidationError('Ce nom d\'utilisateur est déjà pris.')

    def validate_email(self, email):
        user = Utilisateur.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Cet email est déjà utilisé.')