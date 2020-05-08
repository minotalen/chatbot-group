from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
import json

app = Flask(__name__, static_url_path='/static')

app.config["SECRET_KEY"] = "Elefantengeheimnis"

socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

users = []

@app.route('/')
def send_index_page():
    return render_template('index.html')

@socketio.on('json')
def handleJson(payload):
    print("sending: " + payload)
    send(payload,json=True)


@socketio.on('user_registration')
def update_users(payload):
    users.append({"user_id" : request.sid, "user_name" : payload['message']})
    print("added user: " + payload['message'] + "with session id: " + request.sid)

@socketio.on('username', namespace='/private')
def receive_username(username):
    users.append({username : request.sid})
    print(users)

@socketio.on('connect')
def connect():
    initial_data = {"level": 1,"sender": "server","room":"First Hallway","items":[],"message": "Welcome!"}
    json_data = json.dumps(initial_data)
    send(json_data, json=True)
    print("You are now connected with the server")

@socketio.on('disconnect')
def disconnect():
    print("You are disconneced from the server")

@socketio.on_error()
def error_handler(e):
    raise Exception("Some error happened, no further notice")

if __name__ == "__main__" :
    print("Try to start server...")
    socketio.run(app, host='0.0.0.0',debug = True)

