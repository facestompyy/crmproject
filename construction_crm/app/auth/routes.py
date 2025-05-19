from flask import render_template, flash, redirect, url_for, request
from app.auth.forms import FormulaireConnexion, FormulaireInscription
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.auth import bp

@bp.route('/connexion', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = FormulaireConnexion()
    if form.validate_on_submit():
        utilisateur = User.query.filter_by(username=form.nom_utilisateur.data).first()
        if utilisateur is None or not utilisateur.check_password(form.mot_de_passe.data):
            flash('Nom d\'utilisateur ou mot de passe invalide')
            return redirect(url_for('auth.login'))
        login_user(utilisateur, remember=form.se_souvenir.data)
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('main.index'))
    return render_template('auth/login.html', title='Connexion', form=form)

@bp.route('/deconnexion')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/enregistrement', methods=['GET', 'POST'])
@login_required
def register():
    if current_user.role != 'admin':
        return redirect(url_for('main.index'))
    form = FormulaireInscription()
    if form.validate_on_submit():
        utilisateur = User(
            username=form.nom_utilisateur.data,
            email=form.email.data,
            role=form.role.data
        )
        utilisateur.set_password(form.mot_de_passe.data)
        db.session.add(utilisateur)
        db.session.commit()
        flash('Nouvel utilisateur enregistre avec succes!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Enregistrement', form=form)