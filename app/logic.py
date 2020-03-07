"""Implements the logic for the /move endpoint in server.py"""

import heapq
import time
from enum import Enum, auto
from typing import List

# from pathos.multiprocessing import ProcessingPool  # TODO - MultiProcessing

from app import structures

# POOL = ProcessingPool(3) # TODO - MultiProcessing

class Mode(Enum):
    """These values are used in test.py to see if the snake is doing what I expect."""
    hungry = auto()
    grow = auto()
    defend = auto()
    random = auto()

def getMove(data: dict, snakeName: str) -> (structures.Direction, Mode):

    """Parent function for deciding the next move."""
    game = structures.Game(data, snakeName)

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
    if not game.food:
        return None

    def eatWorker(point: structures.Point, game: structures.Game) -> (structures.Point, float):
        """Given a food location, decide if we should try to eat it and give a score based on its
        distance and safety."""
        # take riskier paths to the food if we're starving
        firstMoveMood = structures.Mood.SAFE if game.me.health > 10 else structures.Mood.RISKY 
        remainingMoveMood = structures.Mood.SAFE if game.me.health > 25 else structures.Mood.RISKY
        validHeadMoves = game.getMoves(game.me.head, firstMoveMood)
        
        if not any([game.uf.connected(x, point) for x in validHeadMoves]): 
            return (None, -1.0) # if food is not reachable in our current mood, ignore this food.
        if game.uf.getSize(point) < game.me.size and game.me.health > 25: 
            return (None, -1.0) # if we are not very hungry and the areas is smaller than us, ignore this food.
        if any([point.distance(s.head) * 3 <= point.distance(game.me.head) for s in game.enemies]) and game.me.health > 10:
            return (None, -1.0) # if we are not starving and the food is 3x closer to another enemy, ignore this food.

        path = game.aStar(point, firstMoveMood, remainingMoveMood)
        
        if not path:
            return (None, -1.0) # if we cannot reach the food using our current mood, ignore this food..
        if len(path) > game.me.health:
            return (None, -1.0) # if we'll die before we reach the food, ignore this food.

        dist = len(path) / game.height if len(path) / game.height <= 1 else 1 # clamp to 1
        areaSize = game.uf.getSize(path[0]) / (game.height * game.width)
        
        if game.me.health < 20:
            return (path[0], (0.4 * (1 - dist)) + (0.6 * areaSize)) # prioritize closer food if health is getting low
        else:
            return (path[0], (0.3 * (1 - dist)) + (0.7 * areaSize)) # otherwise, care more about area size

    # pairs = POOL.map(eatWorker, game.food, [game] * len(game.food)) # TODO - MultiProcessing
    pairs = [eatWorker(f, game) for f in game.food] # TODO
    pairs = [p for p in pairs if p[0]]

    if not pairs:
        return None

    bestMove = max(pairs, key=lambda x: x[1])[0]
    bestMove = game.directionFromHead(bestMove)

    return bestMove

def defend(game: structures.Game) -> str:
    """Go to the safest location."""
    moves = game.getMoves(game.me.head, structures.Mood.RISKY)
    if not moves:
        return None

    def _key(p: structures.Point, g: structures.Game) -> int:
        risk = structures.getRisk(g.getState(p))
        normalizedAreaSize = g.uf.getSize(p) / (g.height * g.width)
        futureScore = g.simulateMove(p, 3)
        return max(risk,futureScore) - normalizedAreaSize
    
    # scores = POOL.map(_key, moves, [game] * len(moves)) # TODO - MultiProcessing
    scores = [_key(m, game) for m in moves] # TODO
    bestMove = moves[scores.index(min(scores))]
    bestMove = game.directionFromHead(bestMove)

    return bestMove
