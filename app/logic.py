import copy

from app import structures

def getMove(data):
    """
    Goals:
        - eat food / a*
        - kill other snakes
        - chase tail / defense
    """
    game = structures.Game(data)

    # if game.me.health < 50:
    #     return eat()
    # else:

    safeMoves = sorted(game.getSafeMoves(game.me.head), key=lambda p: getAreaSize(game, p))

    if safeMoves:
        return game.directionFromHead(safeMoves[-1])
    else:
        print("No safe moves!")
        return "up"

# used to move towards the bigger area so you don't get stuck
# TODO: don't run function if points in same area
def getAreaSize(game: structures.Game, p: structures.Point):
    visited = set([p.tup])

    def bfs(point: structures.Point):
        if not game.isSafe(point):
            return

        for neighbour in game.getSafeMoves(point):
            if neighbour.tup not in visited:
                visited.add(neighbour.tup)
                bfs(neighbour)
    
    return len(visited)

# def eat():
#     # a* towards the closest food
#     pass

# def a_star(game: Game):
#     pass
