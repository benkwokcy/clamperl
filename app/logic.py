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
            print(f"Eat - {move}")
            return move

    # Take the safest move.
    move = defend(game)
    if move:
        print(f"Defend - {move}")
        return move

    # No moves where we survive.
    move = structures.randomDirection()
    print(f"Random - {move}")
    return 

def eat(game: structures.Game) -> str:
    """Move towards food.

    Takes riskier paths to the food if it is urgent.
    """
    mood = structures.Mood.SAFE if game.me.health > 25 else structures.Mood.RISKY

    while game.food:
        _, point = heapq.heappop(game.food)
        path = game.aStar(point, mood)
        if path:
            return game.directionFromHead(path[0])

    return None

def defend(game: structures.Game) -> str:
    """Go to the safest location."""
    moves = game.getMoves(game.me.head, structures.Mood.RISKY)

    if not moves:
        return None

    # we want a low risk move in big area
    def key(p: structures.Point) -> int:
        nonlocal game
        risk = structures.getRisk(game.getState(p))
        normalizedAreaSize = game.uf.getSize(p) / (game.height * game.width)
        return risk - normalizedAreaSize

    bestMove = min(moves, key=key) 

    return game.directionFromHead(bestMove)
