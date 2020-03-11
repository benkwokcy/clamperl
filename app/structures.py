"""Data structures used by logic.py"""

import heapq
import random
from collections import defaultdict, deque
from enum import Enum, auto
from typing import Dict, List, Set


class Point:
    """A 2D point representing a position on the game board."""
    def __init__(self, data):
        self.x = data["x"]
        self.y = data["y"]
        self.tup = (self.x, self.y)

    def left(self):
        return Point({"x": self.x-1, "y": self.y})

    def right(self):
        return Point({"x": self.x+1, "y": self.y})

    def up(self):
        return Point({"x": self.x, "y": self.y-1})

    def down(self):
        return Point({"x": self.x, "y": self.y+1})
    
    def neighbours(self):
        return {
            Point({"x": self.x-1, "y": self.y}), 
            Point({"x": self.x+1, "y": self.y}), 
            Point({"x": self.x, "y": self.y-1}), 
            Point({"x": self.x, "y": self.y+1})
        }

    def distance(self, other) -> int:
        """Manhattan distance between this point and another point."""
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    def __str__(self) -> str:
        """Overrides the print representation."""
        return str(self.tup)
    
    def __eq__(self, other) -> bool:
        """Override equality."""
        if type(other) is type(self):
            return self.tup == other.tup
        else:
            return False
    
    def __lt__(self, other) -> bool:
        """Needed to break ties in heapq"""
        return sum(self.tup) < sum(other.tup)
    
    def __hash__(self) -> int:
        """Since we override equality, we need to ensure equivalent objects have identical hashes."""
        return hash(self.tup)

class Snake:
    def __init__(self, data: dict):
        body = data["body"]
        self.id = data["id"]
        self.name = data["name"]
        self.body = [Point(c) for c in body]
        self.head = Point(body[0])
        self.tail = Point(body[-1])
        self.middle = [ Point(c) for c in body[1:-1] ]
        self.size = len(body)
        self.health = data["health"]
        self.ate = (self.size >= 2) and (body[-1] == body[-2]) # just ate food so there is a body part on top of the tail
        self.data = data
    
    def copy(self):
        return Snake(self.data)

class Direction(Enum):
    """The /move endpoint expects a string of this form."""
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

    @staticmethod # suppresses no 'self' reference warning
    def randomDirection():
        """Use this if we're going to die no matter what."""
        return random.choice([d.value for d in Direction])

class State(Enum):
    """Each 1x1 square on the game board is given a state."""
    EMPTY_SIDE = auto()
    EMPTY_MIDDLE = auto()
    FOOD = auto()
    SELF_HEAD = auto()
    SELF_BODY = auto()
    SELF_TAIL = auto()
    ENEMY_HEAD = auto()
    ENEMY_HEAD_AREA_WEAK_AND_STUCK = auto() # a point where a weaker enemy is forced to go to
    ENEMY_HEAD_AREA_WEAK = auto() # a point reachable by an enemy head who's length is less than ours
    ENEMY_HEAD_AREA_EQUAL = auto() # a point reachable by an enemy head who's length is equal to ours
    ENEMY_HEAD_AREA_STRONG = auto() # a point reachable by an enemy head who's length is greater than ours
    ENEMY_HEAD_AREA_MULTIPLE_STRONG_OR_EQUAL = auto() # a point reachable by multiple enemy heads who could kill us
    ENEMY_BODY = auto()
    ENEMY_TAIL = auto()

    @staticmethod
    def getHeadState(me: Snake, enemy: Snake):
        if me.size > enemy.size:
            return State.ENEMY_HEAD_AREA_WEAK
        elif me.size == enemy.size:
            return State.ENEMY_HEAD_AREA_EQUAL
        else:
            return State.ENEMY_HEAD_AREA_STRONG
    
    @staticmethod
    def getSideOrMiddle(point: Point, length: int):
        if point.x in (0, length-1) or point.y in (0, length-1):
            return State.EMPTY_SIDE
        else:
            return State.EMPTY_MIDDLE

