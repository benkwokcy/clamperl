"""Data structures used by logic.py"""

import heapq
from enum import Enum
from typing import List
import random

class Direction(Enum):
    """The /move endpoint expects a string of this form."""
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

def randomDirection():
    """Use this if we're going to die no matter what."""
    return random.choice([d.value for d in Direction])

class Mood(Enum):
    """Sets the maximum riskiness allowed by getMoves.
    
    This allows us to easily configure the behavior of the snake.
    Anywhere you see mood as a parameter, you can modify it to make
    the snake act safer or riskier.
    """
    SAFE = 3 # only moves with no chance of death
    RISKY = 5 # include moves with some chance of death
    ALL = 6 # include moves where we definitely die

class State(Enum):
    """Each position on the game board is given one of these states."""
    SELF_TAIL = 1
    EMPTY = 2
    FOOD = 3
    ENEMY_TAIL = 4
    ENEMY_HEAD_AREA_WEAK = 5
    ENEMY_HEAD_AREA_EQUAL = 6
    ENEMY_HEAD_AREA_STRONG = 7
    SELF_BODY = 8
    ENEMY_BODY = 9

def getRisk(state: State) -> int:
    """Allows me to rank moves by the danger level of their states."""
    risk = {
        # SAFE
        State.FOOD: 0, # grab food if possible
        State.SELF_TAIL: 1,
        State.ENEMY_HEAD_AREA_WEAK: 1, # a point reachable by an enemy head who's length is less than ours
        State.EMPTY: 2,
        State.ENEMY_TAIL: 3,

        # POSSIBLE DEATH
        State.ENEMY_HEAD_AREA_EQUAL: 4, # a point reachable by an enemy head who's length is greater than or equal to ours
        State.ENEMY_HEAD_AREA_STRONG: 5, # a point reachable by an enemy head who's length is greater than ours

        # DEFINITE DEATH
        State.ENEMY_BODY: 6,
        State.SELF_BODY: 6,
    }

    return risk[state]

class Point:
    """A 2D point representing a position on the game board."""
    def __init__(self, data):
        self.x = data["x"]
        self.y = data["y"]
        self.tup = (self.x, self.y)

    def up(self):
        return Point({"x": self.x, "y": self.y-1})
    
    def down(self):
        return Point({"x": self.x, "y": self.y+1})

    def left(self):
        return Point({"x": self.x-1, "y": self.y})

    def right(self):
        return Point({"x": self.x+1, "y": self.y})

    def allMoves(self):
        """Returns points for up, down, left, right."""
        moves = [
            Point({"x": self.x, "y": self.y-1}),
            Point({"x": self.x, "y": self.y+1}),
            Point({"x": self.x-1, "y": self.y}),
            Point({"x": self.x+1, "y": self.y})
        ]
        random.shuffle(moves) # snake tends to move in the same pattern if we don't randomize

        return moves
    
    def distance(self, other):
        """Manhattan distance between this point and another point."""
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    def __str__(self):
        """Overrides the print representation."""
        return str(self.tup)
    
    def __eq__(self, other):
        """Override equality."""
        if type(other) is type(self):
            return self.tup == other.tup
        else:
            return False
    
    def __lt__(self, other):
        """Needed to break ties in heapq"""
        return sum(self.tup) < sum(other.tup)
    
    def __hash__(self):
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
        self.ate = self.size >= 2 and body[-1] == body[-2] # just ate food so there is a body part on top of the tail

