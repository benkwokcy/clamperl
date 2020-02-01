from enum import Enum
from collections import namedtuple

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

    def up(self):
        return Point({"x": self.x, "y": self.y+1})
    
    def down(self):
        return Point({"x": self.x, "y": self.y-1})

    def left(self):
        return Point({"x": self.x-1, "y": self.y})

    def right(self):
        return Point({"x": self.x+1, "y": self.y})

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
    
    def getSafeMoves(self):
        moves = (self.me.head.up(), self.me.head.down(), self.me.head.left(), self.me.head.right())
        directions = (Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT)

        return [direction for move, direction in zip(moves, directions) if self.isSafe(move)]

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