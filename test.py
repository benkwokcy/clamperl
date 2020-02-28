import pprint
import unittest
import json

from app import logic, structures

class TestGetMove(unittest.TestCase):
    """Convention for tests is assertEqual(ACTUAL, EXPECTED)"""

    def test_avoid_wall_down(self):
        mock = { "board": {"height": 2, "width": 1, "food": [], "snakes": []}, "you": {"id": "", "name": "testsnake", "health": 90, "body": [{"x": 0, "y": 0}]}, }
        self.assertEqual(logic.getMove(mock), ("down", logic.Mode.defend), msg=boardString(mock))

    def test_avoid_wall_up(self):
        mock = { "board": {"height": 2, "width": 1, "food": [], "snakes": []}, "you": {"id": "", "name": "testsnake", "health": 90, "body": [{"x": 0, "y": 1}]}, }
        self.assertEqual(logic.getMove(mock), ("up", logic.Mode.defend), msg=boardString(mock))

    def test_avoid_wall_left(self):
        mock = { "board": {"height": 1, "width": 2, "food": [], "snakes": []}, "you": {"id": "", "name": "testsnake", "health": 90, "body": [{"x": 1, "y": 0}]}, }
        self.assertEqual(logic.getMove(mock), ("left", logic.Mode.defend), msg=boardString(mock))

    def test_avoid_wall_right(self):
        mock = { "board": {"height": 1, "width": 2, "food": [], "snakes": []}, "you": {"id": "", "name": "testsnake", "health": 90, "body": [{"x": 0, "y": 0}]}, }
        self.assertEqual(logic.getMove(mock), ("right", logic.Mode.defend), msg=boardString(mock))

    def test_eat_down(self):
        mock = { "board": {"height": 3, "width": 1, "food": [{"x": 0, "y": 2}], "snakes": []}, "you": {"id": "", "name": "testsnake", "health": 40, "body": [{"x": 0, "y": 1}]}, }
        self.assertEqual(logic.getMove(mock), ("down", logic.Mode.hungry), msg=boardString(mock))

    def test_eat_up(self):
        mock = { "board": {"height": 3, "width": 1, "food": [{"x": 0, "y": 0}], "snakes": []}, "you": {"id": "", "name": "testsnake", "health": 40, "body": [{"x": 0, "y": 1}]}, }
        self.assertEqual(logic.getMove(mock), ("up", logic.Mode.hungry), msg=boardString(mock))

    def test_avoid_trap_right(self):
        mock = {"board": {"height": 11, "width": 11, "food": [], "snakes": []}, "you": { "id": "", "name": "testsnake", "health": 60, "body": [ {"x": 4, "y": 0}, {"x": 4, "y": 1}, {"x": 4, "y": 2}, {"x": 4, "y": 3}, {"x": 3, "y": 3}, {"x": 3, "y": 4}, {"x": 2, "y": 4}, {"x": 2, "y": 3}, {"x": 1, "y": 3}, {"x": 1, "y": 4}, {"x": 0, "y": 4}, {"x": 0, "y": 3}, {"x": 0, "y": 2}, {"x": 0, "y": 1}, {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 1, "y": 1}, ], },}
        self.assertEqual(logic.getMove(mock), ("right", logic.Mode.defend), msg=boardString(mock))

    def test_avoid_enemy_up(self):
        mock = { "board": { "height": 11, "width": 11, "food": [ {"x": 1, "y": 3}, {"x": 2, "y": 5}, {"x": 2, "y": 10}, {"x": 6, "y": 8}, ], "snakes": [ { "id": "", "name": "testenemy", "health": 90, "body": [{"x": 1, "y": 4}, {"x": 2, "y": 4}, {"x": 3, "y": 4}], } ], }, "you": { "id": "", "name": "testsnake", "health": 90, "body": [{"x": 0, "y": 3}, {"x": 0, "y": 4}, {"x": 0, "y": 5}], }, }
        self.assertEqual(logic.getMove(mock), ("up", logic.Mode.grow), msg=boardString(mock))

    def test_avoid_enemy_right(self):
        mock = { "board": { "height": 3, "width": 3, "food": [], "snakes": [ {"id": "", "name": "testenemy", "health": 90, "body": [{"x": 0, "y": 0}]}, {"id": "", "name": "testenemy2", "health": 90, "body": [{"x": 0, "y": 1}]}, ], }, "you": {"id": "", "name": "testsnake", "health": 90, "body": [{"x": 1, "y": 0}]}, }
        self.assertEqual(logic.getMove(mock), ("right", logic.Mode.defend), msg=boardString(mock))

    def test_avoid_enemy_right2(self):
        mock = { "board": { "height": 11, "width": 11, "food": [{"x": 2, "y": 7}, {"x": 5, "y": 10}], "snakes": [ {"id": "", "name": "testenemy", "health": 90, "body": [{"x": 0, "y": 6}, {"x": 0, "y": 5}, {"x": 1, "y": 5}]}, {"id": "", "name": "testenemy2", "health": 90, "body": [{"x": 4, "y": 2}, {"x": 3, "y": 2}, {"x": 2, "y": 2}]}, {"id": "", "name": "testenemy3", "health": 90, "body": [{"x": 8, "y": 8}, {"x": 7, "y": 8}, {"x": 7, "y": 6}, {"x": 7, "y": 5}, {"x": 7, "y": 4}, {"x": 7, "y": 3}, {"x": 7, "y": 2}, {"x": 7, "y": 1}]}, ], }, "you": {"id": "", "name": "testsnake", "health": 90, "body": [{"x": 1, "y": 7}, {"x": 1, "y": 8}, {"x": 2, "y": 8}],}, }
        self.assertEqual(logic.getMove(mock), ("right", logic.Mode.grow), msg=boardString(mock))

    def test_jar(self):
        mock = formatJson('{"Turn":166,"Food":[{"X":2,"Y":1},{"X":0,"Y":2},{"X":3,"Y":1},{"X":4,"Y":10},{"X":0,"Y":0},{"X":6,"Y":8},{"X":3,"Y":5},{"X":3,"Y":0},{"X":4,"Y":4},{"X":10,"Y":6},{"X":1,"Y":1}],"Snakes":[{"ID":"gs_WPBVpXKMQ4mwy9jGPBFDVkpb","Name":"codeallthethingz / d1!","URL":"","Body":[{"X":5,"Y":5},{"X":5,"Y":6},{"X":4,"Y":6},{"X":4,"Y":7},{"X":3,"Y":7},{"X":3,"Y":6}],"Health":82,"Death":null,"Color":"#5b35d7","HeadType":"pixel","TailType":"pixel","Latency":"73","Shout":""},{"ID":"gs_c77ygtGDqJKrQvMhtGBF7T6M","Name":"joram / jsnek-attempt-at-neural-net","URL":"","Body":[{"X":5,"Y":-1},{"X":5,"Y":0},{"X":5,"Y":1}],"Health":98,"Death":{"Cause":"wall-collision","Turn":2},"Color":"#1ecdc7","HeadType":"","TailType":"","Latency":"334","Shout":""},{"ID":"gs_xMyPbqdXyWHgpwG9B9x9Rxj6","Name":"benkwokcy / huntail","URL":"","Body":[{"X":5,"Y":3},{"X":6,"Y":3},{"X":7,"Y":3},{"X":8,"Y":3},{"X":8,"Y":4},{"X":8,"Y":5},{"X":9,"Y":5},{"X":10,"Y":5},{"X":10,"Y":4},{"X":9,"Y":4}],"Health":82,"Death":null,"Color":"#d897cb","HeadType":"tongue","TailType":"round-bum","Latency":"114","Shout":""},{"ID":"gs_gkKk7WJJxJH6GB6p7Wp7RGHf","Name":"joshhartmann11 / Jake The Snake","URL":"","Body":[{"X":5,"Y":7},{"X":5,"Y":8},{"X":4,"Y":8},{"X":3,"Y":8},{"X":2,"Y":8},{"X":1,"Y":8},{"X":1,"Y":9},{"X":2,"Y":9},{"X":3,"Y":9},{"X":4,"Y":9},{"X":5,"Y":9}],"Health":86,"Death":null,"Color":"#BEEF00","HeadType":"","TailType":"","Latency":"180","Shout":""}]}')
        self.assertEqual(logic.getMove(mock), ("right", logic.Mode.grow), msg=boardString(mock))

