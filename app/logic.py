"""Implements the logic for the /move endpoint in server.py"""

import heapq
from enum import Enum, auto
from typing import List

from app import structures


class Mode(Enum):
    """These values are used in test.py to see if the snake is doing what I expect."""
    grow = auto()
    defend = auto()
    random = auto()

def getMove(data: dict, snakeID: str = None) -> (structures.Direction, Mode):
    """Parent function for deciding the next move."""
    if not snakeID:
        snakeID = data["you"]["id"]
    game = structures.Game(data, snakeID)

    # Eat when food dips below threshold or our size is smaller than the average enemy
    move = eat(game)
    if move:
        return (move, Mode.grow)

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
    canKill = any([game.getState(m) == structures.State.ENEMY_HEAD_AREA_WEAK_AND_STUCK for m in game.getMoves(game.me.head, structures.Mood.SAFE)])

    def skipFood(point: structures.Point, distance: int, game: structures.Game):
        if game.me.health > 50 and max(game.enemies, key=lambda x: x.size).size < game.me.size and (distance > 3 or canKill):
            return True
        for s in game.enemies:
            if point.distance(s.head) * 2 <= point.distance(game.me.head) and game.me.health > 10:
                return True # if we are not starving and the food is 2x closer to another enemy, ignore this food.
            if point.distance(s.head) == 2 and point.distance(game.me.head) == 2 and s.size >= game.me.size:
                return True # if a equal/bigger enemy is also 2 moves from food, ignore this food.

        return False

    food = game.foodPerimeter(firstMoveMood, remainingMoveMood, maxPathLength=game.height)

    moves = []
    for foodPoint, pathLength, firstMove in food:
        if not skipFood(foodPoint, pathLength, game):
            heapq.heappush(moves, (pathLength, firstMove))
    
    if not moves:
        return None

    while moves:
        _, move = heapq.heappop(moves)
        futureRisk, isTailConnected, isEnemyTailConnected, areaSize = game.simulateMove(move, 1)
        moveString = game.directionFromHead(move)
        if game.me.size > 13 and game.me.health > 25 and not isTailConnected:
            continue
        if game.me.health > 20 and not (futureRisk <= structures.Mood.SAFE.value or isTailConnected or (areaSize >= game.me.size and isEnemyTailConnected)):
            continue
        return moveString

    return None

def defend(game: structures.Game) -> str:
    """Go to the safest location."""
    moves = game.getMoves(game.me.head, structures.Mood.RISKY)
    if not moves:
        return None

    def tailChaseBuster(p, g):
        """Identify larger snakes who can intercept me chasing my tail from 2-3 moves away"""

        def isThreeMovesAway(source, destination, game):
            destinationNeighbours = [d for d in destination.neighbours() if d.distance(source) == 2]
            moves = game.getMoves(source, structures.Mood.RISKY)
            moves = [m for m in moves if destination.distance(m) == 2]
            for m in moves:
                for p in game.getMoves(m, structures.Mood.RISKY):
                    if p in destinationNeighbours:
                        return True
            
            return False

        if g.getState(p) == structures.State.SELF_TAIL and g.me.size > 5:
            twoMovesAway = g.me.middle[-1]
            threeMovesAway = g.me.middle[-2]
            for e in g.enemies:
                if e.size > g.me.size and e.head.distance(g.me.head) <= 6:
                    if e.head.distance(twoMovesAway) == 2 and set(g.getMoves(e.head, structures.Mood.RISKY)).intersection(twoMovesAway.neighbours()):
                        return True
                    if e.head.distance(threeMovesAway) == 3 and isThreeMovesAway(e.head, threeMovesAway, game):
                        return True

    def _key(p: structures.Point, g: structures.Game):
        if tailChaseBuster(p,g):
            currentRisk = 4.5
        else:
            currentRisk = structures.getRisk(g.getState(p))
        futureRisk, isTailConnected, isEnemyTailConnected, areaSize = g.simulateMove(p, 3)
        finalRisk = max(currentRisk, futureRisk)
        
        return (-finalRisk, isTailConnected, areaSize, isEnemyTailConnected, g.getState(p) == structures.State.ENEMY_HEAD_AREA_WEAK_AND_STUCK)
    
    bestMoves = [(_key(m, game), game.directionFromHead(m)) for m in moves]
    bestMove = max(bestMoves)[1]

    return bestMove
