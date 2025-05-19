from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login = LoginManager()

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    login.init_app(app)
    login.login_view = 'auth.login'
    
    # Import and register blueprints
    from app.auth.routes import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.clients.routes import bp as clients_bp
    app.register_blueprint(clients_bp, url_prefix='/clients')
    
    from app.main.routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    return app

# Import models after app creation to avoid circular imports
from app import models