def formatJson(response: str) -> dict:
    """Convert the raw json response from Battlesnake Online Engine
    into a dictionary that is accepted by our Game board matrix. 

    You can grab these json responses from
    Developer Tools -> Network -> Websockets -> Messages. These responses
    can be imported here and turned into unit tests.
    """

    def formatList(l):
        """Takes a list of dictionaries and turns the keys to lowercase."""
        return [{k.lower():v for k,v in p.items()} for p in l]

    inputDict = json.loads(response)
    outputDict = {
        "board": {"height": 11, "width": 11, "food": [], "snakes": []},
        "you": {"id": "", "name": "testsnake", "health": 100, "body": []},
    }

    outputDict["board"]["food"] = formatList(inputDict["Food"])
    for snake in inputDict["Snakes"]:
        if snake["Death"]:
            continue
        if snake["Name"] == "benkwokcy / huntail":
            outputDict["you"]["health"] = snake["Health"]
            outputDict["you"]["body"] = formatList(snake["Body"])
        else:
            outputDict["board"]["snakes"].append(
                {
                    "id": "",
                    "name": "testenemy",
                    "health": snake["Health"],
                    "body": formatList(snake["Body"])
                }
            )
          
    return outputDict

def boardString(mock: dict) -> str:
    """Return printable representation of the game board so I 
    can easily see the state of the board for any test case."""

    def symbol(state):
        if state == structures.State.FOOD:
            return "F"
        elif state == structures.State.SELF_BODY:
            return "+"
        elif state == structures.State.SELF_TAIL:
            return ">"
        elif state in (structures.State.ENEMY_BODY, structures.State.ENEMY_TAIL):
            return "X"
        else:
            return " "

    board = structures.Game(mock).board
    strings = ["\n"]
    for row in board:
        strings.append("[" + "|".join([symbol(state) for state in row]) + "]")

    return "\n".join(strings)

if __name__ == "__main__":
    unittest.main()
