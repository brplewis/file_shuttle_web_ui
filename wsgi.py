from washington import create_app
from flask_socketio import SocketIO

app = create_app()
app.config.from_object('config.ProdConfig')
socketio= SocketIO(app)


if __name__ == "__main__":
    socketio.app()
    #app.run(host='0.0.0.0')
