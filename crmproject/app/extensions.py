from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager  # The class

# Create instances
db = SQLAlchemy()
login_manager = LoginManager()  # The instance we'll use everywhere

# You can add extension configurations here if needed
login_manager.login_view = 'auth.login'  # Set the login view
login_manager.login_message_category = 'info'  # Set flash message category