def getRisk(state: State) -> int:
    """Assign a riskiness value to each state.
    The higher the value, the more dangerous the state is.
    This allows me to compare moves and choose the safer options.
    """
    risk = {
        # SAFE
        State.FOOD: 0,
        State.ENEMY_HEAD_AREA_WEAK_AND_STUCK: 1,
        State.SELF_TAIL: 2,
        State.EMPTY_MIDDLE: 2,
        State.ENEMY_HEAD_AREA_WEAK: 2, # head on collision will kill the other snake.
        State.ENEMY_TAIL: 3,
        State.EMPTY_SIDE: 4,

        # POSSIBLE DEATH
        State.ENEMY_HEAD_AREA_EQUAL: 5, # head on collision will kill both of us.
        State.ENEMY_HEAD_AREA_STRONG: 6, # head on collision will kill our snake.
        State.ENEMY_HEAD_AREA_MULTIPLE_STRONG_OR_EQUAL: 7,

        # DEFINITE DEATH
        State.SELF_HEAD: 8,
        State.SELF_BODY: 8,
        State.ENEMY_HEAD: 8,
        State.ENEMY_BODY: 8
    }

    return risk[state]

class Mood(Enum):
    """Assigns names to commonly used risk values.
    This is used to set the maximum riskiness allowed by the getMoves() function.
    When we do this, we can easily configure the behavior of the snake.
    Anywhere you see mood as a parameter, you can modify it to make the snake act
    safer or riskier.
    """
    SAFE = 4 # only moves with no chance of death
    RISKY = 7 # include moves with some chance of death
    ALL = 8 # include moves where we definitely die

