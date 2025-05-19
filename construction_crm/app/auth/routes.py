from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_utilisateur, logout_utilisateur, login_required, current_utilisateur
from werkzeug.security import generate_password_hash
from app import db
from app.models import Utilisateur, Journal
from datetime import datetime
from .forms import LoginForm, RegistrationForm
from .decorators import admin_required

bp = Blueprint('auth', __name__)

# ... (keep your existing login/logout routes) ...

@bp.route('/utilisateurs')
@login_required
@admin_required
def utilisateurs():
    utilisateurs_list = Utilisateur.query.all()
    return render_template('utilisateurs/utilisateurs.html', utilisateurs=utilisateurs_list)

@bp.route('/utilisateurs/ajouter', methods=['GET', 'POST'])
@login_required
@admin_required
def ajouter_utilisateur():
    if request.method == 'POST':
        try:
            nom_utilisateur = request.form['nom_utilisateur']
            
            # Vérifier l'existence de l'utilisateur
            if Utilisateur.query.filter_by(nom_utilisateur=nom_utilisateur).first():
                flash('Ce nom d\'utilisateur existe déjà', 'danger')
                return redirect(url_for('auth.ajouter_utilisateur'))

            # Créer le nouvel utilisateur
            nouvel_utilisateur = Utilisateur(
                nom_utilisateur=nom_utilisateur,
                mot_de_passe=generate_password_hash(request.form['mot_de_passe']),
                role='employé'  # Rôle par défaut
            )

            db.session.add(nouvel_utilisateur)
            db.session.commit()

            # Journalisation
            journal = Journal(
                action=f"Nouvel utilisateur créé: {nom_utilisateur}",
                utilisateur_id=current_utilisateur.id,
                date=datetime.utcnow()
            )
            db.session.add(journal)
            db.session.commit()

            flash(f'Utilisateur {nom_utilisateur} créé. Définissez ses permissions.', 'warning')
            return redirect(url_for('auth.utilisateurs'))

        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de la création: {str(e)}", 'danger')
            return redirect(url_for('auth.ajouter_utilisateur'))

    return render_template('utilisateurs/ajouter_utilisateur.html')

@bp.route('/utilisateurs/modifier_role/<int:id>', methods=['POST'])
@login_required
@admin_required
def modifier_role(id):
    utilisateur = Utilisateur.query.get_or_404(id)
    nouveau_role = request.form.get('role')
    
    if nouveau_role in ['admin', 'employé']:
        try:
            utilisateur.role = nouveau_role
            db.session.commit()
            flash('Rôle mis à jour avec succès', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de la mise à jour: {str(e)}", 'danger')
    
    return redirect(url_for('auth.utilisateurs'))