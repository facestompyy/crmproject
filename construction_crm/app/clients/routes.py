from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.extensions import db
import os
from app.clients import bp
from app.models import Client, Document
from app.clients.forms import FormulaireClient
@bp.route('/')
@login_required
def index():
    clients = Client.query.all()
    return render_template('clients/index.html', title='Clients', clients=clients)

@bp.route('/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter():
    form = FormulaireClient()
    if form.validate_on_submit():
        client = Client(
            name=form.nom.data,
            phone=form.telephone.data,
            email=form.email.data,
            address=form.adresse.data,
            notes=form.notes.data
        )
        db.session.add(client)
        db.session.commit()
        flash('Client ajoute avec succes!')
        return redirect(url_for('clients.index'))
    return render_template('clients/ajouter.html', title='Ajouter Client', form=form)

@bp.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def details(id):
    client = Client.query.get_or_404(id)
    form = FormulaireClient()
    if form.validate_on_submit():
        client.name = form.nom.data
        client.phone = form.telephone.data
        client.email = form.email.data
        client.address = form.adresse.data
        client.notes = form.notes.data
        db.session.commit()
        flash('Modifications enregistrees.')
        return redirect(url_for('clients.details', id=client.id))
    elif request.method == 'GET':
        form.nom.data = client.name
        form.telephone.data = client.phone
        form.email.data = client.email
        form.adresse.data = client.address
        form.notes.data = client.notes
    return render_template('clients/details.html', title='Details Client', client=client, form=form)

@bp.route('/<int:client_id>/upload', methods=['POST'])
@login_required
def upload_file(client_id):
    if 'document' not in request.files:
        flash('Aucun fichier selectionne')
        return redirect(url_for('clients.details', id=client_id))
    
    file = request.files['document']
    if file.filename == '':
        flash('Aucun fichier selectionne')
        return redirect(url_for('clients.details', id=client_id))
    
    if file:
        filename = secure_filename(file.filename)
        upload_folder = app.config['UPLOADED_DOCUMENTS_DEST']
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        doc = Document(
            filename=filename,
            path=filepath,
            client_id=client_id,
            uploaded_by=current_user.id,
            document_type=request.form.get('document_type', 'other')
        )
        db.session.add(doc)
        db.session.commit()
        flash('Fichier envoye avec succes!')
    
    return redirect(url_for('clients.details', id=client_id))