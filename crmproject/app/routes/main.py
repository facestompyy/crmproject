from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template('main/home.html')  # You already have this template

@bp.route('/favicon.ico')
def favicon():
    return '', 404  # Simple 404 response for favicon