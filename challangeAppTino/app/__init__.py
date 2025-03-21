#imports im init eingezogen (von config)
import os

#import logging stuff
import logging
from logging.handlers import RotatingFileHandler

#Imports nach Seite 62
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
#login_manager handelt sessions
from flask_login import LoginManager



login_manager = LoginManager()
#weiteres die Session handeln/sql --> nach models verschoben, ergibt da mehr sinn (nach testing zu löschen)
#from flask_login import LoginManager
#überbleibsel für weiterentwicklung ausserhalb des Schulprojekts. (aus scope/zeitgründen so gut als möglich entfernt, import bleibt da ich kurz vor abgabe die anzahl errors nicht beheben konnte)
#from sqlalchemy.orm import DeclarativeBase


#Selber startup wie anleitung seite 62
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Starten des loggers 
if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/mynotes.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
app.logger.setLevel(logging.INFO)
app.logger.addHandler(file_handler)    
app.logger.info('Challange App Tino wird gestartet')



#Login Handler
login_manager.init_app(app)



from app.models import User
#Verknüpft Session mit BenutzerID
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
login_manager.login_view = 'login'


from app import models, routes, api