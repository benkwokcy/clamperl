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

def getMove(data: dict) -> (structures.Direction, Mode):
    """Parent function for deciding the next move."""
    game = structures.Game(data)

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

    firstMoveMood = structures.Mood.SAFE if game.me.health > 12 else structures.Mood.RISKY # take riskier paths to the food if we're starving
    validHeadMoves = game.getMoves(game.me.head, structures.Mood.RISKY)

    paths = []
    maxDistance = 0
    for point in game.food:
        if any([game.uf.connected(x, point) for x in validHeadMoves]): # food is reachable
            path = game.aStar(point, firstMoveMood, structures.Mood.RISKY) 
            if path and len(path) <= game.me.health: # if len(path) is greater, we'll die before we get there
                paths.append(path)
                maxDistance = max(maxDistance, len(path))

    if not paths:
        return None

    def score(path):
        """We want the closest food that is also in a big open area."""
        dist = len(path) / maxDistance
        areaSize = game.uf.getSize(path[0]) / (game.height * game.width)

        print("food", dist, areaSize) # TODO

        return (0.3 * (1 - dist)) + (0.7 * areaSize)

    bestMove = max(paths, key=score)[0]

    return game.directionFromHead(bestMove)

def defend(game: structures.Game) -> str:
    """Go to the safest location."""
    moves = game.getMoves(game.me.head, structures.Mood.RISKY)
    if not moves:
        return None

    def _key(p: structures.Point) -> int:
        nonlocal game
        risk = structures.getRisk(game.getState(p))
        area = game.simulateMove(p)
        print("defend", risk, area) # TODO
        return (0.7 * (1 - risk)) + (0.3 * area)

    bestMove = max(moves, key=_key)

    return game.directionFromHead(bestMove)
