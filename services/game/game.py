import logging
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, send
from configure import get_configuration, configure_inject

app = Flask(__name__)
conf = get_configuration()

# logging.basicConfig(level=logging.INFO)
logging.info("Starting up game service")
logging.info(conf)

configure_inject(conf)

app.config['SECRET_KEY'] = conf.game_secret

socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/')
def sessions():
    return render_template('session.html')


@socketio.on('connect')
def test_connect():
    print("CONNECTION")
    socketio.emit('player_update', {'data': 'Connected'})


@socketio.on('join')
def on_join(data):
    # username = data['username']
    game = data['game']
    join_room(game)
    print(f"has joined the room")


@socketio.on('leave')
def on_leave(data):
    # username = data['username']
    game = data['game']
    leave_room(game)
    print(f"has left the room")


@socketio.on('my event')
def handle_my_custom_event(json):
    print('received my event: ', json, type(json))
    # game = json['game']
    socketio.emit('my event', json)


if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0')
