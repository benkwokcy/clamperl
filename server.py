"""Bottle/Cheroot web server implementing the Battlesnake 2020 API."""

import json
import os

import bottle
from cheroot import wsgi

from app.logic import getMove

@bottle.post('/start')
def start():
    """Notifies your snake that it is participating in a new game."""
    return bottle.HTTPResponse(
        status = 200,
        headers = {
            "Content-Type": "application/json"
        },
        body = json.dumps({
            "color": "#979ed8",
            "headType": "tongue",
            "tailType": "round-bum"
        })
    )

@bottle.post('/move')
def move():
    """Updates your snake with the current state of the game board and asks for a move."""
    data = bottle.request.json
    # print(json.dumps(data)) # LOGGING
    direction,_ = getMove(data)

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

class CherryPyServer(bottle.ServerAdapter):
    """Credit to Jon Knoll for the suggestion to use CherryPy."""
    def run(self, handler):
        server = wsgi.Server((self.host, self.port), handler)
        try:
            server.start()
        finally:
            server.stop()

application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host = os.getenv('IP', '0.0.0.0'),
        port = os.getenv('PORT', '8080'),
        debug = os.getenv('DEBUG', True),
        server = CherryPyServer
    )
    print(f"clamperl is running on port {os.getenv('PORT', '8080')}")
