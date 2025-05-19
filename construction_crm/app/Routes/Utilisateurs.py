from flask import Blueprint
from app.extensions import db
from app.models import Utilisateur

bp = Blueprint('utilisateurs', __name__)

@bp.route('/login')
def login():
    return "Login page"