"""Implements the logic for the /move endpoint in server.py"""

import heapq
import time
from enum import Enum, auto
from typing import List

from pathos.multiprocessing import ProcessingPool

from app import structures

POOL = ProcessingPool(3)

class Mode(Enum):
    """These values are used in test.py to see if the snake is doing what I expect."""
    hungry = auto()
    grow = auto()
    defend = auto()
    random = auto()

def getMove(data: dict) -> (structures.Direction, Mode):

    """Parent function for deciding the next move."""
    game = structures.Game(data)

    # Eat when food dips below threshold or our size is smaller than the average enemy
    smallerThanAverage = game.enemies and (game.me.size <= (sum([e.size for e in game.enemies]) / len(game.enemies)))
    if game.me.health < 50 or smallerThanAverage:
        # start_time = time.time() # RUNTIME LOGGING
        move = eat(game)
        # print("Eat took %f seconds" % (time.time() - start_time)) # RUNTIME LOGGING
        if move:
            return (move, Mode.hungry if game.me.health < 50 else Mode.grow)

    # Take the safest move.
    # start_time = time.time() # RUNTIME LOGGING
    move = defend(game)
    # print("Defend took %f seconds" % (time.time() - start_time)) # RUNTIME LOGGING
    if move:
        return (move, Mode.defend)

    # No moves where we survive.
    move = structures.Direction.randomDirection()
    return (move, Mode.random)

def eat(game: structures.Game) -> str:
    """Move towards food that is reachable, nearby, and in a big open area."""

    # take riskier paths to the food if we're starving
    firstMoveMood = structures.Mood.SAFE if game.me.health > 10 else structures.Mood.RISKY 
    remainingMoveMood = structures.Mood.SAFE if game.me.health > 25 else structures.Mood.RISKY
    validHeadMoves = game.getMoves(game.me.head, structures.Mood.RISKY)

    points = []
    for point in game.food:
        if any([game.uf.connected(x, point) for x in validHeadMoves]): # food is reachable
            if game.uf.getSize(point) < game.me.size and game.me.health > 25: # avoid areas smaller than us if not that hungry
                continue
            points.append(point)

    paths = POOL.map(game.aStar, points, [firstMoveMood] * len(points), [remainingMoveMood] * len(points))
    paths = [p for p in paths if p and len(p) <= game.me.health] # if len(path) is greater, we'll die before we get there

    if not paths:
        return None
    
    maxDistance = max([len(p) for p in paths])

    def score(path: List[structures.Point]) -> structures.Point:
        """We want the closest food that is also in a big open area."""

        # these are normalized to [0,1]
        dist = len(path) / maxDistance
        areaSize = game.uf.getSize(path[0]) / (game.height * game.width)

        if game.me.health < 20:
            return (0.4 * (1 - dist)) + (0.6 * areaSize) # prioritize closer food if health is getting low
        else:
            return (0.3 * (1 - dist)) + (0.7 * areaSize) # otherwise, care more about area size

    bestMove = max(paths, key=score)[0]
    bestMove = game.directionFromHead(bestMove)

    # print(f"game {game.id[:5]} - turn {game.turn} - eat {bestMove}") # TODO

    return bestMove

def defend(game: structures.Game) -> str:
    """Go to the safest location."""
    moves = game.getMoves(game.me.head, structures.Mood.RISKY)
    if not moves:
        return None

    def _key(p: structures.Point, g: structures.Game) -> int:
        risk = structures.getRisk(g.getState(p))
        normalizedAreaSize = g.uf.getSize(p) / (g.height * g.width)
        futureScore = g.simulateMove(p)
        return max(risk,futureScore) - normalizedAreaSize
    
    scores = POOL.map(_key, moves, [game] * len(moves))
    bestMove = moves[scores.index(min(scores))]
    bestMove = game.directionFromHead(bestMove)

    # print(f"game {game.id[:5]} - turn {game.turn} - defend {bestMove}") # TODO

    return bestMove
