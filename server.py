from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)

app.config["SECRET_KEY"] = "Elefantengeheimnis"

socketio = SocketIO(app)

if __name__ == "__main__" :
    socketio.run(app, port = 1337, debug = True)
    print("server started")