class Game:
    """Contains the game board and all objects on the board.

    This is the main data structure for making decisions about the game.
    """
    def __init__(self, data: dict):
        self.height = data["board"]["height"]
        self.width = data["board"]["width"]
        self.board = [[State.EMPTY] * self.width for _ in range(self.height)]
        self.me = Snake(data["you"])
        self.enemies = [Snake(d) for d in data["board"]["snakes"]] 
        self.food = [] # minheap of food with distance as key
        self.uf = None # union find of connected areas on the board

        # myself
        self.setState(self.me.head, State.SELF_BODY)
        self.setStates(self.me.middle, State.SELF_BODY)
        self.setState(self.me.tail, State.SELF_BODY if self.me.ate else State.SELF_TAIL) # if just ate, the tail has a body part on top of it

        # enemies
        for enemy in self.enemies:
            # head on collisions kill the snake who is smaller. Equal lengths means both snakes die.
            for move in self.getMoves(enemy.head, Mood.RISKY):
                if self.me.size > enemy.size:
                    self.setState(move, State.ENEMY_HEAD_AREA_WEAK)
                elif self.me.size == enemy.size:
                    self.setState(move, State.ENEMY_HEAD_AREA_EQUAL)
                else:
                    self.setState(move, State.ENEMY_HEAD_AREA_STRONG)
            self.setState(enemy.head, State.ENEMY_BODY)
            self.setStates(enemy.middle, State.ENEMY_BODY)
            self.setState(enemy.tail, State.ENEMY_BODY if enemy.ate else State.ENEMY_TAIL) # if just ate, the tail has a body part on top of it

        # calculate reachable areas
        self.uf = UnionFind(self.board)
        for row in range(self.height):
            for col in range(self.width):
                p = Point({"x": col, "y": row})
                if getRisk(self.getState(p)) <= Mood.RISKY.value: 
                    for neighbour in self.getMoves(p, Mood.RISKY):
                        self.uf.union(p, neighbour)

        # food
        validHeadMoves = self.getMoves(self.me.head, Mood.RISKY)
        for coordinates in data["board"]["food"]:
            point = Point(coordinates)
            self.setState(point, State.FOOD)
            if any([self.uf.connected(x, point) for x in validHeadMoves]): # only push food reachable from the head
                # we want food that is close but we also want food that is in a big open area
                normalizedDistance = point.distance(self.me.head) / (self.height + self.width)
                normalizedAreaSize = self.uf.getSize(point) / (self.height * self.width)
                weightedAverage = ((normalizedDistance * 0.3) - (normalizedAreaSize * 0.7)) / 2 # you can fiddle with these weights
                heapq.heappush(self.food, (weightedAverage, point)) 

    def setState(self, point: Point, state: State):
        """Set a state at a point, if the risk is higher or the point is empty."""
        boardState = self.board[point.y][point.x]
        if boardState == State.EMPTY or getRisk(state) > getRisk(self.board[point.y][point.x]):
            self.board[point.y][point.x] = state

    def setStates(self, points, state):
        """Same as setState but takes a list of points."""
        for point in points:
            self.setState(point, state)

    def getState(self, point: Point) -> State:
        """Get state from a point on the board."""
        return self.board[point.y][point.x]
    
    def getMoves(self, point: Point, mood: Mood) -> List[Point]:
        """Get all valid moves from a point that have risk <= mood."""

        # All moves that are inside the board and have risk <= mood.
        moves = [m for m in point.allMoves() if self.isValid(m) and getRisk(self.getState(m)) <= mood.value]

        return moves

    def isValid(self, point: Point) -> bool:
        """Check if a point is within the game board boundaries."""
        return 0 <= point.x < self.width and 0 <= point.y < self.height

    def directionFromHead(self, point: Point) -> str:
        """Given a valid move from the head, return its direction as a string."""
        head = self.me.head
        directions = {
            (head.x, head.y-1): Direction.UP,
            (head.x, head.y+1): Direction.DOWN,
            (head.x-1, head.y): Direction.LEFT,
            (head.x+1, head.y): Direction.RIGHT,
        }

        assert (point.tup in directions), "Point wasn't a valid move from head."

        return directions[point.tup].value

    def aStar(self, dest: Point, mood: Mood) -> List[Point]:
        """A* Algorithm.
        
        Figures out the shortest path to a destination from the head.
        Heuristic is the manhattan distance to the destination point.
        """
        head = self.me.head
        heap = [(dest.distance(head), head)]
        pathCost = {head.tup: 0} # path cost so far from destination
        parent = {head: head} # the point preceding another point in the path

        while heap:
            _, move = heapq.heappop(heap)
            if move == dest:
                return self.getPath(parent, dest) # path found
            for neighbour in self.getMoves(move, mood):
                if neighbour.tup not in pathCost or pathCost[move.tup] + 1 < pathCost[neighbour.tup]:
                    parent[neighbour] = move
                    pathCost[neighbour.tup] = pathCost[move.tup] + 1
                    heapq.heappush(heap, (pathCost[neighbour.tup] + dest.distance(neighbour), neighbour))

        return None # no path to destination

    def getPath(self, parent: Point, dest: Point) -> List[Point]:
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
        parent1 = self.find(p1)
        parent2 = self.find(p2)

        if parent1 == parent2:
            return
        
        # link the smaller tree to the root of the bigger tree
        if self.size[parent1] >= self.size[parent2]:
            self.id[parent2] = parent1
            self.size[parent1] += self.size[parent2]
        else:
            self.id[parent1] = parent2
            self.size[parent2] += self.size[parent1]
    
    def find(self, p: Point) -> int:
        p = self.getIndex(p)

        while p != self.id[p]:
            self.id[p] = self.id[self.id[p]] # path compression - make every other node point to its grandparent
            p = self.id[p]
        
        return p

    def connected(self, p1: Point, p2: Point) -> bool:
        return self.find(p1) == self.find(p2)

    def getIndex(self, point: Point) -> int:
        return (point.y * self.width) + point.x
    
    def getSize(self, point: Point) -> int:
        return self.size[self.find(point)]
