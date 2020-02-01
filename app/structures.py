from enum import Enum
from typing import List

class Direction:
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

class State(Enum):
    EMPTY = 1
    FOOD = 2
    SELF = 3
    ENEMY = 4

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

    def allMoves(self):
        return (
            Point({"x": self.x, "y": self.y-1}),
            Point({"x": self.x, "y": self.y+1}),
            Point({"x": self.x-1, "y": self.y}),
            Point({"x": self.x+1, "y": self.y})
        )
    
    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    def __str__(self):
        return str(self.tup)

class Snake:
    def __init__(self, data: dict):
        self.name = data["name"]
        self.parts = { Point(c) for c in data["body"] }
        self.head = Point(data["body"][0])
        self.health = data["health"]

class Game:
    def __init__(self, data: dict):
        self.height = data["board"]["height"]
        self.width = data["board"]["width"]
        self.board = [[State.EMPTY] * self.width for _ in range(self.height)]

        self.me = Snake(data["you"])
        self.enemies = [Snake(d) for d in data["board"]["snakes"]]

        for coordinates in data["board"]["food"]:
            point = Point(coordinates)
            self.setState(point, State.FOOD)
        for coordinates in data["you"]["body"]:
            point = Point(coordinates)
            self.setState(point, State.SELF)
        for snake in data["board"]["snakes"]:
            for coordinates in snake["body"]:
                point = Point(coordinates)
                self.setState(point, State.ENEMY)
    
    # get all safe moves from a point
    def getSafeMoves(self, point: Point) -> List[Point]:
        return [m for m in point.allMoves() if self.isSafe(m)]

    # set a state at a point
    def setState(self, point: Point, state: State):
        self.board[point.y][point.x] = state

    # get state from a point
    def getState(self, point: Point) -> State:
        return self.board[point.y][point.x]
    
    # see if a point is inside the board
    def inBounds(self, point: Point) -> bool:
        return 0 <= point.x < self.width and 0 <= point.y < self.height
    
    # see if you would die at a given point
    def isSafe(self, point: Point) -> bool:
        return self.inBounds(point) and self.getState(point) in (State.EMPTY, State.FOOD)

    # given a valid move from the head, return its state type
    def directionFromHead(self, point: Point) -> State:
        head = self.me.head
        directions = {
            (head.x, head.y-1): Direction.UP,
            (head.x, head.y+1): Direction.DOWN,
            (head.x-1, head.y): Direction.LEFT,
            (head.x+1, head.y): Direction.RIGHT,
        }

        assert (point.tup in directions), "Point wasn't a valid move from head."

        return directions[point.tup]