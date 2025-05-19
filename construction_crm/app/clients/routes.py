from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.clients.models import db 
from datetime import datetime
import re  # Import the regex module

bp = Blueprint('clients', __name__)

@bp.route('/clients')
@login_required
def liste_clients():
    clients = Client.query.filter_by(utilisateur_id=current_user.id).all()
    return render_template('clients/index.html', clients=clients)

@bp.route('/clients/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter_client():
    if request.method == 'POST':
        try:
            # Clean phone number using Python's re module
            telephone = re.sub(r'\D', '', request.form['telephone'])
            
            # Validate phone number (10 digits)
            if len(telephone) != 10 or not telephone.isdigit():
                flash('Le numéro de téléphone doit contenir 10 chiffres', 'danger')
                return redirect(url_for('clients.ajouter_client'))

            # Format as (xxx)xxx-xxxx
            telephone_formaté = f"({telephone[:3]}){telephone[3:6]}-{telephone[6:]}"
            
            nouveau_client = Client(
                nom=request.form['nom'],
                telephone=telephone_formaté,
                email=request.form.get('email', ''),
                entreprise=request.form.get('entreprise', ''),
                utilisateur_id=current_user.id
            )
            
            db.session.add(nouveau_client)
            db.session.commit()
            
            flash('Client ajouté avec succès!', 'success')
            return redirect(url_for('clients/index.html'))
            
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de l'ajout du client: {str(e)}", 'danger')
            return redirect(url_for('clients.ajouter_client'))
    
    return render_template('clients/ajouter.html')

@bp.route('/clients/modifier/<int:id>', methods=['GET', 'POST'])
@login_required
def modifier_client(id):
    client = Client.query.get_or_404(id)
    if client.utilisateur_id != current_user.id:
        flash('Action non autorisée', 'danger')
        return redirect(url_for('clients/index.html'))
    
    if request.method == 'POST':
        try:
            # Clean and validate phone number
            telephone = re.sub(r'\D', '', request.form['telephone'])
            if len(telephone) != 10 or not telephone.isdigit():
                flash('Numéro de téléphone invalide', 'danger')
                return redirect(url_for('clients.modifier_client', id=id))
            
            client.nom = request.form['nom']
            client.telephone = f"({telephone[:3]}){telephone[3:6]}-{telephone[6:]}"
            client.email = request.form.get('email', '')
            client.entreprise = request.form.get('entreprise', '')
            
            db.session.commit()
            flash('Client modifié avec succès!', 'success')
            return redirect(url_for('clients/index.html'))
            
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de la modification: {str(e)}", 'danger')
            return redirect(url_for('clients.modifier_client', id=id))
    
    return render_template('clients/modifier.html', client=client)

@bp.route('/clients/supprimer/<int:id>')
@login_required
def supprimer_client(id):
    client = Client.query.get_or_404(id)
    if client.utilisateur_id != current_user.id:
        flash('Action non autorisée', 'danger')
        return redirect(url_for('clients/index.html'))
    
    try:
        db.session.delete(client)
        db.session.commit()
        flash('Client supprimé avec succès', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f"Erreur lors de la suppression: {str(e)}", 'danger')
    
    return redirect(url_for('clients/index.html'))
    
@bp.route('/')
@login_required
def index():
    clients = Client.query.filter_by(utilisateur_id=current_user.id).all()
    return render_template('clients/index.html', clients=clients)    
    