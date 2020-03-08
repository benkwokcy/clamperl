"""Implements the logic for the /move endpoint in server.py"""

import heapq
# import time
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

def getMove(data: dict, snakeID: str = None) -> (structures.Direction, Mode):
    """Parent function for deciding the next move."""
    if not snakeID:
        snakeID = data["you"]["id"]
    game = structures.Game(data, snakeID)

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

        if point.distance(game.me.head) > game.height:
            return (None, -1.0) # if it's too far, ignore this food.
        if not any([game.ufRisky.connected(x, point) for x in validHeadMoves]): 
            return (None, -1.0) # if food is not reachable in our current mood, ignore this food.
        if game.ufSafe.getSize(point) < game.me.size and game.me.health > 25: 
            return (None, -1.0) # if we are not very hungry and the areas is smaller than us, ignore this food.
        if any([point.distance(s.head) * 2 <= point.distance(game.me.head) for s in game.enemies]) and game.me.health > 10:
            return (None, -1.0) # if we are not starving and the food is 3x closer to another enemy, ignore this food.
        if any([point.distance(s.head) == 2 and point.distance(game.me.head) == 2 and s.size >= game.me.size for s in game.enemies]):
            return (None, -1.0) # if a equal/bigger enemy is also 2 moves from food, ignore this food.
        if game.me.size > 20 and game.me.health > 25 and not game.ufSafe.connected(point, game.me.tail):
            return (None, -1.0) # if i'm getting very long and not that hungry, prefer to stay by my tail

        path = game.aStar(point, firstMoveMood, remainingMoveMood)
        
        if not path:
            return (None, -1.0) # if we cannot reach the food using our current mood, ignore this food.
        if len(path) > game.me.health:
            return (None, -1.0) # if we'll die before we reach the food, ignore this food.
        if len(path) > game.height:
            return (None, -1.0) # if it's too far, ignore this food.

        dist = len(path) / game.height if len(path) / game.height <= 1 else 1 # clamp to 1
        areaSize = game.ufRisky.getSize(path[0]) / (game.height * game.width)
        
        if game.me.health < 20:
            return (path[0], (0.4 * (1 - dist)) + (0.6 * areaSize)) # prioritize closer food if health is getting low
        else:
            return (path[0], (0.3 * (1 - dist)) + (0.7 * areaSize)) # otherwise, care more about area size

    # pairs = POOL.map(eatWorker, game.food, [game] * len(game.food)) # TODO - MultiProcessing
    pairs = [eatWorker(f, game) for f in game.food] # TODO
    pairs = [p for p in pairs if p[0]]

    if not pairs:
        return None

    pairs.sort(key=lambda x:x[1], reverse=True)
    for move,_ in pairs:
        if game.me.health > 25 and game.simulateMove(move, numFutures=2) != 0.0:
            continue
        return game.directionFromHead(move)

    return None

def defend(game: structures.Game) -> str:
    """Go to the safest location."""
    moves = game.getMoves(game.me.head, structures.Mood.RISKY)
    if not moves:
        return None

    def _key(p: structures.Point, g: structures.Game) -> int:
        currentRisk = structures.getRisk(g.getState(p))
        futureRisk = g.simulateMove(p, 3)
        finalRisk = max(currentRisk, futureRisk)
        currentAreaSize = (g.height * g.width) / g.ufSafe.getSize(p)
        distToEnemies = 1 / min([e.head.distance(p) for e in g.enemies if any([g.ufRisky.connected(p, q) for q in g.getMoves(e.head, structures.Mood.RISKY)])] or [g.height + g.height])
        distToTail = p.distance(g.me.middle[-1]) if g.ufSafe.connected(p, g.me.tail) else g.height + g.height
        return (finalRisk, currentAreaSize, distToEnemies, distToTail)
    
    # scores = POOL.map(_key, moves, [game] * len(moves)) # TODO - MultiProcessing
    scores = [_key(m, game) for m in moves] # TODO
    bestMove = moves[scores.index(min(scores))]
    bestMove = game.directionFromHead(bestMove)

    return bestMove
