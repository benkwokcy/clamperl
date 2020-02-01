from app import structures

def get_move(data):
    game = structures.Game(data)
    return game.getSafeMoves()[0]
