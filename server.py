from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)

app.config["SECRET_KEY"] = "Elefantengeheimnis"

socketio = SocketIO(app)

if __name__ == "__main__" :
    print("Try to start server...")
    socketio.run(app, debug = True)

@socketio.on('connect')
def connect():
    print("You are now connected with the server")

@socketio.on('disconnect')
def disconnect():
    print("You are disconneced from the server")

@socketio.on_error()
def error_handler(e):
    raise Exception("Some error happened, no further notice")


