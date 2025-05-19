from flask import Blueprint, render_template
from app.extensions import db
from app.models import Client

bp = Blueprint('clients', __name__)

@bp.route('/clients')
def list_clients():
    clients = Client.query.all()
    return render_template('clients/index.html', clients=clients)