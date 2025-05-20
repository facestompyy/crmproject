from flask import Flask
from .extensions import db, login_manager  # Changed to relative import

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Import blueprints
    from app.routes.clients import bp as clients_bp
    from .routes.utilisateurs import bp as utilisateurs_bp
    from .routes.projets import bp as projets_bp
    
    # Register blueprints
    app.register_blueprint(clients_bp, url_prefix='/clients')
    app.register_blueprint(utilisateurs_bp)
    app.register_blueprint(projets_bp)
    
    return app