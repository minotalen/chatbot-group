from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__, static_url_path='/static')

app.config["SECRET_KEY"] = "Elefantengeheimnis"

socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

@app.route('/')
def send_index_page():
    return render_template('index.html')

@socketio.on('message')
def handleMessage(msg): 
	print('Message: ' + msg)
	send(msg, broadcast=True)

@socketio.on('connect')
def connect():
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
