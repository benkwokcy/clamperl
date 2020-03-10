"""Implements the logic for the /move endpoint in server.py"""

import heapq
from enum import Enum, auto
from typing import List

from app import structures


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
        move = eat(game)
        if move:
            return (move, Mode.hungry if game.me.health < 50 else Mode.grow)

    # Take the safest move.
    move = defend(game)
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
        """Given a food location, decide if we should try to eat it and return the path if we should."""
        # take riskier paths to the food if we're starving
        firstMoveMood = structures.Mood.SAFE if game.me.health > 10 else structures.Mood.RISKY 
        remainingMoveMood = structures.Mood.SAFE if game.me.health > 25 else structures.Mood.RISKY
        validHeadMoves = game.getMoves(game.me.head, firstMoveMood)

        if point.distance(game.me.head) > game.height:
            return None # if it's too far, ignore this food.
        if not any([game.ufRisky.connected(x, point) for x in validHeadMoves]): 
            return None # if food is not reachable even by risky moves, ignore this food.
        if game.ufSafe.getSize(point) < game.me.size and game.me.health > 25: 
            return None # if we are not very hungry and the areas is smaller than us, ignore this food.
        if any([point.distance(s.head) * 2 <= point.distance(game.me.head) for s in game.enemies]) and game.me.health > 10:
            return None # if we are not starving and the food is 3x closer to another enemy, ignore this food.
        if any([point.distance(s.head) == 2 and point.distance(game.me.head) == 2 and s.size >= game.me.size for s in game.enemies]):
            return None # if a equal/bigger enemy is also 2 moves from food, ignore this food.
        if game.me.size > 13 and game.me.health > 25 and not game.ufSafe.connected(point, game.me.tail):
            return None # if i'm getting very long and not that hungry, prefer to stay by my tail

        path = game.aStar(point, firstMoveMood, remainingMoveMood)
        
        if not path:
            return None # if we cannot reach the food using our current mood, ignore this food.
        if len(path) > game.me.health:
            return None # if we'll die before we reach the food, ignore this food.
        if len(path) > game.height:
            return None # if it's too far, ignore this food.

        return path

    moves = []
    for f in game.food:
        path = eatWorker(f, game)
        if path:
            heapq.heappush(moves, (len(path), path[0]))
    
    if not moves:
        return None

    while moves:
        _, move = heapq.heappop(moves)
        futureRisk, isTailConnected, isEnemyTailConnected, _ = game.simulateMove(move, 1)
        if game.me.health > 20 and not (futureRisk < structures.Mood.SAFE.value or isTailConnected or isEnemyTailConnected):
            continue
        return game.directionFromHead(move)

    return None

def defend(game: structures.Game) -> str:
    """Go to the safest location."""
    moves = game.getMoves(game.me.head, structures.Mood.RISKY)
    if not moves:
        return None

    def _key(p: structures.Point, g: structures.Game):
        currentRisk = structures.getRisk(g.getState(p))
        futureRisk, isTailConnected, isEnemyTailConnected, areaSize = g.simulateMove(p, 3)
        finalRisk = max(currentRisk, futureRisk)
        
        # HACK - Reverse boolean values because we want the min key value
        return (finalRisk, not isTailConnected, not isEnemyTailConnected, -areaSize)
    
    bestMoves = [(_key(m, game), m) for m in moves]
    bestMove = min(bestMoves)[1]
    bestMove = game.directionFromHead(bestMove)

    return bestMove
