#Quellen für hilfe beim erstellen der Endpunkte übers ganze internet sowie inspiration vom Microblog Dokumentation. 

from app import app, db, login_manager
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, Note
from app.forms import RegistrationForm, NoteForm, SearchForm

# Startseite (leitet auf das Notizen weiter)
@app.route('/')
def index():
    return redirect(url_for('notizen'))



#Registrierungsendpunkt Endpunkt mehr oder weniger anhand der schulvorlage
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
    # Route /register wurde mit POST betreten. Prüfung, ob alles o.k. ist:
    #hinzugefügt: prüfen ob der User existiert. 
        if User.query.filter_by(username=form.username.data).first():
            flash('User existiert bereits', 'danger')
            return render_template('register.html', form=form)
    #FAlls nicht, User hinzufügen
        user = User(username=form.username.data, email=form.email.data, password_hash=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    # Route /register wurde mit GET betreten
    return render_template('register.html', title='Register', form=form)


# Login, leicht abgewandelte version des im PDF existierenden
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('notizen'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        #Abgewandelt, da passwort hash probleme machte. // verifikation über username nicht email
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            app.logger.info('login des User: %s erfolgreich', current_user.username)
            return redirect(url_for('notizen'))
        flash('Ungültiger Benutzername oder Passwort', 'danger')
        app.logger.info('loginversuch ungültiger User: %s', current_user.username)
    return render_template('login.html')


# Endpunkt für Logout
@app.route('/logout')
@login_required
def logout():
    _username=current_user.id
    app.logger.info('logout User: %s', current_user.username)
    logout_user()
    flash('Erfolgreich ausgeloggt.', 'info')
    return redirect(url_for('login'))

# Notizen anzeigen
@app.route('/notizen')
@login_required
def notizen():
    #Alle notizen des Nutzers
    notizen = Note.query.filter_by(user_id=current_user.id).all()
    return render_template('notizen.html', Note=Note, user=current_user)

# neue Notiz hinzufügen
@app.route('/add_note', methods=['POST'])
@login_required
def add_note():
    title = request.form.get('title')
    content = request.form.get('content')

    if not title or not content:
        flash('Titel und Inhalt dürfen nicht leer sein.', 'danger')
        return redirect(url_for('notizen'))

    new_note = Note(
        title=title,
        content=content,
        user_id=current_user.id
    )
    db.session.add(new_note)
    db.session.commit()

    flash('Notiz erfolgreich erstellt!', 'success')
    return redirect(url_for('notizen'))

#Endpunkt zum Editieren einer Notiz
@app.route('/edit_note/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_note(id):
    note = Note.query.get_or_404(id)
    print(note)

    # Verhindern das anderer leute Notizen geändert werden
    if note.user_id != current_user.id:
        flash('Du bist nicht berechtigt, diese Notiz zu bearbeiten.', 'danger')
        return redirect(url_for('notizen'))

    if request.method == 'POST':
        note.title = request.form.get('title')
        note.content = request.form.get('content')
        db.session.commit()
        flash('Notiz erfolgreich bearbeitet.', 'success')
        return redirect(url_for('notizen'))

    return render_template('edit_note.html', note=note, user=current_user)

#Endpunkt zum löschen einer Notiz
@app.route('/delete_note/<int:id>', methods=['GET'])
@login_required
def delete_note(id):
    note = Note.query.get_or_404(id)

    #verhindern das anderer Leute Notizen gelöscht werden
    if note.user_id != current_user.id:
        flash('Du bist nicht berechtigt, diese Notiz zu löschen.', 'danger')
        return redirect(url_for('notizen'))

    db.session.delete(note)
    db.session.commit()
    flash('Notiz gelöscht.', 'success')
    return redirect(url_for('notizen'))

#Endpunkt fürs Debuggen, Zeigt die "flash-Messages" der Session an (nur nützlich wenn Pages aufgerufen werden welche flashmeldungen generieren die nicht angezeigt werden können. TODO: In der Finalen version zu entfernen)
@app.route('/show')
def show():
    return render_template('show.html', user=current_user)



