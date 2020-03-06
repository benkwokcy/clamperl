"""Data structures used by logic.py"""

import heapq
import random
import time
from collections import defaultdict
from enum import Enum, auto
from typing import List, Dict


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
    EMPTY = auto()
    FOOD = auto()
    SELF_HEAD = auto()
    SELF_BODY = auto()
    SELF_TAIL = auto()
    ENEMY_HEAD = auto()
    ENEMY_HEAD_AREA_WEAK = auto() # a point reachable by an enemy head who's length is less than ours
    ENEMY_HEAD_AREA_EQUAL = auto() # a point reachable by an enemy head who's length is equal to ours
    ENEMY_HEAD_AREA_STRONG = auto() # a point reachable by an enemy head who's length is greater than ours
    ENEMY_BODY = auto()
    ENEMY_TAIL = auto()

def getRisk(state: State) -> int:
    """Assign a riskiness value to each state.
    The higher the value, the more dangerous the state is.
    This allows me to compare moves and choose the safer options.
    """
    risk = {
        # SAFE
        State.FOOD: 0, # grab food if possible
        State.SELF_TAIL: 1,
        State.ENEMY_HEAD_AREA_WEAK: 1, # head on collision will kill the other snake.
        State.EMPTY: 2,
        State.ENEMY_TAIL: 3,

        # POSSIBLE DEATH
        State.ENEMY_HEAD_AREA_EQUAL: 4, # head on collision will kill both of us.
        State.ENEMY_HEAD_AREA_STRONG: 5, # head on collision will kill our snake.

        # DEFINITE DEATH
        State.SELF_HEAD: 6,
        State.SELF_BODY: 6,
        State.ENEMY_HEAD: 6,
        State.ENEMY_BODY: 6
    }

    return risk[state]

class Mood(Enum):
    """Assigns names to commonly used risk values.
    This is used to set the maximum riskiness allowed by the getMoves() function.
    When we do this, we can easily configure the behavior of the snake.
    Anywhere you see mood as a parameter, you can modify it to make the snake act
    safer or riskier.
    """
    SAFE = 3 # only moves with no chance of death
    RISKY = 5 # include moves with some chance of death
    ALL = 6 # include moves where we definitely die

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
        self.name = data["name"]
        self.head = Point(body[0])
        self.tail = Point(body[-1])
        self.middle = { Point(c) for c in body[1:-1] } # everything except the head and the tail
        self.size = len(body)
        self.health = data["health"]
        self.ate = (self.size >= 2) and (body[-1] == body[-2]) # just ate food so there is a body part on top of the tail

