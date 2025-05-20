from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models import Client
from app.extensions import db
from flask_login import login_required

bp = Blueprint('clients', __name__, url_prefix='/clients')

@bp.route('/')
def index():
    clients = Client.query.all()
    return render_template('clients/index.html', clients=clients)

@bp.route('/<int:id>')
def view(id):
    client = Client.query.get_or_404(id)
    return render_template('clients/view.html', client=client)
    
@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        # Process form data
        client = Client(
            name=request.form['name'],
            email=request.form['email'],
            phone=request.form['phone'],
            company=request.form.get('company', ''),
            notes=request.form.get('notes', '')
        )
        db.session.add(client)
        db.session.commit()
        flash('Client created successfully!', 'success')
        return redirect(url_for('clients.view', id=client.id))
    
    return render_template('clients/create.html')

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    client = Client.query.get_or_404(id)
    if request.method == 'POST':
        client.name = request.form['name']
        client.email = request.form['email']
        client.phone = request.form['phone']
        client.company = request.form.get('company', '')
        client.notes = request.form.get('notes', '')
        db.session.commit()
        flash('Client updated successfully!', 'success')
        return redirect(url_for('clients.view', id=client.id))
    
    return render_template('clients/edit.html', client=client)    