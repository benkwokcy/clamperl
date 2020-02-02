"""Bottle/Gunicorn web server implementing the Battlesnake 2020 API."""

import json
import os

import bottle

from app import logic

@bottle.post('/start')
def start():
    """Notifies your snake that it is participating in a new game."""
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

@bottle.post('/move')
def move():
    """Updates your snake with the current state of the game board and asks for a move."""
    data = bottle.request.json
    direction = logic.getMove(data)

    return bottle.HTTPResponse(
        status = 200,
        headers = {
            "Content-Type": "application/json"
        },
        body = json.dumps({
            "move": direction
        })
    )

@bottle.post('/end')
def end():
    """Notifies your snake that the game is over."""
    return bottle.HTTPResponse(status = 200)

@bottle.post('/ping')
def ping():
    """The engine is asking your snake if it is alive"""
    return bottle.HTTPResponse(status = 200)

@bottle.route('/')
def index():
    """Not used by the game server."""
    return "Available endpoints: /start /end /move /ping"

application = bottle.default_app() # this is needed by gunicorn for some reason

if __name__ == '__main__':
    bottle.run(
        application,
        host = os.getenv('IP', '0.0.0.0'),
        port = os.getenv('PORT', '8080'),
        debug = os.getenv('DEBUG', True)
    )
    print(f"huntail is running on port {os.getenv('PORT', '8080')}")
