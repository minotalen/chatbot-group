from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
import json
import database_SQLite as database
from answerhandler_json import answerHandler


app = Flask(__name__, static_url_path='/static')

app.config["SECRET_KEY"] = "x!\x84Iy\xf9#gE\xedBQqg+\xf3A+\xe3\xd3\x01\x1a\xdf\xd2"

socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

user_sessions = []

@app.route('/')
def send_index_page():
    return render_template('index.html')


@socketio.on('json')
def handleJson(payload):
    print("sending: " + payload)
    send(answerHandler(payload, get_username_by_sid(request.sid)), json=True)


@socketio.on('user_registration')
def update_users(payload):
    readable_json = json.loads(payload)
        
    database.insert_user(readable_json['message'], '123456')
    user_sessions.append({"user": readable_json['message'], "sid": request.sid})
    initial_data = {"level": 0, "sender": "bot", "room": "startgame", "mode": "game", "message": "Hello, " + readable_json['message'] + "!"}
    json_data = json.dumps(initial_data)
    send(json_data, json=True)
    intro_text = {"level": 0, "sender": "bot", "room": "startgame", "mode": "game", "message": "current room"}
    json_data = json.dumps(intro_text)
    send(answerHandler(json_data, get_username_by_sid(request.sid)), json=True)


@socketio.on('connect')
def connect():
    initial_data = {"level": 0, "sender": "bot", "room": "startgame", "mode": "game", "message": "Welcome! Insert username."}
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

if __name__ == "__main__":
    print("Try to start server...")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
