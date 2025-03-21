from app import app, db
from flask import jsonify, request, session, make_response
from flask_login import login_user, login_required, current_user
from werkzeug.security import check_password_hash
from app.models import Note, User



@app.route('/api', methods=['GET'])
def api_info():
    return jsonify({
        "message": "API der MyNotes Applikation",
        "endpoints": {
            "/api/login": {
                "method": "POST",
                "auth_required": False,
                "description": "Gibt das Session Cookie für die andern Endpunkte"
            },
            "/api/my_notes": {
                "method": "GET",
                "auth_required": True,
                "description": "Gibt alle Notizen des aktuell eingeloggten Nutzers zurück."
            },
            "/api/add_note": {
                "method": "POST",
                "auth_required": True,
                "description": "Fügt eine neue Notiz hinzu. Erwartet JSON mit 'title' und 'content'."
            },
            "/api/delete_note/<note_id>": {
                "method": "DELETE",
                "auth_required": True,
                "description": "Löscht eine Notiz mit der gegebenen ID, sofern sie dem eingeloggten Nutzer gehört."
            }
        }
    }), 200

#Postman API zum erhalten des Session Cookies
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username und Passwort erforderlich'}), 400

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        response = make_response(jsonify({'message': 'Login erfolgreich'}), 200)
        response.set_cookie('session', session.get('_id', ''), httponly=True)
        return response

    return jsonify({'error': 'Ungültiger Benutzername oder Passwort'}), 401


#Suche nach all meinen notizen
@app.route('/api/my_notes', methods=['GET'])
@login_required
def get_my_notes():
    notes = Note.query.filter_by(user_id=current_user.id).all()
    result = [{
        'id': note.id,
        'title': note.title,
        'content': note.content,
        'created_at': note.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': note.updated_at.strftime('%Y-%m-%d %H:%M:%S')
    } for note in notes]
    return jsonify(result), 200

#API um neue Notiz hinzuzufügen
@app.route('/api/add_note', methods=['POST'])
@login_required
def api_add_note():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({'error': 'Titel und Content sind erforderlich'}), 400

    note = Note(title=title, content=content, user_id=current_user.id)
    db.session.add(note)
    db.session.commit()

    return jsonify({'message': 'Notiz erfolgreich erstellt', 'note_id': note.id}), 201

#API zum löschen einer Notiz
@app.route('/api/delete_note/<int:note_id>', methods=['DELETE'])
@login_required
def api_delete_note(note_id):
    note = Note.query.get_or_404(note_id)

    if note.user_id != current_user.id:
        return jsonify({'error': 'Löschen anderer Leute Notizen ist nicht erlaubt'}), 403
    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': 'Notiz gelöscht'}), 200