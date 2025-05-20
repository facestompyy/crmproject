from flask import Flask
from .extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)  # Correct: using the instance
    
    # Import models AFTER db initialization
    from .models import Utilisateur
    from .routes import main
    from .routes import auth
    
    # Setup user loader HERE where everything is available
    @login_manager.user_loader  # Correct: using the instance
    def load_user(user_id):
        return Utilisateur.query.get(int(user_id))
    
    # Import and register blueprints
    from .routes import clients, utilisateurs, projets
    app.register_blueprint(clients.bp)
    app.register_blueprint(utilisateurs.bp)
    app.register_blueprint(projets.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp, url_prefix='/auth')
    
    return app