class Game:
    """Contains the game board and all objects on the board.
    This is the main data structure for making decisions about the game.
    """
    def __init__(self, data: dict):
        self.id = data.get("game", { "id": "0" })["id"]
        self.turn = data.get("turn", "0")
        self.height = data["board"]["height"]
        self.width = data["board"]["width"]
        self.board = [[State.EMPTY] * self.width for _ in range(self.height)]
        self.me = Snake(data["you"])
        self.enemies = [Snake(d) for d in data["board"]["snakes"] if d["name"] != self.me.name] 
        self.food = []
        self.uf = UnionFind(self.board) # connected areas

        # myself
        self.setState(self.me.head, State.SELF_HEAD)
        self.setStates(self.me.middle, State.SELF_BODY)
        self.setState(self.me.tail, State.SELF_BODY if self.me.ate else State.SELF_TAIL) # if just ate, the tail has a body part on top of it

        # food
        for coordinates in data["board"]["food"]:
            self.food.append(Point(coordinates))
            self.setState(Point(coordinates), State.FOOD)

        # enemies
        for enemy in self.enemies:
            for move in self.getMoves(enemy.head, Mood.RISKY):
                if self.me.size > enemy.size:
                    self.setState(move, State.ENEMY_HEAD_AREA_WEAK)
                elif self.me.size == enemy.size:
                    self.setState(move, State.ENEMY_HEAD_AREA_EQUAL)
                else:
                    self.setState(move, State.ENEMY_HEAD_AREA_STRONG)
            self.setState(enemy.head, State.ENEMY_HEAD)
            self.setStates(enemy.middle, State.ENEMY_BODY)
            self.setState(enemy.tail, State.ENEMY_BODY if enemy.ate else State.ENEMY_TAIL) # if just ate, the tail has a body part on top of it

        # calculate reachable areas
        for row in range(self.height):
            for col in range(self.width):
                p = Point({"x": col, "y": row})
                if getRisk(self.getState(p)) <= Mood.RISKY.value: 
                    for neighbour in self.getMoves(p, Mood.RISKY):
                        self.uf.union(p, neighbour)

    def setState(self, point: Point, state: State):
        """Set a state at a point, if the risk is higher or the point is empty."""
        boardState = self.board[point.y][point.x]
        if boardState == State.EMPTY or getRisk(state) > getRisk(boardState):
            self.board[point.y][point.x] = state

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

        moves = [ 
            Point({"x": point.x, "y": point.y-1}), 
            Point({"x": point.x, "y": point.y+1}), 
            Point({"x": point.x-1, "y": point.y}), 
            Point({"x": point.x+1, "y": point.y})
        ]

        # All moves that are inside the board and have risk <= mood
        moves = [m for m in moves if isValid(m) and getRisk(self.getState(m)) <= mood.value]

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
    
    def simulateMove(self, move: Point) -> float:
        """Simulate one move into the future and return the estimated risk of that future state.

        We calculate multiple future states and take the average score.
        In each future, our snake takes the given move and the enemy snakes take a random move.
        The score is based on the size of the area our snake ends up in. We prefer areas connected by
        safe moves.
        """
        originalBoard = [row[:] for row in self.board] # deep copy of board state
        numFutures = 3

        # we will calculate numFutures futures and take the average
        for _ in range(numFutures):

            # set up future board state
            if self.getState(self.me.tail) == State.SELF_TAIL:
                self.board[self.me.tail.y][self.me.tail.x] = State.EMPTY
            self.setState(self.me.head, State.SELF_BODY)
            self.setState(move, State.SELF_HEAD)

            for enemy in self.enemies:
                if self.getState(enemy.tail) == State.ENEMY_TAIL:
                    self.board[enemy.tail.y][enemy.tail.x] = State.EMPTY            
                self.setState(enemy.head, State.SELF_BODY)
                possibleMoves = set(self.getMoves(enemy.head, Mood.RISKY))
                if possibleMoves:
                    enemyMove = possibleMoves.pop() # each enemy takes a random move
                    self.setState(enemyMove, State.ENEMY_HEAD)
                    for p in self.getMoves(enemyMove, Mood.SAFE):
                        self.setState(p, State.ENEMY_HEAD_AREA_STRONG if enemy.size > self.me.size else State.ENEMY_HEAD_AREA_EQUAL)

            # calculate area sizes
            safeSize = self.getAreaSize(move, Mood.SAFE)
            riskySize = self.getAreaSize(move, Mood.RISKY)

            if safeSize <= self.me.size:
                return 1
            if riskySize <= self.me.size:
                return 0.5

            # restore board state
            self.board = originalBoard

        return 0

    def getAreaSize(self, p: Point, mood: Mood) -> int:
        """Area size not including the given point, 
        if we only take points obeying the given mood.
        
        Use this instead of UnionFind if you only care
        about the size of a single connected area.
        """
        seen = set([p])
        stack = [p]
        size = 0

        while stack:
            curr = stack.pop()
            for neighbour in self.getMoves(curr, mood):
                if neighbour not in seen:
                    seen.add(neighbour)
                    stack.append(neighbour)
                    size += 1

        return size

    def aStar(self, dest: Point, firstMoveMood: Mood, pathMood: Mood) -> List[Point]:
        """A* Algorithm.
        Figures out the shortest path to a destination from the head.
        Heuristic is the "manhattan" distance to the destination point.
        
        Takes two moods.
        firstMoveMood = maximum risk level allowed for the first move from the head.
        pathMood = maximum risk level allowed for remaining moves in the path.

        For example, we find paths where the first move is safe and the rest of the
        moves are risky.
        """

        def getPath(parent: Dict[Point, Point], dest: Point) -> List[Point]:
            """Reconstruct path from a parent pointer array.
            Path returned does not include the source.
            """
            path = []

            p = dest
            while parent[p] != self.me.head:
                path.append(p)
                p = parent[p]

            path.append(p)

            return path[::-1]

        head = self.me.head
        heap = [(dest.distance(head), head)]
        pathCost = {head.tup: 0} # path cost so far from destination
        parent = {head: head} # the point preceding another point in the path

        while heap:
            _, move = heapq.heappop(heap)
            if move == dest:
                return getPath(parent, dest) # path found
            for neighbour in self.getMoves(move, firstMoveMood if move == head else pathMood):
                if neighbour.tup not in pathCost or pathCost[move.tup] + 1 < pathCost[neighbour.tup]:
                    parent[neighbour] = move
                    pathCost[neighbour.tup] = pathCost[move.tup] + 1
                    heapq.heappush(heap, (pathCost[neighbour.tup] + dest.distance(neighbour), neighbour))

        return None # no path to destination

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
                return "@"
            elif state == State.ENEMY_BODY:
                return "X"
            elif state == State.ENEMY_TAIL:
                return "<"
            else:
                return " "

        result = ["\n"]
        for row in self.board:
            result.append("[" + "|".join([symbol(state) for state in row]) + "]")
        result.append(f"Health: {self.me.health}")

        return "\n".join(result)

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
