import logging
import time
import threading
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, send
from configure import get_configuration, configure_inject
from server.game_server import GameServerNamespace
# from game_room import GameRoom

app = Flask(__name__)
conf = get_configuration()

# logging.basicConfig(level=logging.INFO)
logging.info("Starting up game service")
logging.info(conf)

configure_inject(conf)

app.config['SECRET_KEY'] = conf.game_secret

socketio = SocketIO(app, cors_allowed_origins="*")


# @socketio.on('connect')
# def test_connect():
#     print("CONNECTION")
#     socketio.emit('player_update', {'data': 'Connected'})


# @socketio.on('join')
# def on_join(data):
#     game_id = data['game_id']

#     join_room(game_id)

#     print(data)

#     socketio.emit('data', data, room=game_id)


# @socketio.on('leave')
# def on_leave(data):
#     game_id = data['game_id']
#     leave_room(game_id)
#     socketio.emit('data', data, room=game_id)


# @socketio.on('data')
# def handle_my_custom_event(data):
#     print('received my event: ', data, type(data))
#     game_id = data['game_id']

#     socketio.emit('data', data, room=game_id)


if __name__ == "__main__":

    socketio.on_namespace(GameServerNamespace('/'))
    socketio.run(app, debug=True, host='0.0.0.0')
