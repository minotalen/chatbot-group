from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
from flask_cors import CORS
import json
import csv
from answerhandler import answerHandler

# from answerhandler_withdatabase import answerHandler

app = Flask(__name__, static_url_path='/static')

app.config["SECRET_KEY"] = "x!\x84Iy\xf9#gE\xedBQqg+\xf3A+\xe3\xd3\x01\x1a\xdf\xd2"
cors = CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app)
# socketio.init_app(app, cors_allowed_origins='*')

users = []


@app.route('/')
def send_index_page():
    return render_template('index.html')


@socketio.on('json')
def handleJson(payload):
    print("sending: " + payload)
    send(answerHandler(payload), json=True)


@socketio.on('user_registration')
def update_users(payload):
    readable_json = json.loads(payload)
    users.append(
        {"user_id": request.sid, "user_name": readable_json['message']})
    initial_data = {"level": 1, "sender": "bot", "room": "Introduction", "items": [
    ], "message": "Hello, " + readable_json['message'] + "!"}
    json_data = json.dumps(initial_data)
    send(json_data, json=True)
    intro_text = {"level": 1, "sender": "bot",
                  "room": "Introduction", "items": [], "message": "current room"}
    json_data = json.dumps(intro_text)
    send(answerHandler(json_data), json=True)
    print("added user: " +
          readable_json['message'] + " with session id: " + request.sid)


@socketio.on('connect')
def connect():
    initial_data = {"level": 1, "sender": "bot",
                    "room": "First Hallway", "items": [], "message": "Welcome!"}
    json_data = json.dumps(initial_data)
    send(json_data, json=True)
    print("You are now connected with the server")


@socketio.on('disconnect')
def disconnect():
    print("You are disconneced from the server")


@socketio.on_error()
def error_handler(e):
    raise Exception("Some error happened, no further notice")


# with open('rooms.csv') as csv_file:
#     roomreader = csv.reader(csv_file)
#     rows = list(roomreader)
#     print(rows[1])


if __name__ == "__main__":
    print("Try to start server...")
    socketio.run(app, host='elephanture.informatik.uni-bremen.de',
                 port=5000, debug=True)
