import heapq
from enum import Enum
from typing import List
import random

# maximum riskiness allowed by getMoves()
class Mood(Enum):
    SAFE = 1
    AGGRESSIVE = 2
    RISKY = 3
    SUICIDAL = 4
    ALL = 5

# /move endpoint expects a lowercase string of this form
class Direction:
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

def randomDirection():
    return random.choice(list(Direction))

class State(Enum):
    SELF_TAIL = 1
    EMPTY = 2
    FOOD = 3
    ENEMY_TAIL = 4
    ENEMY_HEAD_AREA_WEAK = 5
    ENEMY_HEAD_AREA_STRONG = 6,
    ENEMY_HEAD = 7
    SELF_BODY = 8
    ENEMY_BODY = 9

# allows me to rank moves by riskiness
def getRisk(state: State) -> int:
    risk = {
        # SUPER SAFE
        State.SELF_TAIL: 0,

        # SAFE
        State.ENEMY_TAIL: 1,
        State.EMPTY: 1,
        State.FOOD: 1,
        
        # ARGUEABLE
        State.ENEMY_HEAD_AREA_WEAK: 2, # can modify this to change aggressiveness

        # POSSIBLE DEATH
        State.ENEMY_HEAD_AREA_STRONG: 3,

        # DEFINITE DEATH
        State.ENEMY_HEAD: 4, # could take them out with me
        State.ENEMY_BODY: 5,
        State.SELF_BODY: 5,
    }

    return risk[state]

class Point:
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

    # all possible moves from current point
    def allMoves(self):
        return (
            Point({"x": self.x, "y": self.y-1}),
            Point({"x": self.x, "y": self.y+1}),
            Point({"x": self.x-1, "y": self.y}),
            Point({"x": self.x+1, "y": self.y})
        )
    
    # manhattan distance between this point and another point
    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    # overriding the print() representation
    def __str__(self):
        return str(self.tup)
    
    def __eq__(self, other):
        if type(other) is type(self):
            return self.tup == other.tup
        else:
            return False

class Snake:
    def __init__(self, data: dict):
        self.name = data["name"]
        self.head = Point(data["body"][0])
        self.tail = Point(data["body"][-1])
        self.middle = { Point(c) for c in data["body"][1:-1] } # everything except the head and the tail
        self.size = len(data["body"])
        self.health = data["health"]

    # can kill another snake who is smaller
    def canKill(self, other):
        return self.size > other.size

class Game:
    def __init__(self, data: dict):
        self.height = data["board"]["height"]
        self.width = data["board"]["width"]
        self.board = [[State.EMPTY] * self.width for _ in range(self.height)]
        self.me = Snake(data["you"])
        self.enemies = [Snake(d) for d in data["board"]["snakes"]]
        self.food = [] # minheap of food with distance as key
        self.uf = None # union find of connected areas on the board (separated by snake bodies)

        # food
        for coordinates in data["board"]["food"]:
            point = Point(coordinates)
            self.setState(point, State.FOOD)
            heapq.heappush(self.food, (point.distance(self.me.head), point))

        # myself
        self.setState(self.me.head, State.SELF_BODY)
        self.setStates(self.me.middle, State.SELF_BODY)
        self.setState(self.me.tail, State.SELF_TAIL)

        # enemies
        for enemy in self.enemies:
            for move in enemy.head.allMoves():
                if self.me.canKill(enemy):
                    self.setState(move, State.ENEMY_HEAD_AREA_WEAK)
                else:
                    self.setState(move, State.ENEMY_HEAD_AREA_STRONG)
            self.setState(enemy.head, State.ENEMY_HEAD)
            self.setStates(enemy.middle, State.ENEMY_BODY)
            self.setState(enemy.tail, State.ENEMY_TAIL)

        # calculate reachable areas
        self.uf = UnionFind(self.board)
        for row in range(self.height):
            for col in range(self.width):
                p = Point({"x": col, "y": row})
                for neighbour in self.getMoves(p):
                    self.uf.union(p, neighbour)

    # set a state at a point, if the risk is higher or the point is empty
    def setState(self, point: Point, state: State):
        boardState = self.board[point.y][point.x]
        if boardState == State.EMPTY or getRisk(state) > getRisk(self.board[point.y][point.x]):
            self.board[point.y][point.x] = state

    # same as setState but takes a list of points    
    def setStates(self, points, state):
        for point in points:
            self.setState(point, state)

    # get state from a point
    def getState(self, point: Point) -> State:
        return self.board[point.y][point.x]
    
    # get all valid moves from a point, sorted by increasing risk and decreasing area size, where risk is capped by mood
    def getMoves(self, point: Point, mood: Mood) -> List[Point]:
        moves = [m for m in point.allMoves() if self.isValid(m) and self.getRisk(m) <= mood.value]
        moves.sort(key = lambda m: (getRisk(self.getState(m)), -self.uf.getSize(m)))

        return moves

    def isValid(self, point: Point) -> bool:
        return 0 <= point.x < self.width and 0 <= point.y < self.height

    # given a valid move from the head, return its Direction type
    def directionFromHead(self, point: Point) -> Direction:
        head = self.me.head
        directions = {
            (head.x, head.y-1): Direction.UP,
            (head.x, head.y+1): Direction.DOWN,
            (head.x-1, head.y): Direction.LEFT,
            (head.x+1, head.y): Direction.RIGHT,
        }

        assert (point.tup in directions), "Point wasn't a valid move from head."

        return directions[point.tup]

    # A* algorithm - find the shortest path to move towards a destination from the head
    # and return the first move and the length of the path
    def aStar(self, dest: Point, mood: Mood) -> (Direction, int):
        head = self.me.head
        heap = [(dest.distance(head), head)]
        pathCost = {head.tup: 0}
        parent = {head.tup: head.tup}

        while heap:
            move,_ = heapq.heappop(heap)
            if move == dest:
                parent[dest.tup] = move.tup
                path = self.getPath(parent, dest)
                return (self.directionFromHead(path[0]), len(path))
            for neighbour in self.getMoves(move, mood):
                # TODO - use this to move to the food

        return (randomDirection(), -1) # if unreachable,

    # reconstruct shortest path from parent array for A*
    # path returned does not include the source
    def getPath(self, parent, dest):
        path = []

        p = dest
        while parent[p] != self.me.head:
            path.append(p)
            p = parent[p]

        path.append(p)

        return path[::-1]

# Weighted UnionFind
# all the functions take in Point objects for convenience
# however the id and size lists are indexed by int indices (see getIndex())
# TODO: Path compression
class UnionFind:
    def __init__(self, board: List[List[State]]):
        self.height = len(board)
        self.width = len(board[0])
        self.id = [i for i in range(self.height * self.width)]
        self.size = [1 for i in range(self.height * self.width)]

    def union(self, p1: Point, p2: Point):
        if self.connected(p1, p2):
            return

        p1 = self.getIndex(p1)
        p2 = self.getIndex(p2)
        
        if self.size[p1] >= self.size[p2]:
            self.id[p2] = p1
            self.size[p1] += self.size[p2]
        else:
            self.id[p1] = p2
            self.size[p2] += self.size[p1]
    
    def find(self, p: Point) -> int:
        p = self.getIndex(p)

        while p != self.id[p]:
            p = self.id[p]
        
        return p

    def connected(self, p1: Point, p2: Point) -> bool:
        return self.find(p1) == self.find(p2)

    def getIndex(self, point: Point) -> int:
        return (point.y * self.width) + point.x
    
    def getSize(self, point: Point) -> int:
        return self.size[self.find(self.getIndex(point))]
