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

    def test_eat_right(self):
        mock = formatJson('{"Turn":97,"Food":[{"X":8,"Y":9},{"X":9,"Y":10},{"X":10,"Y":6}],"Snakes":[{"ID":"gs_V8R79TJtSbDjb3YtdDMqQRP9","Name":"benkwokcy / huntail","URL":"","Body":[{"X":1,"Y":6},{"X":1,"Y":7},{"X":1,"Y":8},{"X":1,"Y":9},{"X":2,"Y":9}],"Health":12,"Death":null,"Color":"#d897cb","HeadType":"tongue","TailType":"round-bum","Latency":"93","Shout":""},{"ID":"gs_KPPYQ7jHvCX7MmYHd8mTPvqF","Name":"adriaanwm / dontdie","URL":"","Body":[{"X":8,"Y":3},{"X":8,"Y":2},{"X":9,"Y":2},{"X":10,"Y":2},{"X":10,"Y":3},{"X":9,"Y":3},{"X":9,"Y":4},{"X":8,"Y":4},{"X":7,"Y":4},{"X":6,"Y":4},{"X":5,"Y":4},{"X":4,"Y":4},{"X":3,"Y":4},{"X":2,"Y":4},{"X":1,"Y":4}],"Health":97,"Death":null,"Color":"#000000","HeadType":"sand-worm","TailType":"block-bum","Latency":"167","Shout":""},{"ID":"gs_SpTmPVj3w6RVkP7tgXqDF9Kd","Name":"jonasstenberg / Ktrip","URL":"","Body":[{"X":5,"Y":-1},{"X":5,"Y":0},{"X":5,"Y":1},{"X":5,"Y":1}],"Health":99,"Death":{"Cause":"wall-collision","Turn":2},"Color":"#491010","HeadType":"","TailType":"","Latency":"360","Shout":""},{"ID":"gs_cb4PypKHVCjxtXByqfwJMhGd","Name":"ian321 / Snake #1","URL":"","Body":[{"X":1,"Y":-1},{"X":1,"Y":0},{"X":1,"Y":1},{"X":1,"Y":2}],"Health":98,"Death":{"Cause":"wall-collision","Turn":10},"Color":"#00FFFF","HeadType":"smile","TailType":"hook","Latency":"0","Shout":""}]}')
        self.assertEqual(logic.getMove(mock), ("right", logic.Mode.hungry), msg=str(structures.Game(mock)))

    def test_eat_right_2(self):
        mock = formatJson('{"Turn":213,"Food":[{"X":10,"Y":2},{"X":1,"Y":6},{"X":8,"Y":3},{"X":9,"Y":3},{"X":10,"Y":3},{"X":8,"Y":2},{"X":3,"Y":7},{"X":7,"Y":6},{"X":2,"Y":7},{"X":4,"Y":1},{"X":2,"Y":0},{"X":1,"Y":7},{"X":10,"Y":4},{"X":10,"Y":0},{"X":1,"Y":9},{"X":10,"Y":6},{"X":7,"Y":5},{"X":3,"Y":3},{"X":4,"Y":7},{"X":0,"Y":7},{"X":10,"Y":5},{"X":10,"Y":10},{"X":0,"Y":4},{"X":9,"Y":7},{"X":2,"Y":6},{"X":4,"Y":9},{"X":4,"Y":0},{"X":4,"Y":2},{"X":0,"Y":5},{"X":3,"Y":5}],"Snakes":[{"ID":"gs_XGyDpmGxBqcfRgbSVVm3BWtW","Name":"shoya4000 / Battlesnake-Hordes","URL":"","Body":[{"X":2,"Y":9},{"X":2,"Y":8},{"X":1,"Y":8},{"X":0,"Y":8},{"X":0,"Y":9},{"X":0,"Y":10},{"X":1,"Y":10},{"X":1,"Y":10}],"Health":100,"Death":null,"Color":"#cd681e","HeadType":"","TailType":"","Latency":"80","Shout":""},{"ID":"gs_FPHbQSdjj3xGcJ93DYBTp48V","Name":"owenj / bad snake","URL":"","Body":[{"X":1,"Y":-1},{"X":1,"Y":0},{"X":1,"Y":1}],"Health":98,"Death":{"Cause":"wall-collision","Turn":2},"Color":"#8f4949","HeadType":"","TailType":"","Latency":"0","Shout":""},{"ID":"gs_kKg7rJKY7W98QPSXDxcvRpyX","Name":"anosim114 / snake 0.0.3","URL":"","Body":[{"X":9,"Y":-1},{"X":9,"Y":0},{"X":9,"Y":1}],"Health":98,"Death":{"Cause":"wall-collision","Turn":2},"Color":"#cdcb1e","HeadType":"","TailType":"","Latency":"0","Shout":""},{"ID":"gs_t76FM6GbkcJrQXkCDd8rVKj8","Name":"battlesnake / Training Snake 7","URL":"","Body":[{"X":1,"Y":-1},{"X":1,"Y":0},{"X":1,"Y":1},{"X":1,"Y":2}],"Health":95,"Death":{"Cause":"wall-collision","Turn":10},"Color":"#1ecd3f","HeadType":"","TailType":"","Latency":"0","Shout":""},{"ID":"gs_g7SvJRhdfWT8SfVwR6jWMdPY","Name":"jnorth / help!","URL":"","Body":[{"X":9,"Y":-1},{"X":9,"Y":0},{"X":9,"Y":1}],"Health":94,"Death":{"Cause":"wall-collision","Turn":6},"Color":"#49628f","HeadType":"","TailType":"","Latency":"0","Shout":""},{"ID":"gs_XMVWxdB6gwyhbY8DF9DdRyXC","Name":"benkwokcy / huntail","URL":"","Body":[{"X":6,"Y":5},{"X":6,"Y":4},{"X":6,"Y":3},{"X":6,"Y":2},{"X":6,"Y":1},{"X":6,"Y":0},{"X":5,"Y":0},{"X":5,"Y":1},{"X":5,"Y":2},{"X":5,"Y":3},{"X":5,"Y":4},{"X":5,"Y":5},{"X":5,"Y":6},{"X":5,"Y":7},{"X":5,"Y":8}],"Health":38,"Death":null,"Color":"#d897cb","HeadType":"tongue","TailType":"round-bum","Latency":"354","Shout":""}]}')
        self.assertEqual(logic.getMove(mock), ("right", logic.Mode.hungry), msg=str(structures.Game(mock)))

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

    def test_grow_left(self):
        mock = formatJson('{"Turn":40,"Food":[{"X":2,"Y":2},{"X":2,"Y":9},{"X":2,"Y":7},{"X":4,"Y":3},{"X":10,"Y":0},{"X":4,"Y":8}],"Snakes":[{"ID":"gs_CJgbP8p4Fcw9SvPDQX94RVCP","Name":"vadimbrodsky / Solid SNEK","URL":"","Body":[{"X":6,"Y":2},{"X":7,"Y":2},{"X":7,"Y":3},{"X":7,"Y":4},{"X":8,"Y":4}],"Health":76,"Death":null,"Color":"#628f49","HeadType":"","TailType":"","Latency":"83","Shout":""},{"ID":"gs_4dFwRDjXHdXYVKTdMgMVFFYD","Name":"dupdup / dupdup","URL":"","Body":[{"X":1,"Y":-1},{"X":1,"Y":0},{"X":1,"Y":1},{"X":1,"Y":2}],"Health":93,"Death":{"Cause":"wall-collision","Turn":10},"Color":"#8f7f49","HeadType":"","TailType":"","Latency":"0","Shout":""},{"ID":"gs_rWbGDXVkpG8WWXBkjRXxkMwV","Name":"ttttin / TTTTin","URL":"","Body":[{"X":1,"Y":-1},{"X":1,"Y":0},{"X":1,"Y":1}],"Health":94,"Death":{"Cause":"wall-collision","Turn":6},"Color":"#491010","HeadType":"","TailType":"","Latency":"0","Shout":""},{"ID":"gs_SffRBY6GW9f7XpwgXHq3d64H","Name":"cindyunrau / worm","URL":"","Body":[{"X":5,"Y":-1},{"X":5,"Y":0},{"X":5,"Y":1}],"Health":98,"Death":{"Cause":"wall-collision","Turn":2},"Color":"#493810","HeadType":"","TailType":"","Latency":"0","Shout":""},{"ID":"gs_MFJ3XSdKcJmmfvvttTpyQj9W","Name":"declanmcintosh / Kevin","URL":"","Body":[{"X":1,"Y":-1},{"X":1,"Y":0},{"X":1,"Y":1}],"Health":98,"Death":{"Cause":"wall-collision","Turn":2},"Color":"#7f498f","HeadType":"","TailType":"","Latency":"0","Shout":""},{"ID":"gs_yTgqKdj4Ph4WkwvMpx8vXd6S","Name":"benkwokcy / huntail","URL":"","Body":[{"X":5,"Y":3},{"X":5,"Y":4},{"X":5,"Y":5},{"X":5,"Y":6},{"X":5,"Y":7}],"Health":82,"Death":null,"Color":"#d897cb","HeadType":"tongue","TailType":"round-bum","Latency":"106","Shout":""}]}')
        self.assertEqual(logic.getMove(mock), ("left", logic.Mode.grow), msg=str(structures.Game(mock)))

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
