"""Implements the logic for the /move endpoint."""

import heapq
from typing import List

from app import structures

def getMove(data: dict) -> structures.Direction:
    """Parent function for deciding the next move."""
    game = structures.Game(data)

    # Eat when food dips below threshold or our size is smaller than the average enemy
    hungry = game.me.health < 50
    smallerThanAverage = game.enemies and (game.me.size <= (sum([e.size for e in game.enemies] / len(game.enemies))))
    if hungry or smallerThanAverage:
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
    """Move towards food."""

    mood = structures.Mood.SAFE
    if game.me.health <= 25: # take riskier paths to the food if we're starving
        mood = structures.Mood.RISKY

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
