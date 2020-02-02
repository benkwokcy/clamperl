"""Implements the logic for the /move endpoint."""

import heapq
from typing import List

from app import structures

def getMove(data: dict) -> structures.Direction:
    """Parent function for deciding the next move."""
    game = structures.Game(data)

    # Eat when food dips below threshold.
    if game.me.health < 50:
        move = eat(game)
        if move:
            return move

    # Take the safest move.
    move = defend(game)
    if move:
        return move

    # No moves where we survive.
    return structures.randomDirection()

def eat(game: structures.Game) -> str:
    """Move towards food.

    Takes riskier paths to the food if it is urgent.
    """
    mood = structures.Mood.AGGRESSIVE if game.me.health > 25 else structures.Mood.RISKY

    while game.food:
        _, _, point = heapq.heappop(game.food)
        path = game.aStar(point, mood)
        if path:
            return game.directionFromHead(path[0])

    return None

def defend(game: structures.Game) -> str:
    """Go to the safest location."""
    moves = game.getMoves(game.me.head, structures.Mood.SUICIDAL)

    if not moves:
        return None

    key = lambda m: (structures.getRisk(game.getState(m)), -game.uf.getSize(m)) # lowest risk, biggest area
    bestMove = min(moves, key=key) 

    return game.directionFromHead(bestMove)
