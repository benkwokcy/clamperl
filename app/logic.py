"""Implements the logic for the /move endpoint."""

import heapq
from typing import List

from structures import Mood, Game, Direction, Point, randomDirection

def getMove(data) -> Direction:
    """Parent function for deciding the next move."""
    game = Game(data)

    # HUNGRY - try to eat if health dips below a threshold
    if game.me.health < 50:
        move = eat(game)
        if move:
            return game.directionFromHead(move)

    # DEFENSIVE - go to the safest location
    moves = game.getMoves(game.me.head, Mood.ALL)
    if moves:
        return game.directionFromHead(moves[0])

    # RANDOM - should not reach here
    print("No valid moves in board. Should only happen in a 1x1 board.")
    return randomDirection()

def eat(game) -> Point:
    """Move towards food.

    Takes riskier paths to the food if it is urgent.
    """
    mood = Mood.AGGRESSIVE if game.me.health > 25 else Mood.RISKY

    while game.food:
        _, point = heapq.heappop(game.food)
        path = game.aStar(point, mood)
        if path:
            return path[0]

    return None


