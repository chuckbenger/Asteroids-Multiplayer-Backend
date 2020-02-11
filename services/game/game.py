import logging
from flask import Flask
from flask_socketio import SocketIO
from configure import get_configuration, configure_inject
from server.game_server import GameServerNamespace


app = Flask(__name__)
conf = get_configuration()

logging.info("Starting up game service")
logging.info(conf)

configure_inject(conf)

app.config['SECRET_KEY'] = conf.game_secret

socketio = SocketIO(app, cors_allowed_origins="*")

if __name__ == "__main__":

    socketio.on_namespace(GameServerNamespace('/'))
    socketio.run(app, debug=True, host='0.0.0.0')
