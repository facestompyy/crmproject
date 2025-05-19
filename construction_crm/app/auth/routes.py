from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Utilisateur  # Make sure this line uses Utilisateur
from app.auth.forms import LoginForm, RegistrationForm

bp = Blueprint('auth', __name__)

@bp.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if current_user.is_authenticated:
        return redirect(url_for('main.accueil'))
    
    form = LoginForm()
    if form.validate_on_submit():
        utilisateur = Utilisateur.query.filter_by(nom_utilisateur=form.nom_utilisateur.data).first()
        if utilisateur is None or not utilisateur.check_password(form.mot_de_passe.data):
            flash('Nom d\'utilisateur ou mot de passe invalide', 'danger')
            return redirect(url_for('auth.connexion'))
        login_user(utilisateur, remember=form.se_souvenir_de_moi.data)
        flash('Connexion réussie!', 'success')
        return redirect(url_for('main.accueil'))
    return render_template('auth/connexion.html', title='Connexion', form=form)

@bp.route('/deconnexion')
@login_required
def deconnexion():
    logout_user()
    flash('Vous avez été déconnecté avec succès.', 'info')
    return redirect(url_for('main.accueil'))

@bp.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if current_user.is_authenticated:
        return redirect(url_for('main.accueil'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Vérifier si l'utilisateur existe déjà
        if Utilisateur.query.filter_by(nom_utilisateur=form.nom_utilisateur.data).first():
            flash('Ce nom d\'utilisateur est déjà pris', 'danger')
            return redirect(url_for('auth.inscription'))
        
        # Créer un nouvel utilisateur
        nouvel_utilisateur = Utilisateur(
            nom_utilisateur=form.nom_utilisateur.data,
            email=form.email.data,
            role='employé'  # Rôle par défaut
        )
        nouvel_utilisateur.set_password(form.mot_de_passe.data)
        
        db.session.add(nouvel_utilisateur)
        db.session.commit()
        
        flash('Votre compte a été créé avec succès!', 'success')
        return redirect(url_for('auth.connexion'))
    
    return render_template('auth/inscription.html', title='Inscription', form=form)

@bp.route('/utilisateurs')
@login_required
def utilisateurs():
    if not current_user.role == 'admin':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('main.accueil'))
    
    liste_utilisateurs = Utilisateur.query.all()
    return render_template('auth/utilisateurs.html', utilisateurs=liste_utilisateurs)

@bp.route('/utilisateurs/modifier/<int:id>', methods=['GET', 'POST'])
@login_required
def modifier_utilisateur(id):
    if not current_user.role == 'admin':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('main.accueil'))
    
    utilisateur = Utilisateur.query.get_or_404(id)
    
    if request.method == 'POST':
        nouveau_role = request.form.get('role')
        if nouveau_role in ['admin', 'employé']:
            utilisateur.role = nouveau_role
            db.session.commit()
            flash('Rôle mis à jour avec succès', 'success')
        else:
            flash('Rôle invalide', 'danger')
        
        return redirect(url_for('auth.utilisateurs'))
    
    return render_template('auth/modifier_utilisateur.html', utilisateur=utilisateur)