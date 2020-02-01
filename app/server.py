import json
import os

import bottle

from logic import get_move

# Not used
@bottle.route('/')
def index():
    return "Available endpoints: /start /end /move /ping"

# The engine is asking your snake if it is alive
@bottle.post('/ping')
def ping():
    return bottle.HTTPResponse(status = 200)

# Notifies your snake that it is participating in a new game
@bottle.post('/start')
def start():
    return bottle.HTTPResponse(
        status = 200,
        headers = {
            "Content-Type": "application/json"
        },
        body = json.dumps({
            "color": "#d897cb",
            "headType": "tongue",
            "tailType": "round-bum"
        })
    )

# Updates your snake with the current state of the game board and asks for a move
@bottle.post('/move')
def move():
    data = bottle.request.json
    direction = get_move(data)

    return bottle.HTTPResponse(
        status = 200,
        headers = {
            "Content-Type": "application/json"
        },
        body = json.dumps({
            "move": direction
        })
    )

# Notifies your snake that the game is over.
@bottle.post('/end')
def end():
    return bottle.HTTPResponse(status = 200)

application = bottle.default_app() # this is needed by gunicorn for some reason

if __name__ == '__main__':
    bottle.run(
        application,
        host = os.getenv('IP', '0.0.0.0'),
        port = os.getenv('PORT', '8080'),
        debug = os.getenv('DEBUG', True)
    )
    print(f"huntail is running on port {os.getenv('PORT', '8080')}")
