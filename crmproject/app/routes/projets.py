from flask import Blueprint
from app.extensions import db
from app.models import Projet

bp = Blueprint('projets', __name__)

@bp.route('/projets')
def list_projets():
    return "Projects list"