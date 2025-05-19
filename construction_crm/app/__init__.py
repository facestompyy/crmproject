from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.extensions import db, login_manager

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)  # Changed to login_manager
    login_manager.login_view = 'utilisateurs.login'  # Changed to login_manager
    
    # Register all blueprints
    from app.routes import (
        auth,
        clients,
        main,
        projets,
        utilisateurs
    )
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(clients.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(projets.bp) 
    app.register_blueprint(utilisateurs.bp)
    
    
    return app