import pprint
import unittest
import json

from app import logic, structures

class TestGetMove(unittest.TestCase):
    """Test template:
    def test_<NAME>(self):
        mock = formatJson(<JSON RESPONSE STRING>)
        self.assertEqual(<ACTUAL RESULT>, <EXPECTED RESULT>, msg=str(structures.Game(mock)))
    """

    def test_avoid_wall_down(self):
        mock = { "board": {"height": 2, "width": 1, "food": [], "snakes": []}, "you": {"id": "", "name": "testsnake", "health": 90, "body": [{"x": 0, "y": 0}]}, }
        self.assertEqual(logic.getMove(mock), ("down", logic.Mode.defend), msg=str(structures.Game(mock)))

    def test_avoid_wall_up(self):
        mock = { "board": {"height": 2, "width": 1, "food": [], "snakes": []}, "you": {"id": "", "name": "testsnake", "health": 90, "body": [{"x": 0, "y": 1}]}, }
        self.assertEqual(logic.getMove(mock), ("up", logic.Mode.defend), msg=str(structures.Game(mock)))

    def test_avoid_wall_left(self):
        mock = { "board": {"height": 1, "width": 2, "food": [], "snakes": []}, "you": {"id": "", "name": "testsnake", "health": 90, "body": [{"x": 1, "y": 0}]}, }
        self.assertEqual(logic.getMove(mock), ("left", logic.Mode.defend), msg=str(structures.Game(mock)))

    def test_avoid_wall_right(self):
        mock = { "board": {"height": 1, "width": 2, "food": [], "snakes": []}, "you": {"id": "", "name": "testsnake", "health": 90, "body": [{"x": 0, "y": 0}]}, }
        self.assertEqual(logic.getMove(mock), ("right", logic.Mode.defend), msg=str(structures.Game(mock)))

    def test_eat_down(self):
        mock = { "board": {"height": 3, "width": 1, "food": [{"x": 0, "y": 2}], "snakes": []}, "you": {"id": "", "name": "testsnake", "health": 40, "body": [{"x": 0, "y": 1}]}, }
        self.assertEqual(logic.getMove(mock), ("down", logic.Mode.hungry), msg=str(structures.Game(mock)))

    def test_eat_up(self):
        mock = { "board": {"height": 3, "width": 1, "food": [{"x": 0, "y": 0}], "snakes": []}, "you": {"id": "", "name": "testsnake", "health": 40, "body": [{"x": 0, "y": 1}]}, }
        self.assertEqual(logic.getMove(mock), ("up", logic.Mode.hungry), msg=str(structures.Game(mock)))

    def test_avoid_trap_right(self):
        mock = {"board": {"height": 11, "width": 11, "food": [], "snakes": []}, "you": { "id": "", "name": "testsnake", "health": 60, "body": [ {"x": 4, "y": 0}, {"x": 4, "y": 1}, {"x": 4, "y": 2}, {"x": 4, "y": 3}, {"x": 3, "y": 3}, {"x": 3, "y": 4}, {"x": 2, "y": 4}, {"x": 2, "y": 3}, {"x": 1, "y": 3}, {"x": 1, "y": 4}, {"x": 0, "y": 4}, {"x": 0, "y": 3}, {"x": 0, "y": 2}, {"x": 0, "y": 1}, {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 1, "y": 1}, ], },}
        self.assertEqual(logic.getMove(mock), ("right", logic.Mode.defend), msg=str(structures.Game(mock)))

    def test_grow_up(self):
        mock = { "board": { "height": 11, "width": 11, "food": [ {"x": 1, "y": 3}, {"x": 2, "y": 5}, {"x": 2, "y": 10}, {"x": 6, "y": 8}, ], "snakes": [ { "id": "", "name": "testenemy", "health": 90, "body": [{"x": 1, "y": 4}, {"x": 2, "y": 4}, {"x": 3, "y": 4}], } ], }, "you": { "id": "", "name": "testsnake", "health": 90, "body": [{"x": 0, "y": 3}, {"x": 0, "y": 4}, {"x": 0, "y": 5}], }, }
        self.assertEqual(logic.getMove(mock), ("up", logic.Mode.grow), msg=str(structures.Game(mock)))

    def test_grow_right(self):
        mock = { "board": { "height": 11, "width": 11, "food": [{"x": 2, "y": 7}, {"x": 5, "y": 10}], "snakes": [ {"id": "", "name": "testenemy", "health": 90, "body": [{"x": 0, "y": 6}, {"x": 0, "y": 5}, {"x": 1, "y": 5}]}, {"id": "", "name": "testenemy2", "health": 90, "body": [{"x": 4, "y": 2}, {"x": 3, "y": 2}, {"x": 2, "y": 2}]}, {"id": "", "name": "testenemy3", "health": 90, "body": [{"x": 8, "y": 8}, {"x": 7, "y": 8}, {"x": 7, "y": 6}, {"x": 7, "y": 5}, {"x": 7, "y": 4}, {"x": 7, "y": 3}, {"x": 7, "y": 2}, {"x": 7, "y": 1}]}, ], }, "you": {"id": "", "name": "testsnake", "health": 90, "body": [{"x": 1, "y": 7}, {"x": 1, "y": 8}, {"x": 2, "y": 8}],}, }
        self.assertEqual(logic.getMove(mock), ("right", logic.Mode.grow), msg=str(structures.Game(mock)))
    def test_avoid_enemy_right(self):
        mock = { "board": { "height": 3, "width": 3, "food": [], "snakes": [ {"id": "", "name": "testenemy", "health": 90, "body": [{"x": 0, "y": 0}]}, {"id": "", "name": "testenemy2", "health": 90, "body": [{"x": 0, "y": 1}]}, ], }, "you": {"id": "", "name": "testsnake", "health": 90, "body": [{"x": 1, "y": 0}]}, }
        self.assertEqual(logic.getMove(mock), ("right", logic.Mode.defend), msg=str(structures.Game(mock)))

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

if __name__ == "__main__":
    unittest.main()
