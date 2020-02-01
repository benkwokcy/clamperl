import copy
import heapq
from typing import List

from app import structures

def getMove(data):
    game = structures.Game(data)

    # HUNGRY - try to eat
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

# takes riskier routes if eating is more urgent
def eat(game):
    mood = structures.Mood.AGGRESSIVE if game.me.health > 25 else structures.Mood.RISKY

    while game.food:
        _, point = heapq.heappop(game.food)
        move, length = game.aStar(point, mood)
        if length != -1:
            return move

    return None


