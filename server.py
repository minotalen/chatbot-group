from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)

app.config["SECRET_KEY"] = "Elefantengeheimnis"

socketio = SocketIO(app)

if __name__ == "__server__" :
    socketio.run(app)
    print("server started")