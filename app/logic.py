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
    smallerThanAverage = game.enemies and (game.me.size < max(game.enemies, key=lambda e: e.size).size) # TODO
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
    if not game.food:
        return None
    
    firstMoveMood = structures.Mood.SAFE 
    remainingMoveMood = structures.Mood.SAFE

    def skipFood(point: structures.Point, distance: int, game: structures.Game):
        if game.ufSafe.getSize(point) < game.me.size and game.me.health > 25: # TODO - I don't actually UF these!!
            return True # if we are not very hungry and the areas is smaller than us, ignore this food.
        if any([point.distance(s.head) * 2 <= point.distance(game.me.head) for s in game.enemies]) and game.me.health > 10:
            return True # if we are not starving and the food is 3x closer to another enemy, ignore this food.
        if any([point.distance(s.head) == 2 and point.distance(game.me.head) == 2 and s.size >= game.me.size for s in game.enemies]):
            return True # if a equal/bigger enemy is also 2 moves from food, ignore this food.
        if game.me.size > 13 and game.me.health > 25 and not game.ufSafe.connected(point, game.me.tail): # TODO
            return True # if i'm getting very long and not that hungry, prefer to stay by my tail
        
        return False

    food = game.foodPerimeter(firstMoveMood, remainingMoveMood, min(game.height, game.me.health))

    moves = []
    for foodPoint, pathLength, firstMove in food:
        if not skipFood(foodPoint, pathLength, game):
            heapq.heappush(moves, (pathLength, firstMove))
    
    if not moves:
        return None

    while moves:
        _, move = heapq.heappop(moves)
        futureRisk, isTailConnected, isEnemyTailConnected, _ = game.simulateMove(move, 1)
        if game.me.health > 20 and not (futureRisk <= structures.Mood.SAFE.value or isTailConnected or isEnemyTailConnected):
            continue
        return game.directionFromHead(move)

    return None

def defend(game: structures.Game) -> str:
    """Go to the safest location."""
    moves = game.getMoves(game.me.head, structures.Mood.RISKY)
    if not moves:
        return None

    def tailChaseBuster(p, g):
        if g.getState(p) == structures.State.SELF_TAIL and g.me.size > 5:
            twoMovesAway = g.me.middle[-1]
            # threeMovesAway = g.me.middle[-2]
            for e in g.enemies:
                if e.size > g.me.size and e.head.distance(g.me.head) <= 6:
                    if e.head.distance(twoMovesAway) == 2 and set(g.getMoves(e.head, structures.Mood.RISKY)).intersection(twoMovesAway.neighbours()):
                        return True
                    # if e.head.distance(threeMovesAway) == 3 and any([g.ufRisky.connected(threeMovesAway, m) for m in g.getMoves(e.head, structures.Mood.RISKY)]):
                    #     return True

    def _key(p: structures.Point, g: structures.Game):
        if tailChaseBuster(p,g):
            currentRisk = 4.5
        else:
            currentRisk = structures.getRisk(g.getState(p))
        futureRisk, isTailConnected, isEnemyTailConnected, areaSize = g.simulateMove(p, 3)
        finalRisk = max(currentRisk, futureRisk)
        
        # HACK - Reverse boolean values because we want the min key value
        return (finalRisk, not isTailConnected, not isEnemyTailConnected, -areaSize)
    
    bestMoves = [(_key(m, game), game.directionFromHead(m)) for m in moves]
    bestMove = min(bestMoves)[1]

    return bestMove
