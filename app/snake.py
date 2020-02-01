import enum, collections
from app import classes

def get_move(data):
    game = classes.Game(data)
    return game.getSafeMoves()[0]