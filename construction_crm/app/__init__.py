from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate  # Add this import
from app.clients.routes import bp as clients_bp
app.register_blueprint(clients_bp, url_prefix='/clients')

db = SQLAlchemy()
login = LoginManager()
migrate = Migrate()  # Initialize migrate here

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    
    # Initialize database
    db.init_app(app)
    
    # Import and register blueprints AFTER db initialization
    from app.clients.routes import bp as clients_bp
    from app.utilisateurs.routes import bp as utilisateurs_bp
    from app.projets.routes import bp as projets_bp
    
    app.register_blueprint(clients_bp)
    app.register_blueprint(utilisateurs_bp)
    app.register_blueprint(projets_bp)
    
    return app