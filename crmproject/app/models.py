from app.extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Utilisateur(UserMixin, db.Model):
    __tablename__ = 'utilisateurs'
    
    id = db.Column(db.Integer, primary_key=True)
    nom_utilisateur = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    mot_de_passe_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='employé')
    
    def set_password(self, password):
        self.mot_de_passe_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.mot_de_passe_hash, password)

    def __repr__(self):
        return f'<Utilisateur {self.username}>'
        
class Client(db.Model):
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    telephone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    entreprise = db.Column(db.String(120))
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'))
    
    def __repr__(self):
        return f'<Client {self.nom}>'

class Journal(db.Model):
    __tablename__ = 'journal'
    
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(200))
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'))
    
    def __repr__(self):
        return f'<Journal {self.action[:20]}>'
        
class Projet(db.Model):
    id = db.Column(db.Integer, primary_key=True)        
        
# Create alias for backward compatibility
User = Utilisateur        

@login_manager.user_loader  # Changed to login_manager
def load_user(id):
    return Utilisateur.query.get(int(id))