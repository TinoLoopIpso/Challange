#Datenbankschemen grob wie Seite 66 aus dem Webapplikationen mit Flask PDF
from datetime import datetime
from flask_login import UserMixin
#TODO: löschen from app import db, login_manager
from app import login_manager, db

#Initiale Idee war das DB schema mit UserMixin zu erleichtern. Empfehlung durch Stackoverflow.
#Da nicht wirklich funktionabel 

#Verknüpft Session mit BenutzerID
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

#Usertabelle +UserMixin setup
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, nullable=False)
    #nullable hinzugefügt aufgrund eines testfehlers mit leerer emailadresse
    password_hash = db.Column(db.String(128))
    notes = db.relationship('Note', backref='author', lazy='dynamic')

#Datenbank für Notizen 
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

