#Beim erstellen der html seiten habe ich nach besseren wegen gesucht die einzelnen forms zu handeln. 
#Chatgpt hat mir eine die idee gegeben die einzelnen forms in eine eigene Datei zu verlagern die danach wieder eingebunden werden können. dadurch müssen nicht 100 verschiedene html seiten erstellt werden 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from app import login_manager

# definitionen für die Felder der verschiedenen Formulare (login von hand)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    #Passwortmindestlänge 6 hinzugefügt
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class NoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
    tags = StringField('Tags (comma-separated)')
    submit = SubmitField('Save Note')

class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')