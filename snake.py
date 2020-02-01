import enum, collections
import data_structures

def get_move(data):
    game = data_structures.Game(data)
    return game.getSafeMoves()[0].name