class Game:
    """Contains the game board and all objects on the board.
    This is the main data structure for making decisions about the game.
    """
    def __init__(self, data: dict, snakeID: str):
        self.id = data.get("game", { "id": "0" })["id"]
        self.turn = data.get("turn", "0")
        self.height = data["board"]["height"]
        self.width = data["board"]["width"]
        self.board = [[None] * self.width for _ in range(self.height)]
        self.me = None
        self.enemies = []
        self.food = []
        self.ufRisky = UnionFind(self.board) # connected areas

        # board
        for row in range(self.height):
            for col in range(self.width):
                self.board[row][col] = State.getSideOrMiddle(Point({"x":col, "y":row}), self.height)

        # food
        for coordinates in data["board"]["food"]:
            self.food.append(Point(coordinates))
            self.setState(Point(coordinates), State.FOOD)

        # snakes
        for s in data["board"]["snakes"]:
            s = Snake(s)
            if snakeID == s.id:
                self.me = s
            else:
                self.enemies.append(s)

        # myself
        self.setState(self.me.head, State.SELF_HEAD)
        self.setStates(self.me.middle, State.SELF_BODY)
        self.setState(self.me.tail, State.SELF_BODY if self.me.ate else State.SELF_TAIL, overrideRisk=True) # if just ate, the tail has a body part on top of it

        # enemies
        for enemy in self.enemies:
            enemyMoves = self.getMoves(enemy.head, Mood.RISKY)
            if len(enemyMoves) == 1 and enemy.size < self.me.size:
                self.setState(enemyMoves[0], State.ENEMY_HEAD_AREA_WEAK_AND_STUCK)
            else:
                for move in enemyMoves:
                    self.setState(move, State.getHeadState(self.me, enemy))
            self.setState(enemy.head, State.ENEMY_HEAD)
            self.setStates(enemy.middle, State.ENEMY_BODY)
            self.setState(enemy.tail, State.ENEMY_BODY if enemy.ate else State.ENEMY_TAIL, overrideRisk=True) # if just ate, the tail has a body part on top of it

        # calculate reachable areas from my head
        # It *DOES NOT* include any heads or bodies. Do not try to see if these are connected.
        # Squares on either side of my head are not connected through my head.
        validMoves = self.getMoves(self.me.head, Mood.RISKY)
        for move in validMoves:
            if self.ufRisky.getSize(move) == 1:
                points = self.floodFill(move, Mood.RISKY, maxAreaLength=self.me.size*2)
                for p in points:
                    self.ufRisky.union(p, move)

    def setState(self, point: Point, newState: State, overrideRisk = False):
        """Set a state at a point, if the risk is higher or the point is empty."""
        if overrideRisk:
            self.board[point.y][point.x] = newState
            return

        oldState = self.getState(point)
        riskyHeadStates = (State.ENEMY_HEAD_AREA_EQUAL, State.ENEMY_HEAD_AREA_STRONG)
        weakHeadStates = (State.ENEMY_HEAD_AREA_WEAK_AND_STUCK, State.ENEMY_HEAD_AREA_WEAK)

        if newState in riskyHeadStates and oldState in riskyHeadStates:
            self.board[point.y][point.x] = State.ENEMY_HEAD_AREA_MULTIPLE_STRONG_OR_EQUAL
        elif (newState, oldState) == weakHeadStates or (oldState, newState) == weakHeadStates:
            self.board[point.y][point.x] = State.ENEMY_HEAD_AREA_WEAK_AND_STUCK
        elif oldState in (State.EMPTY_SIDE, State.EMPTY_MIDDLE) or getRisk(newState) > getRisk(oldState):
            self.board[point.y][point.x] = newState

    def setStates(self, points: List[State], state: State):
        """Same as setState but takes a list of points."""
        for point in points:
            self.setState(point, state)

    def getState(self, point: Point) -> State:
        """Get state from a point on the board."""
        return self.board[point.y][point.x]
    
    def getMoves(self, point: Point, mood: Mood) -> List[Point]:
        """Get all valid moves from a point that have risk <= mood."""

        def isValid(point: Point) -> bool:
            """Check if a point is within the game board boundaries."""
            return 0 <= point.x < self.width and 0 <= point.y < self.height

        # All moves that are inside the board and have risk <= mood
        moves = [m for m in point.neighbours() if isValid(m) and getRisk(self.getState(m)) <= mood.value]

        # If we don't shuffle, snake moves in predictable patterns when heuristics are tied for all moves
        random.shuffle(moves)

        return moves

    def directionFromHead(self, point: Point) -> str:
        """Given a valid move from the head, return its direction as a string."""
        head = self.me.head
        directions = {
            head.up().tup: Direction.UP,
            head.down().tup: Direction.DOWN,
            head.left().tup: Direction.LEFT,
            head.right().tup: Direction.RIGHT,
        }

        assert (point.tup in directions), "Point wasn't a valid move from head."

        return directions[point.tup].value
    
    def simulateMove(self, move: Point, numFutures: int):
        """Simulate one move into the future and see if it's risky.
        Bad means we are not safely connected to our tail and the safe area is smaller
        than us."""

        def moveSelf(p: Point) -> Point:
            # moves my snake one move on board and modifies the snake object
            if self.me.ate and self.getState(p) != State.FOOD:
                self.setState(self.me.tail, State.SELF_TAIL, overrideRisk=True)
            if not self.me.ate:
                self.setState(self.me.tail, State.EMPTY_MIDDLE, overrideRisk=True)
                if self.getState(p) != State.FOOD:
                    self.setState(self.me.middle[-1], State.SELF_TAIL, overrideRisk=True)

            self.me.tail = self.me.middle[-1]
            if self.getState(p) != State.FOOD:
                self.me.middle.pop()

            self.setState(p, State.SELF_HEAD, overrideRisk=True)            
            self.setState(self.me.head, State.SELF_BODY, overrideRisk=True)

            self.me.middle.insert(0, self.me.head)
            self.me.head = p
            self.me.body = [self.me.head] + self.me.middle + [self.me.tail]

        def moveEnemy(p: Point, snake: Snake) -> Point:
            # moves enemy snake one move on board
            tail = snake.tail

            if snake.ate and self.getState(p) != State.FOOD:
                self.setState(snake.tail, State.ENEMY_TAIL, overrideRisk=True)
            if not snake.ate:
                self.setState(snake.tail, State.EMPTY_MIDDLE, overrideRisk=True)
                if self.getState(p) != State.FOOD:
                    self.setState(snake.middle[-1], State.ENEMY_TAIL, overrideRisk=True)
                    tail = snake.middle[-1]
            self.setState(p, State.ENEMY_HEAD, overrideRisk=True)
            self.setState(snake.head, State.ENEMY_BODY, overrideRisk=True)
            for m in self.getMoves(p, Mood.RISKY):
                self.setState(m, State.getHeadState(self.me, snake))

            return tail

        def removeSnake(snake: Snake):
            for p in [snake.head, snake.tail] + snake.middle:
                self.setState(p, State.getSideOrMiddle(p, self.height), overrideRisk=True)
        
        # we need to restore the original board before we return
        originalBoard = [row[:] for row in self.board]
        originalMe = self.me.copy()

        # reset head areas and move my snake
        for row in range(self.height): 
            for col in range(self.width):
                if self.board[row][col] in (State.ENEMY_HEAD_AREA_WEAK, State.ENEMY_HEAD_AREA_EQUAL, State.ENEMY_HEAD_AREA_STRONG, State.ENEMY_HEAD_AREA_MULTIPLE_STRONG_OR_EQUAL):
                    self.board[row][col] = State.EMPTY_MIDDLE # doesn't matter if it is state.empty_side because we only care about safe vs risky
        moveSelf(move)

        # print(f"Future: {self.directionFromHead(move)} INITIAL SETUP") # TODO
        # print(self)

        # metrics for the safety of this future
        isTailReachable = True
        isEnemyTailReachable = True
        riskyAreaSize = self.ufRisky.getSize(move)

        # pre-calculation for enemy moves
        movesRemaining = {}
        movesPerEnemy = {}
        aliveEnemies = set()
        totalMovesUnexplored = 0
        for e in self.enemies:
            moves = { p for p in self.getMoves(e.head, Mood.RISKY) if self.getState(p) != State.SELF_TAIL }
            if not moves: # enemies who will die for sure get removed from the board
                removeSnake(e)
            else:
                aliveEnemies.add(e)
                movesRemaining[e] = moves
                movesPerEnemy[e] = set(moves) # shallow copy
                totalMovesUnexplored += len(moves)

        # save board state so we can return to it after each iteration
        newBoard = [row[:] for row in self.board] 

        for iteration in range(numFutures):

            # keep track of whose head is where
            heads = {}
            
            # we've looked at all enemy moves (but not all permutations) and none are super bad, so return
            if totalMovesUnexplored == 0 and iteration != 0:
                self.board = originalBoard
                self.me = originalMe
                return (0.0, isTailReachable, isEnemyTailReachable, riskyAreaSize)

            # move all enemies who aren't stuck
            enemyTails = set()
            for enemy in aliveEnemies:
                # select the move
                if movesRemaining[enemy]:
                    if enemy.head.distance(self.me.head) <= 4:
                        if enemy.size >= self.me.size:
                            enemyMove = min(movesRemaining[enemy], key=lambda p: p.distance(move))
                        else:
                            enemyMove = max(movesRemaining[enemy], key=lambda p: p.distance(move))
                        movesRemaining[enemy].remove(enemyMove)
                        totalMovesUnexplored -= 1
                    else:
                        enemyMove = movesRemaining[enemy].pop()
                        totalMovesUnexplored -= 1
                elif movesPerEnemy[enemy]:
                    enemyMove = random.choice(tuple(movesPerEnemy[enemy]))
                else: # no possible moves
                    removeSnake(enemy)
                    continue

                # update the board with the move
                if self.getState(enemyMove) == State.ENEMY_HEAD:
                    other = heads[enemyMove]
                    if other.size >= enemy.size:
                        removeSnake(enemy)
                    else:
                        removeSnake(other)
                else:
                    enemyTail = moveEnemy(enemyMove, enemy)
                    heads[enemyMove] = enemy
                    enemyTails.add(enemyTail)

            # calculate metrics
            safeArea, isTailReachable, isEnemyTailReachable = self.floodSafeArea(move, enemyTails, maxPathLength = self.me.size + 2)

            # print(f"Future: {self.directionFromHead(move)}, safeArea={len(safeArea)}, meSize={self.me.size}, isTailReachable={isTailReachable}, isEnemyTailReachable={isEnemyTailReachable}") # TODO
            # print(self)

            if not isTailReachable and len(safeArea) <= self.me.size:
                self.board = originalBoard
                self.me = originalMe
                if not isEnemyTailReachable:
                    if len(safeArea) <= self.me.size / 2:
                        return (7, isTailReachable, isEnemyTailReachable, riskyAreaSize)
                    else:
                        return (6, isTailReachable, isEnemyTailReachable, riskyAreaSize)
                else:
                    return (4.5, isTailReachable, isEnemyTailReachable, riskyAreaSize)

            # restore board state
            self.board = [row[:] for row in newBoard]

        self.board = originalBoard
        self.me = originalMe
        return (0, isTailReachable, isEnemyTailReachable, riskyAreaSize)
    
    def floodFill(self, p: Point, mood: Mood, maxPathLength=float("inf"), maxAreaLength=float("inf")) -> Set[Point]:
        """We count weak head areas that form choke points as risky."""
        seen = set([p])
        queue = deque([(p,1)])

        while queue:
            if len(seen) > maxAreaLength:
                return seen
            curr,dist = queue.popleft()
            if dist < maxPathLength:
                for neighbour in self.getMoves(curr, mood):
                    if neighbour not in seen:
                        if mood == Mood.SAFE and self.getState(neighbour) == State.ENEMY_HEAD_AREA_WEAK and dist > 1 and any([getRisk(self.getState(s)) > Mood.RISKY.value for s in self.getMoves(neighbour, Mood.ALL)]):
                            continue
                        seen.add(neighbour)
                        queue.append((neighbour, dist+1))

        return seen

    def floodSafeArea(self, p: Point, enemyTails, maxPathLength=float("inf")):
        """We can calculate whether a body part will move out of the way or not"""
        seen = set([p])
        queue = deque([(p,1)])
        hasEnemyTail = False
        hasMyTail = False

        while queue:
            curr,dist = queue.popleft()
            if curr == self.me.tail:
                hasMyTail = True
            elif curr in enemyTails:
                hasEnemyTail = True
            if hasMyTail and hasEnemyTail and len(seen) > self.me.size:
                return (seen, hasMyTail, hasEnemyTail)
            if dist < maxPathLength:
                for neighbour in self.getMoves(curr, Mood.ALL):
                    if neighbour not in seen:
                        neighbourState = self.getState(neighbour)
                        if neighbourState == State.ENEMY_HEAD_AREA_WEAK and dist > 1 and any([getRisk(self.getState(s)) > Mood.RISKY.value for s in self.getMoves(neighbour, Mood.ALL)]):
                            continue # risky choke point
                        if getRisk(neighbourState) > Mood.SAFE.value: # consider whether a part of my body will move out of the way by the time I get there
                            if neighbourState == State.SELF_BODY:
                                index = self.me.body.index(neighbour)
                                movesFromTail = 3
                                if (index >= self.me.size - movesFromTail and 
                                        (not self.me.ate and dist > (self.me.size - 1 - index) or 
                                        self.me.ate and dist > (self.me.size - index))):
                                    seen.add(neighbour)
                                    queue.append((neighbour, dist+1))
                                else:
                                    continue
                            else:
                                continue
                        seen.add(neighbour)
                        queue.append((neighbour, dist+1))

        return (seen, hasMyTail, hasEnemyTail)

    def foodPerimeter(self, firstMoveMood: Mood, pathMood: Mood, maxPathLength: int):
        """Get food reachable from the head within a certain path length and mood constraint."""
        startingMoves = self.getMoves(self.me.head, firstMoveMood)

        if not startingMoves:
            return []
        
        seen = set(startingMoves)
        queue = deque([(s,1,s) for s in startingMoves])
        food = []

        while queue:
            curr, dist, parent = queue.popleft()
            if self.getState(curr) == State.FOOD:
                food.append((curr,dist,parent))
            if dist < maxPathLength:
                for neighbour in self.getMoves(curr, pathMood):
                    if neighbour not in seen:
                        if pathMood == Mood.SAFE and self.getState(neighbour) == State.ENEMY_HEAD_AREA_WEAK and neighbour.distance(self.me.head) > 1 and any([getRisk(self.getState(s)) > Mood.RISKY.value for s in self.getMoves(neighbour, Mood.ALL)]):
                            continue
                        seen.add(neighbour)
                        queue.append((neighbour, dist+1, parent))

        return food

    def __str__(self) -> str:
        """Overrides the print representation."""

        def symbol(state: State) -> str:
            if state == State.FOOD:
                return "F"
            elif state == State.SELF_HEAD:
                return "@"
            elif state == State.SELF_BODY:
                return "+"
            elif state == State.SELF_TAIL:
                return ">"
            elif state == State.ENEMY_HEAD:
                return "#"
            elif state == State.ENEMY_BODY:
                return "X"
            elif state == State.ENEMY_TAIL:
                return "<"
            elif state in (State.ENEMY_HEAD_AREA_EQUAL, State.ENEMY_HEAD_AREA_STRONG, State.ENEMY_HEAD_AREA_MULTIPLE_STRONG_OR_EQUAL):
                return "-"
            elif state == State.ENEMY_HEAD_AREA_WEAK:
                return "_"
            else:
                return " "

        assert self.height < 36, "Indices don't go that high in string representation, please extend indices."
        indices = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

        result = ["\n"]
        result.append("   " + " ".join(indices[:self.height]))
        for i, row in enumerate(self.board):
            result.append(indices[i] + " [" + "|".join([symbol(state) for state in row]) + "]")
        result.append(f"Health: {self.me.health}")
        result.append(f"Size: {self.me.size}")

        return "\n".join(result)

    def printUF(self, uf) -> str:
        """Overrides the print representation."""
        assert self.height < 36, "Indices don't go that high in string representation, please extend indices."
        indices = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

        result = ["\n"]
        result.append("   " + " ".join(indices[:self.height]))
        for i, row in enumerate(self.board):
            result.append(indices[i] + " [" + "|".join([str(uf.getSize(Point({"x": j, "y": i}))) for j,_ in enumerate(row)]) + "]")

        print("\n".join(result))

