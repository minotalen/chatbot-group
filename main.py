import sys
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send, emit
import json
import threading

sys.path.insert(1, '/modules')
from modules.answerhandler_json import answerHandler
import modules.database_SQLite as database

app = Flask(__name__, static_url_path='/static')

app.config["SECRET_KEY"] = "x!\x84Iy\xf9#gE\xedBQqg+\xf3A+\xe3\xd3\x01\x1a\xdf\xd2"

socketio = SocketIO(app, ping_timeout=1000, ping_interval=25)
socketio.init_app(app, cors_allowed_origins="*")

user_sessions = []

@app.route('/')
def send_index_page():
    username = session.get('username')
    if username:

        print(username)
        if username:  # database.is_user_logged_in(username):
            return redirect(url_for('send_play_page', username=username))

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
            session['username'] = username
            session['is_logged_in'] = True
            return redirect(url_for('send_play_page', username=username))
        else:
            return render_template('login.html', error_message='username and password do not match.')
    else:
        username = session.get('username')
        if username:

            print(username)
            if username:
                return redirect(url_for('send_play_page', username=username))
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
            return redirect(url_for('send_play_page', username= username))
        else:
            return render_template('signup.html', error_message='Username already taken. Please choose another one.')
    else:
        return render_template('signup.html')


@app.route('/settings', methods=['GET','POST'])
def get_user_settings():
    if request.method == 'POST':
        settings_data = request.get_data()
        print('settings data received')

        update_settings_by_jsondata(settings_data)
        return settings_data
    else:
        username = session.get('username')
        if username:
            settings = database.get_settings_by_username(username)
            print('return settings')
            print(settings)

            if settings:
                return settings
            else:
                return ""
        return ""

@app.route('/profile')
def send_profile_page():
    username = session.get('username')

    if username:
        return render_template('user.html', username=username)
    else:
        print('no user is logged in (username source: session)')
        return redirect(url_for('login'))


@app.route('/play')
def send_play_page():
    username = session.get('username')

    if username:
        return render_template('play.html', username=username)
    else:
        print('no user is logged in (username source: session)')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    username = session.get('username')
    print(username)

    if username:
        session.pop('username', None)
        session.pop('is_logged_in', None)
        print(username + ' has been logged out')
        return redirect(url_for('login'))
    else:
        print('no user is logged in (username source: session)')
        return redirect(url_for('login'))


@app.errorhandler(404)
def show_error_page(error, error_code=404):
    print(error)
    return render_template('error.html', error=error, error_code=error_code)

@app.errorhandler(500)
def handle_error_500(error):
    error = 'error 500: internal server error'
    return show_error_page(error,500)


@socketio.on('json')
def handleJson(payload):
    print("sending: " + payload)
    try:
        """
        que = Queue.Queue()

        t = Thread(target=lambda q, arg1: q.put(foo(arg1)), args=(payload, get_username_by_sid(request.sid)))
        t.start()
        t.join()
        send(que.get(), json=True)
        """
        send(answerHandler(payload, get_username_by_sid(request.sid)), json=True)
    except:
        obj = json.loads(payload)
        print("Unexpected error:", sys.exc_info()[1])
        print("Traceback:", sys.exc_info()[2])
        print("Type:", sys.exc_info()[0])
        send(json.dumps({"level": obj['level'], "sender": "bot", "room": obj['room'], "mode": obj['mode'], "message": "Sorry, something went wrong on the server. Try something different."}),  json=True)

 
@socketio.on('username')
def mapsUsernameToSession(payload):
    username = payload

    user_sessions.append({"user": username, "sid": request.sid}) 

    initial_data = {"level": 0, "sender": "bot", "room": "startgame", "mode": "game", 
                    "message": "Welcome "+ username + "!"} 
    json_data = json.dumps(initial_data) 
    send(json_data, json=True) 

    intro_text = {"level": 0, "sender": "bot", "room": "startgame", "mode": "game", "message": "current room"} 
    json_data = json.dumps(intro_text) 
    send(answerHandler(json_data, get_username_by_sid(request.sid)), json=True) 


@socketio.on('connect') 
def connect(): 
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

def update_settings_by_jsondata(payload):
    readable_json = json.loads(payload)
    username = readable_json["username"]
    database.update_user_settings(username, payload)


if __name__ == "__main__":
    print("Trying to start server...")
    socketio.run(app, host='0.0.0.0', debug=True)
