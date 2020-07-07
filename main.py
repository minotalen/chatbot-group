from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send, emit
import json
import database_SQLite as database
from answerhandler_json import answerHandler
import sys

app = Flask(__name__, static_url_path='/static')

app.config["SECRET_KEY"] = "x!\x84Iy\xf9#gE\xedBQqg+\xf3A+\xe3\xd3\x01\x1a\xdf\xd2"

socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

user_sessions = []


@app.route('/')
def send_index_page():
    username = session.get('username')
    if username:

        print(username)
        if username:  # database.is_user_logged_in(username):
            return redirect(url_for('send_profile_page'))

    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print('username: ' + username)
        print('password: ' + password)

        if database.is_user_valid(username, password):
            """if database.is_user_logged_in(username):
                return render_template('login.html', error_message='user already logged in on another device.')
            else:"""
            # database.update_login(username, True)
            session['username'] = username
            session['is_logged_in'] = True
            return redirect(url_for('send_profile_page', username=username))
        else:
            return render_template('login.html', error_message='username and password do not match.')
    else:
        username = session.get('username')
        if username:

            print(username)
            if username:  # database.is_user_logged_in(username):
                return redirect(url_for('send_profile_page'))
        else:
            return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        r_password = request.form['repeat-password']

        print('username: ' + username)
        print('password: ' + password)
        print('repeat password: ' + r_password)

        if password != r_password:
            return render_template('signup.html',
                                   error_message='Entered passwords do not match. Please make sure to enter identical passwords.')
        userExists = database.does_user_exist(username)
        if not userExists:
            database.add_user(username, password)
            session['username'] = username
            return redirect(url_for('send_profile_page', username=username))
        else:
            return render_template('signup.html', error_message='Username already taken. Please choose another one.')
    else:
        return render_template('signup.html')


@app.route('/settings', methods=['GET', 'POST'])
def get_user_settings():
    data = request.get_json()


@app.route('/profile')
def send_profile_page():
    username = session.get('username')

    if username:  # database.is_user_logged_in(username):
        return render_template('user.html', username=username)
    else:
        print('no user is logged in (username source: session)')
        return redirect(url_for('login'))


@app.route('/play')
def send_play_page():
    username = session.get('username')

    if username:  # database.is_user_logged_in(username):
        return render_template('play.html', username=username)
    else:
        print('no user is logged in (username source: session)')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    username = session.get('username')
    print(username)

    if username:  # and database.is_user_logged_in(username):
        session.pop('username', None)
        session.pop('is_logged_in', None)
        # database.update_login(username, False)
        print(username + ' has been logged out')
        return redirect(url_for('login'))
    else:
        print('no user is logged in (username source: session)')
        return redirect(url_for('login'))


@socketio.on('json')
def handleJson(payload):
    print("sending: " + payload)
    try:
        send(answerHandler(payload, get_username_by_sid(request.sid)), json=True)
    except:
        obj = json.loads(payload)
        print("Unexpected error:", sys.exc_info()[1])
        print("Traceback:", sys.exc_info()[2])
        print("Type:", sys.exc_info()[0])
        send(json.dumps({"level": obj['level'], "sender": "bot", "room": obj['room'], "mode": obj['mode'], "message": "Sorry, something went wrong on the server. Try something different."}),  json=True)

@socketio.on('user_registration')
def update_users(payload):
    readable_json = json.loads(payload)

    database.insert_user(readable_json['message'], '123456')
    user_sessions.append({"user": readable_json['message'], "sid": request.sid})
    initial_data = {"level": 0, "sender": "bot", "room": "startgame", "mode": "game",
                    "message": "Hello, " + readable_json['message'] + "!"}
    json_data = json.dumps(initial_data)
    send(json_data, json=True)
    intro_text = {"level": 0, "sender": "bot", "room": "startgame", "mode": "game", "message": "current room"}
    json_data = json.dumps(intro_text)
    send(answerHandler(json_data, get_username_by_sid(request.sid)), json=True)


@socketio.on('connect')
def connect():
    """ (KK) TODO Move this content to a custom event, e.g. play"""
    initial_data = {"level": 0, "sender": "bot", "room": "startgame", "mode": "game",
                    "message": "Welcome! Insert username."}
    json_data = json.dumps(initial_data)
    send(json_data, json=True)
    print("You are now connected with the server")


@socketio.on('disconnect')
def disconnect():
    user_sessions.remove({"user": get_username_by_sid(request.sid), "sid": request.sid})
    print(user_sessions)
    print("You are disconneced from the server")


@socketio.on_error()
def error_handler(e):
    raise Exception("Some error happened, no further notice")


def get_username_by_sid(sid):
    for users in user_sessions:
        if sid == users['sid']:
            return users['user']


def get_current_username():
    return get_username_by_sid(request.sid)


def get_settings_by_username(username: str):
    if database.does_setting_exist(username):
        data = database.find_settings_by_username(username)
        initial_data = {"username": data[1], "json": data[2]}
        json_data = json.dumps(initial_data)
        return json_data


def update_settings_by_jsondata(payload):
    readable_json = json.loads(payload)
    username = readable_json["username"]
    database.update_user_settings(username, payload)


if __name__ == "__main__":
    print("Trying to start server...")
    socketio.run(app, host='0.0.0.0', debug=True)
