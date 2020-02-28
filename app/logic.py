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
    """Move towards food."""
    firstMoveMood = structures.Mood.SAFE if game.me.health > 10 else structures.Mood.RISKY # take riskier paths to the food if we're starving
    pathMood = structures.Mood.RISKY

    while game.food:
        _, point = heapq.heappop(game.food)
        path = game.aStar(point, firstMoveMood, pathMood) 
        if path and len(path) <= game.me.health: # if len(path) is greater, we'll die before we get there 
            return game.directionFromHead(path[0])

    # although game.food only contains food that is technically reachable, it's possible there's no path that obeys the given mood.
    return None

def defend(game: structures.Game) -> str:
    """Go to the safest location."""
    moves = game.getMoves(game.me.head, structures.Mood.RISKY)
    if not moves:
        return None

    # we want a low risk move in big area
    def _key(p: structures.Point) -> int:
        nonlocal game
        normalizedRisk = structures.getRisk(game.getState(p)) / 6
        normalizedAreaSize = game.uf.getSize(p) / (game.height * game.width)
        return (normalizedRisk * 0.7) - (normalizedAreaSize * 0.1) - (game.simulateMove(p) * 0.2)

    bestMove = min(moves, key=_key) 

    return game.directionFromHead(bestMove)
