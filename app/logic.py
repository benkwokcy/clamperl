"""Implements the logic for the /move endpoint."""

import heapq
from typing import List

from app import structures

def getMove(data):
    """Parent function for deciding the next move."""
    game = structures.Game(data)

    # HUNGRY - try to eat if health dips below a threshold
    if game.me.health < 50:
        move = eat(game)
        if move:
            return move

    # DEFENSIVE - go to the safest location
    moves = game.getMoves(game.me.head, structures.Mood.ALL)
    if moves:
        return game.directionFromHead(moves[0])

    # RANDOM - should not reach here
    print("No valid moves in board. Should only happen in a 1x1 board.")
    return structures.randomDirection()

def eat(game):
    """Move towards food.

    Takes riskier paths to the food if it is urgent.
    """
    mood = structures.Mood.AGGRESSIVE if game.me.health > 25 else structures.Mood.RISKY

    while game.food:
        _, point = heapq.heappop(game.food)
        move, length = game.aStar(point, mood)
        if length != -1:
            return move

    return None


