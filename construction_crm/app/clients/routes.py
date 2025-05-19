from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Client, Journal
from datetime import datetime

bp = Blueprint('clients', __name__)

@bp.route('/clients')
@login_required
def clients():
    clients_list = Client.query.filter_by(utilisateur_id=current_user.id).all()
    return render_template('clients/clients.html', clients=clients_list)

@bp.route('/clients/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter_client():
    if request.method == 'POST':
        try:
            # Nettoyer et valider le téléphone
            telephone = request.form['telephone'].replace(/\D/g, '')
            if len(telephone) != 10 or not telephone.isdigit():
                flash('Format de téléphone invalide (10 chiffres requis)', 'danger')
                return redirect(url_for('clients.ajouter_client'))

            # Créer le client
            nouveau_client = Client(
                nom=request.form['nom'],
                telephone=f"({telephone[:3]}){telephone[3:6]}-{telephone[6:]}",
                email=request.form.get('email', ''),
                entreprise=request.form.get('entreprise', ''),
                utilisateur_id=current_user.id
            )

            db.session.add(nouveau_client)
            db.session.commit()

            # Journalisation
            journal = Journal(
                action=f"Nouveau client ajouté: {request.form['nom']}",
                utilisateur_id=current_user.id,
                date=datetime.utcnow()
            )
            db.session.add(journal)
            db.session.commit()

            flash('Client ajouté avec succès!', 'success')
            return redirect(url_for('clients.clients'))

        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de l'ajout du client: {str(e)}", 'danger')
            return redirect(url_for('clients.ajouter_client'))

    return render_template('clients/ajouter_client.html')

@bp.route('/clients/supprimer/<int:id>')
@login_required
def supprimer_client(id):
    client = Client.query.get_or_404(id)
    if client.utilisateur_id != current_user.id:
        flash('Action non autorisée', 'danger')
        return redirect(url_for('clients.clients'))
    
    try:
        db.session.delete(client)
        db.session.commit()
        flash('Client supprimé avec succès', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f"Erreur lors de la suppression: {str(e)}", 'danger')
    
    return redirect(url_for('clients.clients'))