class UnionFind:
    """Weighted UnionFind with Path Compression.

    Keep track of connected components on the board.
    We can configure what we consider to be connected using Moods, see Game constructor.
    All the functions take in Point objects for convenience.
    The id and size lists are indexed by int indices.
    """
    def __init__(self, board: List[List[State]]):
        self.height = len(board)
        self.width = len(board[0])
        self.id = [i for i in range(self.height * self.width)]
        self.size = [1 for i in range(self.height * self.width)]

    def union(self, p1: Point, p2: Point):
        parent1 = self._find(p1)
        parent2 = self._find(p2)

        if parent1 == parent2:
            return
        
        # link the smaller tree to the root of the bigger tree
        if self.size[parent1] >= self.size[parent2]:
            self.id[parent2] = parent1
            self.size[parent1] += self.size[parent2]
        else:
            self.id[parent1] = parent2
            self.size[parent2] += self.size[parent1]

    def connected(self, p1: Point, p2: Point) -> bool:
        return self._find(p1) == self._find(p2)
    
    def getSize(self, point: Point) -> int:
        return self.size[self._find(point)]

    def _find(self, p: Point) -> int:
        p = self._getIndex(p)

        while p != self.id[p]:
            self.id[p] = self.id[self.id[p]] # path compression - make every other node point to its grandparent
            p = self.id[p]
        
        return p
    
    def _getIndex(self, point: Point) -> int:
        return (point.y * self.width) + point.x
