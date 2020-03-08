import pprint
import unittest
import json

from app import logic, structures

class TestGetMove(unittest.TestCase):
    """Test Template:
    def test_<NAME>(self):
        mock = formatJson(<JSON RESPONSE STRING>)
        self.assertEqual(<ACTUAL RESULT>, <EXPECTED RESULT>, msg=str(structures.Game(mock, "huntail")))
    """

    def test_eat_right(self):
        mock = formatJson('{"Turn":97,"Food":[{"X":8,"Y":9},{"X":9,"Y":10},{"X":10,"Y":6}],"Snakes":[{"ID":"gs_V8R79TJtSbDjb3YtdDMqQRP9","Name":"benkwokcy / huntail","URL":"","Body":[{"X":1,"Y":6},{"X":1,"Y":7},{"X":1,"Y":8},{"X":1,"Y":9},{"X":2,"Y":9}],"Health":12,"Death":null,"Color":"#d897cb","HeadType":"tongue","TailType":"round-bum","Latency":"93","Shout":""},{"ID":"gs_KPPYQ7jHvCX7MmYHd8mTPvqF","Name":"adriaanwm / dontdie","URL":"","Body":[{"X":8,"Y":3},{"X":8,"Y":2},{"X":9,"Y":2},{"X":10,"Y":2},{"X":10,"Y":3},{"X":9,"Y":3},{"X":9,"Y":4},{"X":8,"Y":4},{"X":7,"Y":4},{"X":6,"Y":4},{"X":5,"Y":4},{"X":4,"Y":4},{"X":3,"Y":4},{"X":2,"Y":4},{"X":1,"Y":4}],"Health":97,"Death":null,"Color":"#000000","HeadType":"sand-worm","TailType":"block-bum","Latency":"167","Shout":""},{"ID":"gs_SpTmPVj3w6RVkP7tgXqDF9Kd","Name":"jonasstenberg / Ktrip","URL":"","Body":[{"X":5,"Y":-1},{"X":5,"Y":0},{"X":5,"Y":1},{"X":5,"Y":1}],"Health":99,"Death":{"Cause":"wall-collision","Turn":2},"Color":"#491010","HeadType":"","TailType":"","Latency":"360","Shout":""},{"ID":"gs_cb4PypKHVCjxtXByqfwJMhGd","Name":"ian321 / Snake #1","URL":"","Body":[{"X":1,"Y":-1},{"X":1,"Y":0},{"X":1,"Y":1},{"X":1,"Y":2}],"Health":98,"Death":{"Cause":"wall-collision","Turn":10},"Color":"#00FFFF","HeadType":"smile","TailType":"hook","Latency":"0","Shout":""}]}')
        self.assertEqual(logic.getMove(mock, "huntail"), ("right", logic.Mode.hungry), msg=str(structures.Game(mock, "huntail")))

    def test_eat_right_2(self):
        mock = formatJson('{"Turn":213,"Food":[{"X":10,"Y":2},{"X":1,"Y":6},{"X":8,"Y":3},{"X":9,"Y":3},{"X":10,"Y":3},{"X":8,"Y":2},{"X":3,"Y":7},{"X":7,"Y":6},{"X":2,"Y":7},{"X":4,"Y":1},{"X":2,"Y":0},{"X":1,"Y":7},{"X":10,"Y":4},{"X":10,"Y":0},{"X":1,"Y":9},{"X":10,"Y":6},{"X":7,"Y":5},{"X":3,"Y":3},{"X":4,"Y":7},{"X":0,"Y":7},{"X":10,"Y":5},{"X":10,"Y":10},{"X":0,"Y":4},{"X":9,"Y":7},{"X":2,"Y":6},{"X":4,"Y":9},{"X":4,"Y":0},{"X":4,"Y":2},{"X":0,"Y":5},{"X":3,"Y":5}],"Snakes":[{"ID":"gs_XGyDpmGxBqcfRgbSVVm3BWtW","Name":"shoya4000 / Battlesnake-Hordes","URL":"","Body":[{"X":2,"Y":9},{"X":2,"Y":8},{"X":1,"Y":8},{"X":0,"Y":8},{"X":0,"Y":9},{"X":0,"Y":10},{"X":1,"Y":10},{"X":1,"Y":10}],"Health":100,"Death":null,"Color":"#cd681e","HeadType":"","TailType":"","Latency":"80","Shout":""},{"ID":"gs_FPHbQSdjj3xGcJ93DYBTp48V","Name":"owenj / bad snake","URL":"","Body":[{"X":1,"Y":-1},{"X":1,"Y":0},{"X":1,"Y":1}],"Health":98,"Death":{"Cause":"wall-collision","Turn":2},"Color":"#8f4949","HeadType":"","TailType":"","Latency":"0","Shout":""},{"ID":"gs_kKg7rJKY7W98QPSXDxcvRpyX","Name":"anosim114 / snake 0.0.3","URL":"","Body":[{"X":9,"Y":-1},{"X":9,"Y":0},{"X":9,"Y":1}],"Health":98,"Death":{"Cause":"wall-collision","Turn":2},"Color":"#cdcb1e","HeadType":"","TailType":"","Latency":"0","Shout":""},{"ID":"gs_t76FM6GbkcJrQXkCDd8rVKj8","Name":"battlesnake / Training Snake 7","URL":"","Body":[{"X":1,"Y":-1},{"X":1,"Y":0},{"X":1,"Y":1},{"X":1,"Y":2}],"Health":95,"Death":{"Cause":"wall-collision","Turn":10},"Color":"#1ecd3f","HeadType":"","TailType":"","Latency":"0","Shout":""},{"ID":"gs_g7SvJRhdfWT8SfVwR6jWMdPY","Name":"jnorth / help!","URL":"","Body":[{"X":9,"Y":-1},{"X":9,"Y":0},{"X":9,"Y":1}],"Health":94,"Death":{"Cause":"wall-collision","Turn":6},"Color":"#49628f","HeadType":"","TailType":"","Latency":"0","Shout":""},{"ID":"gs_XMVWxdB6gwyhbY8DF9DdRyXC","Name":"benkwokcy / huntail","URL":"","Body":[{"X":6,"Y":5},{"X":6,"Y":4},{"X":6,"Y":3},{"X":6,"Y":2},{"X":6,"Y":1},{"X":6,"Y":0},{"X":5,"Y":0},{"X":5,"Y":1},{"X":5,"Y":2},{"X":5,"Y":3},{"X":5,"Y":4},{"X":5,"Y":5},{"X":5,"Y":6},{"X":5,"Y":7},{"X":5,"Y":8}],"Health":38,"Death":null,"Color":"#d897cb","HeadType":"tongue","TailType":"round-bum","Latency":"354","Shout":""}]}')
        self.assertEqual(logic.getMove(mock, "huntail"), ("right", logic.Mode.hungry), msg=str(structures.Game(mock, "huntail")))

    def test_defend_up(self):
        mock = formatJson('{"Turn":266,"Food":[{"X":7,"Y":5}],"Snakes":[{"ID":"gs_Pkw9j4j3cDR9WjKrdXh8JSm3","Name":"huntail","URL":"","Body":[{"X":0,"Y":6},{"X":1,"Y":6},{"X":2,"Y":6},{"X":2,"Y":5},{"X":2,"Y":4},{"X":3,"Y":4},{"X":4,"Y":4},{"X":5,"Y":4},{"X":5,"Y":3},{"X":5,"Y":2},{"X":5,"Y":1},{"X":4,"Y":1},{"X":4,"Y":2},{"X":4,"Y":3},{"X":3,"Y":3},{"X":3,"Y":2},{"X":2,"Y":2},{"X":2,"Y":1},{"X":3,"Y":1},{"X":3,"Y":0},{"X":2,"Y":0},{"X":1,"Y":0},{"X":0,"Y":0},{"X":0,"Y":1},{"X":0,"Y":2},{"X":0,"Y":3},{"X":0,"Y":4},{"X":0,"Y":5}],"Health":96,"Death":null,"Color":"#d897cb","HeadType":"tongue","TailType":"round-bum","Latency":"92","Shout":"","Team":""},{"ID":"gs_Cp6H9FdXCdqh6wypV9hWYJPP","Name":"Sir Pent","URL":"","Body":[{"X":6,"Y":10},{"X":5,"Y":10},{"X":5,"Y":9},{"X":5,"Y":8},{"X":4,"Y":8},{"X":3,"Y":8},{"X":3,"Y":7},{"X":4,"Y":7},{"X":5,"Y":7},{"X":6,"Y":7},{"X":7,"Y":7},{"X":7,"Y":6},{"X":6,"Y":6},{"X":6,"Y":5},{"X":6,"Y":4},{"X":6,"Y":3},{"X":7,"Y":3},{"X":8,"Y":3},{"X":9,"Y":3},{"X":9,"Y":2},{"X":9,"Y":1},{"X":9,"Y":0},{"X":10,"Y":0},{"X":10,"Y":1},{"X":10,"Y":2},{"X":10,"Y":3},{"X":10,"Y":4},{"X":10,"Y":5},{"X":10,"Y":6},{"X":10,"Y":7}],"Health":99,"Death":null,"Color":"#FF0000","HeadType":"pixel","TailType":"pixel","Latency":"23","Shout":"Look out!","Team":""},{"ID":"gs_V7ytFKRDJYBxKV7DjmKY7RG3","Name":"Project Z","URL":"","Body":[{"X":0,"Y":5},{"X":0,"Y":6},{"X":0,"Y":7},{"X":1,"Y":7},{"X":2,"Y":7},{"X":2,"Y":8},{"X":1,"Y":8},{"X":1,"Y":9},{"X":1,"Y":10},{"X":2,"Y":10},{"X":2,"Y":9}],"Health":95,"Death":{"Cause":"head-collision","Turn":111,"EliminatedBy":"gs_Pkw9j4j3cDR9WjKrdXh8JSm3"},"Color":"#e91e63","HeadType":"beluga","TailType":"block-bum","Latency":"50","Shout":"","Team":""},{"ID":"gs_XwG4cbBb4y8kvYPRm448tB7D","Name":"k-snek","URL":"","Body":[{"X":7,"Y":3},{"X":7,"Y":4},{"X":7,"Y":5},{"X":7,"Y":6},{"X":6,"Y":6},{"X":6,"Y":5},{"X":5,"Y":5}],"Health":96,"Death":{"Cause":"head-collision","Turn":44,"EliminatedBy":"gs_Cp6H9FdXCdqh6wypV9hWYJPP"},"Color":"#49628f","HeadType":"","TailType":"","Latency":"85","Shout":"","Team":""}]}')
        self.assertEqual(logic.getMove(mock, "huntail"), ("up", logic.Mode.defend), msg=str(structures.Game(mock, "huntail")))
    
    def test_defend_left(self):
        mock = formatJson('{"Turn":10,"Food":[{"X":9,"Y":3}],"Snakes":[{"ID":"gs_SV3C4wvq37WtB6hVJmk7yVXP","Name":"nicodemmus / Lisa","URL":"","Body":[{"X":1,"Y":3},{"X":0,"Y":3},{"X":0,"Y":4}],"Health":92,"Death":{"Cause":"head-collision","Turn":8},"Color":"#00FF00","HeadType":"","TailType":"","Latency":"79","Shout":""},{"ID":"gs_rRR3dm8SYjqpVWvYyfXxvktG","Name":"benkwokcy / huntail","URL":"","Body":[{"X":6,"Y":10},{"X":7,"Y":10},{"X":8,"Y":10},{"X":9,"Y":10},{"X":9,"Y":9}],"Health":99,"Death":null,"Color":"#d897cb","HeadType":"tongue","TailType":"round-bum","Latency":"219","Shout":""},{"ID":"gs_4rJfYt76DfYSPjJkJrkfWKK9","Name":"dwbayly / The Great Sandworm of Dune","URL":"","Body":[{"X":8,"Y":6},{"X":8,"Y":5},{"X":7,"Y":5},{"X":6,"Y":5}],"Health":92,"Death":null,"Color":"FF00FF","HeadType":"","TailType":"","Latency":"192","Shout":""},{"ID":"gs_cBfmDj8fdpMwFhMmXbYhRCwd","Name":"ctrlshift7 / Xenopeltis","URL":"","Body":[{"X":5,"Y":7},{"X":6,"Y":7},{"X":6,"Y":8}],"Health":94,"Death":{"Cause":"head-collision","Turn":6},"Color":"#3399ff","HeadType":"shades","TailType":"pixel","Latency":"82","Shout":""},{"ID":"gs_CHBvjy3B4yfWfSQ8GjP4cX7P","Name":"jonanders / hack-the-snake-us","URL":"","Body":[{"X":6,"Y":8},{"X":7,"Y":8},{"X":7,"Y":7},{"X":6,"Y":7},{"X":5,"Y":7}],"Health":95,"Death":null,"Color":"#DFFF00","HeadType":"","TailType":"","Latency":"82","Shout":""},{"ID":"gs_vVH36FrWMK6MYV7F8gRcBMmK","Name":"wesleyks / SooperTrooper","URL":"","Body":[{"X":1,"Y":1},{"X":2,"Y":1},{"X":2,"Y":2}],"Health":90,"Death":{"Cause":"head-collision","Turn":10},"Color":"#e134eb","HeadType":"bendr","TailType":"bolt","Latency":"95","Shout":""},{"ID":"gs_9BJbK3RkJg7BcJ3WxfxVyhfY","Name":"jbberinger / Citrus Cobra","URL":"","Body":[{"X":1,"Y":1},{"X":1,"Y":2},{"X":1,"Y":3},{"X":2,"Y":3},{"X":3,"Y":3},{"X":3,"Y":4},{"X":3,"Y":4}],"Health":100,"Death":null,"Color":"#43E5DF","HeadType":"tongue","TailType":"pixel","Latency":"86","Shout":""}]}')
        self.assertEqual(logic.getMove(mock, "huntail"), ("left", logic.Mode.defend), msg=str(structures.Game(mock, "huntail")))
    
    def test_defend_left_2(self):
        mock = formatJson('{"Turn":117,"Food":[{"X":9,"Y":8}],"Snakes":[{"ID":"gs_m8XKrm9DQhb7Q7pS88k6Kp9M","Name":"Plissken","URL":"","Body":[{"X":8,"Y":9},{"X":7,"Y":9},{"X":6,"Y":9},{"X":5,"Y":9},{"X":4,"Y":9},{"X":3,"Y":9},{"X":2,"Y":9},{"X":1,"Y":9},{"X":0,"Y":9},{"X":0,"Y":10},{"X":1,"Y":10}],"Health":99,"Death":null,"Color":"#3dcd58","HeadType":"shades","TailType":"round-bum","Latency":"89","Shout":"","Team":""},{"ID":"gs_Y9JTyk9PyjMtrTSbKjMxwR4H","Name":"huntail","URL":"","Body":[{"X":9,"Y":6},{"X":9,"Y":5},{"X":9,"Y":4},{"X":10,"Y":4},{"X":10,"Y":3},{"X":9,"Y":3},{"X":9,"Y":2},{"X":9,"Y":1},{"X":8,"Y":1},{"X":7,"Y":1},{"X":7,"Y":2},{"X":8,"Y":2},{"X":8,"Y":3}],"Health":69,"Death":null,"Color":"#d897cb","HeadType":"tongue","TailType":"round-bum","Latency":"84","Shout":"","Team":""},{"ID":"gs_Dw4yyJ9rC3QDJC4rpRm4QPMT","Name":"naive","URL":"","Body":[{"X":7,"Y":8},{"X":6,"Y":8},{"X":5,"Y":8},{"X":5,"Y":7},{"X":5,"Y":6},{"X":5,"Y":5},{"X":4,"Y":5},{"X":3,"Y":5},{"X":2,"Y":5},{"X":2,"Y":4},{"X":2,"Y":3},{"X":2,"Y":2},{"X":2,"Y":1},{"X":2,"Y":0},{"X":3,"Y":0},{"X":3,"Y":1}],"Health":98,"Death":null,"Color":"#edb638","HeadType":"","TailType":"","Latency":"168","Shout":"","Team":""},{"ID":"gs_kKJpk4CvkPDpqhb3FFGRcf7M","Name":"Peluchito","URL":"","Body":[{"X":1,"Y":8},{"X":0,"Y":8},{"X":0,"Y":7},{"X":0,"Y":6}],"Health":77,"Death":{"Cause":"head-collision","Turn":35,"EliminatedBy":"gs_Dw4yyJ9rC3QDJC4rpRm4QPMT"},"Color":"#ccab0e","HeadType":"bendr","TailType":"freckled","Latency":"185","Shout":"","Team":""}]}')
        self.assertEqual(logic.getMove(mock, "huntail"), ("left", logic.Mode.defend), msg=str(structures.Game(mock, "huntail")))

    def test_defend_left_3(self):
        mock = formatJson('{"Turn":81,"Food":[{"X":10,"Y":0},{"X":9,"Y":3},{"X":0,"Y":9}],"Snakes":[{"ID":"gs_9KWqjgrrwydHXy8FKYjBGqS3","Name":"huntail","URL":"","Body":[{"X":7,"Y":0},{"X":7,"Y":1},{"X":6,"Y":1},{"X":5,"Y":1},{"X":4,"Y":1},{"X":3,"Y":1},{"X":3,"Y":0},{"X":4,"Y":0},{"X":5,"Y":0},{"X":6,"Y":0}],"Health":94,"Death":null,"Color":"#d897cb","HeadType":"tongue","TailType":"round-bum","Latency":"113","Shout":"","Team":""},{"ID":"gs_VWkRjvyVrkCcrXbkPcfc9cRX","Name":"Project Z","URL":"","Body":[{"X":9,"Y":2},{"X":8,"Y":2},{"X":7,"Y":2},{"X":6,"Y":2},{"X":5,"Y":2},{"X":4,"Y":2},{"X":3,"Y":2},{"X":3,"Y":3},{"X":3,"Y":4},{"X":3,"Y":5},{"X":3,"Y":6},{"X":3,"Y":7}],"Health":85,"Death":null,"Color":"#e91e63","HeadType":"beluga","TailType":"block-bum","Latency":"29","Shout":"","Team":""},{"ID":"gs_RcXP9ttSJ47Rmp8Mq6cx6Hj8","Name":"Look Ahead","URL":"","Body":[{"X":0,"Y":3},{"X":0,"Y":2},{"X":0,"Y":1},{"X":0,"Y":0},{"X":1,"Y":0},{"X":2,"Y":0},{"X":2,"Y":1},{"X":1,"Y":1},{"X":1,"Y":2},{"X":1,"Y":3},{"X":2,"Y":3},{"X":2,"Y":4}],"Health":91,"Death":null,"Color":"#64943E","HeadType":"sand-worm","TailType":"round-bum","Latency":"56","Shout":"","Team":""},{"ID":"gs_SQXD3GVfqx8d97Ymd897Q9V9","Name":"D.Va","URL":"","Body":[{"X":8,"Y":7},{"X":8,"Y":8},{"X":8,"Y":9},{"X":8,"Y":10},{"X":9,"Y":10},{"X":10,"Y":10},{"X":10,"Y":9},{"X":9,"Y":9},{"X":9,"Y":8}],"Health":85,"Death":null,"Color":"#EE4BB5","HeadType":"","TailType":"","Latency":"86","Shout":"","Team":""}]}')
        self.assertEqual(logic.getMove(mock, "huntail"), ("left", logic.Mode.defend), msg=str(structures.Game(mock, "huntail")))

    def test_left(self):
        mock = formatJson('{"Turn":87,"Food":[{"X":10,"Y":5},{"X":8,"Y":9}],"Snakes":[{"ID":"gs_7wCTdgFPvth3RmM37wq639g7","Name":"Project Z","URL":"","Body":[{"X":5,"Y":4},{"X":5,"Y":5},{"X":6,"Y":5},{"X":6,"Y":6},{"X":5,"Y":6},{"X":5,"Y":7},{"X":6,"Y":7}],"Health":92,"Death":{"Cause":"head-collision","Turn":43,"EliminatedBy":"gs_d7Fw7YH4MGjGyGrTTXVMdKRC"},"Color":"#e91e63","HeadType":"beluga","TailType":"block-bum","Latency":"33","Shout":"","Team":""},{"ID":"gs_j3YmH9q9JYWTH8d4CWrGGVrK","Name":"huntail","URL":"","Body":[{"X":3,"Y":8},{"X":3,"Y":9},{"X":3,"Y":10},{"X":4,"Y":10},{"X":4,"Y":9},{"X":4,"Y":8},{"X":4,"Y":7},{"X":5,"Y":7},{"X":5,"Y":6},{"X":5,"Y":5},{"X":6,"Y":5},{"X":7,"Y":5},{"X":8,"Y":5}],"Health":98,"Death":null,"Color":"#d897cb","HeadType":"tongue","TailType":"round-bum","Latency":"170","Shout":"","Team":""},{"ID":"gs_qxxvXrcwKrfYq6FQhhhYvQyV","Name":"Dragonborn","URL":"","Body":[{"X":2,"Y":5},{"X":1,"Y":5},{"X":1,"Y":4},{"X":1,"Y":3},{"X":1,"Y":2},{"X":2,"Y":2},{"X":3,"Y":2},{"X":3,"Y":1},{"X":4,"Y":1},{"X":4,"Y":2},{"X":4,"Y":3},{"X":4,"Y":4},{"X":4,"Y":5},{"X":4,"Y":6},{"X":3,"Y":6},{"X":3,"Y":7}],"Health":96,"Death":null,"Color":"#050352","HeadType":"fang","TailType":"curled","Latency":"72","Shout":"","Team":""},{"ID":"gs_d7Fw7YH4MGjGyGrTTXVMdKRC","Name":"Look Ahead","URL":"","Body":[{"X":10,"Y":9},{"X":10,"Y":10},{"X":10,"Y":9},{"X":10,"Y":8},{"X":10,"Y":7},{"X":10,"Y":6},{"X":9,"Y":6},{"X":9,"Y":5},{"X":9,"Y":4},{"X":8,"Y":4},{"X":8,"Y":3}],"Health":85,"Death":{"Cause":"snake-self-collision","Turn":71,"EliminatedBy":"gs_d7Fw7YH4MGjGyGrTTXVMdKRC"},"Color":"#95BF47","HeadType":"pixel","TailType":"sharp","Latency":"55","Shout":"","Team":""}]}')
        self.assertEqual(logic.getMove(mock, "huntail")[0], "left", msg=str(structures.Game(mock, "huntail")))

    def test_defend_right(self):
        mock = formatJson('{"Turn":65,"Food":[{"X":0,"Y":6},{"X":0,"Y":9}],"Snakes":[{"ID":"gs_GQQDGVxDVkyCQWK8M773wf6J","Name":"huntail","URL":"","Body":[{"X":3,"Y":10},{"X":3,"Y":9},{"X":4,"Y":9},{"X":4,"Y":8},{"X":5,"Y":8},{"X":5,"Y":7}],"Health":42,"Death":null,"Color":"#d897cb","HeadType":"tongue","TailType":"round-bum","Latency":"85","Shout":"","Team":""},{"ID":"gs_TQbwmWmyWXJJhkXYFrGB3HRH","Name":"Look Ahead","URL":"","Body":[{"X":4,"Y":7},{"X":3,"Y":7},{"X":3,"Y":6},{"X":3,"Y":5},{"X":3,"Y":4},{"X":4,"Y":4},{"X":5,"Y":4}],"Health":92,"Death":null,"Color":"#64943E","HeadType":"safe","TailType":"round-bum","Latency":"54","Shout":"","Team":""},{"ID":"gs_wdHTFVPMXx9m4VMQkyXgcYRV","Name":"sim-snakey","URL":"","Body":[{"X":2,"Y":3},{"X":2,"Y":4},{"X":1,"Y":4},{"X":1,"Y":5},{"X":0,"Y":5},{"X":0,"Y":4}],"Health":73,"Death":null,"Color":"#628f49","HeadType":"shades","TailType":"bolt","Latency":"134","Shout":"","Team":""},{"ID":"gs_DqtPQctXRjWSt3X6kWRt3ypD","Name":"Nessegrev-flood","URL":"","Body":[{"X":1,"Y":8},{"X":2,"Y":8},{"X":2,"Y":7},{"X":2,"Y":6},{"X":1,"Y":6},{"X":1,"Y":7}],"Health":69,"Death":null,"Color":"#4400ff","HeadType":"sand-worm","TailType":"sharp","Latency":"63","Shout":"","Team":""}]}')
        self.assertEqual(logic.getMove(mock, "huntail"), ("right", logic.Mode.defend), msg=str(structures.Game(mock, "huntail")))
    
    def test_defend_down(self):
        mock = formatJson('{"Turn":4,"Food":[{"X":1,"Y":1},{"X":5,"Y":9}],"Snakes":[{"ID":"gs_XT3B8mhyWjydBWXMKxT4BQrS","Name":"Snax","URL":"","Body":[{"X":8,"Y":8},{"X":8,"Y":7},{"X":9,"Y":7},{"X":9,"Y":8}],"Health":98,"Death":null,"Color":"#800080","HeadType":"tongue","TailType":"freckled","Latency":"88","Shout":"","Team":""},{"ID":"gs_D6FGf9pvc3fkfFGbr7tVXp94","Name":"huntail","URL":"","Body":[{"X":0,"Y":2},{"X":1,"Y":2},{"X":1,"Y":3}],"Health":96,"Death":null,"Color":"#d897cb","HeadType":"tongue","TailType":"round-bum","Latency":"154","Shout":"","Team":""},{"ID":"gs_FcbRGgSfGRX7C79QqSvvFGWS","Name":"Robosnake Mk. III","URL":"","Body":[{"X":6,"Y":6},{"X":7,"Y":6},{"X":7,"Y":5},{"X":8,"Y":5}],"Health":98,"Death":null,"Color":"#5D6D7E","HeadType":"bendr","TailType":"fat-rattle","Latency":"89","Shout":"","Team":""},{"ID":"gs_M74rkxRypxwVtQG3Hc6gTDfH","Name":"noob","URL":"","Body":[{"X":2,"Y":0},{"X":2,"Y":1},{"X":3,"Y":1}],"Health":96,"Death":null,"Color":"#10b3cc","HeadType":"bendr","TailType":"round-bum","Latency":"85","Shout":"","Team":""}]}')
        self.assertEqual(logic.getMove(mock, "huntail"), ("down", logic.Mode.defend), msg=str(structures.Game(mock, "huntail")))

    def test_defend_not_right(self):
        mock = formatJson('{"Turn":76,"Food":[{"X":4,"Y":5}],"Snakes":[{"ID":"gs_XJT4cMq4GGH83txHxFh8ybDC","Name":"1obo / S-1000","URL":"","Body":[{"X":10,"Y":4},{"X":10,"Y":3},{"X":9,"Y":3},{"X":8,"Y":3},{"X":7,"Y":3},{"X":6,"Y":3}],"Health":99,"Death":null,"Color":"#000000","HeadType":"tongue","TailType":"freckled","Latency":"39","Shout":""},{"ID":"gs_qB8JGSXX46x7yVJ8Xq4hXQ8R","Name":"benkwokcy / huntail","URL":"","Body":[{"X":8,"Y":6},{"X":8,"Y":7},{"X":9,"Y":7},{"X":10,"Y":7},{"X":10,"Y":8}],"Health":62,"Death":null,"Color":"#d897cb","HeadType":"tongue","TailType":"round-bum","Latency":"90","Shout":""},{"ID":"gs_WqcBpXhK97DgWW3JpfbWrtmQ","Name":"synthesizedsoul / D.Va","URL":"","Body":[{"X":3,"Y":5},{"X":3,"Y":6},{"X":4,"Y":6},{"X":4,"Y":7},{"X":4,"Y":8},{"X":3,"Y":8},{"X":2,"Y":8},{"X":2,"Y":9},{"X":3,"Y":9},{"X":3,"Y":10},{"X":2,"Y":10}],"Health":95,"Death":null,"Color":"#EE4BB5","HeadType":"","TailType":"","Latency":"116","Shout":""},{"ID":"gs_qQPjpjHtbp8h9SSVfMxVGxh8","Name":"sockbot / fearless-snake","URL":"","Body":[{"X":4,"Y":4},{"X":5,"Y":4},{"X":5,"Y":5},{"X":6,"Y":5},{"X":6,"Y":6},{"X":6,"Y":7},{"X":6,"Y":8},{"X":6,"Y":9},{"X":6,"Y":10}],"Health":91,"Death":null,"Color":"#EC86AC","HeadType":"","TailType":"","Latency":"85","Shout":""}]}')
        self.assertNotEqual(logic.getMove(mock, "huntail")[0], "right", msg=str(structures.Game(mock, "huntail")))

    def test_defend_not_down(self):
        mock = formatJson('{"Turn":108,"Food":[{"X":1,"Y":9}],"Snakes":[{"ID":"gs_6gKDf6SvGcBKFmKfFXcfxRKc","Name":"S-1000","URL":"","Body":[{"X":9,"Y":10},{"X":10,"Y":10},{"X":10,"Y":9},{"X":10,"Y":8},{"X":10,"Y":7},{"X":10,"Y":6},{"X":9,"Y":6}],"Health":96,"Death":{"Cause":"head-collision","Turn":91,"EliminatedBy":"gs_X7JpmcX3TGkbDW7yVY6qFVkb"},"Color":"#000000","HeadType":"shades","TailType":"round-bum","Latency":"17","Shout":"","Team":""},{"ID":"gs_qG3xxCXcyD8gV68SVfKMpFKb","Name":"huntail","URL":"","Body":[{"X":4,"Y":4},{"X":3,"Y":4},{"X":3,"Y":5},{"X":3,"Y":6},{"X":2,"Y":6},{"X":2,"Y":5},{"X":2,"Y":4},{"X":2,"Y":3},{"X":2,"Y":2},{"X":2,"Y":1},{"X":2,"Y":0}],"Health":96,"Death":null,"Color":"#d897cb","HeadType":"tongue","TailType":"round-bum","Latency":"89","Shout":"","Team":""},{"ID":"gs_X7JpmcX3TGkbDW7yVY6qFVkb","Name":"Dragonborn-2","URL":"","Body":[{"X":5,"Y":7},{"X":5,"Y":6},{"X":5,"Y":5},{"X":6,"Y":5},{"X":7,"Y":5},{"X":7,"Y":6},{"X":7,"Y":7},{"X":7,"Y":8},{"X":6,"Y":8},{"X":5,"Y":8},{"X":4,"Y":8},{"X":4,"Y":9},{"X":4,"Y":10},{"X":5,"Y":10},{"X":6,"Y":10},{"X":7,"Y":10},{"X":8,"Y":10},{"X":9,"Y":10}],"Health":98,"Death":null,"Color":"#050352","HeadType":"fang","TailType":"curled","Latency":"82","Shout":"","Team":""},{"ID":"gs_PFMT4kSJpqhDCkK976W6JdqB","Name":"D.Va","URL":"","Body":[{"X":3,"Y":4},{"X":4,"Y":4},{"X":4,"Y":3},{"X":3,"Y":3}],"Health":82,"Death":{"Cause":"head-collision","Turn":23,"EliminatedBy":"gs_X7JpmcX3TGkbDW7yVY6qFVkb"},"Color":"#EE4BB5","HeadType":"","TailType":"","Latency":"87","Shout":"","Team":""}]}')
        self.assertNotEqual(logic.getMove(mock, "huntail")[0], "down", msg=str(structures.Game(mock, "huntail")))

    def test_defend_not_down_2(self):
        mock = formatJson('{"Turn":83,"Food":[{"X":3,"Y":5},{"X":7,"Y":4}],"Snakes":[{"ID":"gs_xGXhGjpHHxjqkFVm6VKXD9hb","Name":"Secret Snake (Experimental)","URL":"","Body":[{"X":9,"Y":8},{"X":10,"Y":8},{"X":10,"Y":7},{"X":10,"Y":6},{"X":9,"Y":6},{"X":8,"Y":6},{"X":8,"Y":7}],"Health":99,"Death":null,"Color":"#877f63","HeadType":"smile","TailType":"regular","Latency":"42","Shout":"","Team":""},{"ID":"gs_Dm4rdh9XR3CJytxBrM3RkVRM","Name":"Medusa Returns","URL":"","Body":[{"X":5,"Y":4},{"X":4,"Y":4},{"X":4,"Y":5},{"X":5,"Y":5},{"X":5,"Y":6},{"X":5,"Y":7},{"X":4,"Y":7},{"X":3,"Y":7},{"X":3,"Y":8},{"X":2,"Y":8},{"X":2,"Y":9},{"X":2,"Y":10}],"Health":88,"Death":null,"Color":"#CFB53B","HeadType":"tongue","TailType":"curled","Latency":"98","Shout":"","Team":""},{"ID":"gs_cMgf9thqWVdxP6JmKB9CfT6G","Name":"huntail","URL":"","Body":[{"X":7,"Y":2},{"X":8,"Y":2},{"X":9,"Y":2},{"X":9,"Y":3},{"X":9,"Y":4},{"X":10,"Y":4},{"X":10,"Y":5},{"X":9,"Y":5},{"X":8,"Y":5}],"Health":94,"Death":null,"Color":"#d897cb","HeadType":"tongue","TailType":"round-bum","Latency":"112","Shout":"","Team":""},{"ID":"gs_q9cRdXvpMb79HWmJyGFF6HS6","Name":"Dragonborn-2","URL":"","Body":[{"X":3,"Y":6},{"X":2,"Y":6},{"X":2,"Y":5},{"X":1,"Y":5},{"X":1,"Y":6},{"X":0,"Y":6},{"X":0,"Y":5},{"X":0,"Y":4},{"X":0,"Y":3},{"X":0,"Y":2},{"X":0,"Y":1}],"Health":95,"Death":null,"Color":"#050352","HeadType":"fang","TailType":"curled","Latency":"80","Shout":"","Team":""}]}')
        self.assertNotEqual(logic.getMove(mock, "huntail"), ("down", logic.Mode.defend), msg=str(structures.Game(mock, "huntail")))

    def test_grow_right(self):
        mock = { "board": { "height": 11, "width": 11, "food": [{"x": 2, "y": 7}, {"x": 5, "y": 10}], "snakes": [ {"id": "huntail", "name": "huntail", "health": 90, "body": [{"x": 1, "y": 7}, {"x": 1, "y": 8}, {"x": 2, "y": 8}],}, {"id": "", "name": "testenemy", "health": 90, "body": [{"x": 0, "y": 6}, {"x": 0, "y": 5}, {"x": 1, "y": 5}]}, {"id": "", "name": "testenemy2", "health": 90, "body": [{"x": 4, "y": 2}, {"x": 3, "y": 2}, {"x": 2, "y": 2}]}, {"id": "", "name": "testenemy3", "health": 90, "body": [{"x": 8, "y": 8}, {"x": 7, "y": 8}, {"x": 7, "y": 6}, {"x": 7, "y": 5}, {"x": 7, "y": 4}, {"x": 7, "y": 3}, {"x": 7, "y": 2}, {"x": 7, "y": 1}]}, ], }, "you": {"id": "huntail", "name": "huntail", "health": 90, "body": [{"x": 1, "y": 7}, {"x": 1, "y": 8}, {"x": 2, "y": 8}],}, }
        self.assertEqual(logic.getMove(mock, "huntail"), ("right", logic.Mode.grow), msg=str(structures.Game(mock, "huntail")))

    def test_grow_right_2(self):
        mock = formatJson('{"Turn":221,"Food":[{"X":0,"Y":0},{"X":1,"Y":0},{"X":7,"Y":10},{"X":6,"Y":3}],"Snakes":[{"ID":"gs_rTBd4Cp7SjFFPWkjBp9cCCpJ","Name":"freiburgermsu / Debest","URL":"","Body":[{"X":1,"Y":-1},{"X":1,"Y":0},{"X":1,"Y":1}],"Health":90,"Death":{"Cause":"wall-collision","Turn":10},"Color":"#164910","HeadType":"","TailType":"","Latency":"0","Shout":""},{"ID":"gs_ddPVXC6Ppw8jcf7jBypVBJxM","Name":"danielrychtera / Slurms MacKenzie","URL":"","Body":[{"X":9,"Y":-1},{"X":9,"Y":0},{"X":9,"Y":1}],"Health":98,"Death":{"Cause":"wall-collision","Turn":2},"Color":"#3e1049","HeadType":"","TailType":"","Latency":"348","Shout":""},{"ID":"gs_wpQfymt9yQkWwBFx6GkRwxmF","Name":"lduchosal / tomjedusor-0.17","URL":"","Body":[{"X":1,"Y":-1},{"X":1,"Y":0},{"X":1,"Y":1}],"Health":94,"Death":{"Cause":"wall-collision","Turn":6},"Color":"#cd1e91","HeadType":"","TailType":"","Latency":"0","Shout":""},{"ID":"gs_4QHRmRbVXWPr3W7jkmdK6hM4","Name":"pushplay / Giftbit Statler","URL":"","Body":[{"X":5,"Y":2},{"X":5,"Y":3},{"X":5,"Y":4},{"X":5,"Y":5}],"Health":95,"Death":{"Cause":"snake-collision","Turn":7},"Color":"#104947","HeadType":"","TailType":"","Latency":"0","Shout":""},{"ID":"gs_fWrBTwQdJ8Jvq8yQjtb4TSP4","Name":"jbberinger / Citrus Cobra","URL":"","Body":[{"X":3,"Y":4},{"X":4,"Y":4},{"X":5,"Y":4},{"X":6,"Y":4},{"X":7,"Y":4},{"X":7,"Y":5},{"X":7,"Y":6},{"X":8,"Y":6},{"X":8,"Y":7},{"X":8,"Y":8},{"X":7,"Y":8},{"X":6,"Y":8},{"X":6,"Y":7},{"X":5,"Y":7},{"X":5,"Y":6},{"X":5,"Y":5},{"X":4,"Y":5}],"Health":70,"Death":null,"Color":"#43E5DF","HeadType":"tongue","TailType":"pixel","Latency":"76","Shout":""},{"ID":"gs_dY3RM7ShMcbfvwvM4KvGWHrc","Name":"benkwokcy / huntail","URL":"","Body":[{"X":3,"Y":6},{"X":3,"Y":7},{"X":3,"Y":8},{"X":2,"Y":8},{"X":2,"Y":7},{"X":1,"Y":7},{"X":0,"Y":7},{"X":0,"Y":6},{"X":1,"Y":6},{"X":2,"Y":6},{"X":2,"Y":5},{"X":1,"Y":5},{"X":0,"Y":5},{"X":0,"Y":4},{"X":0,"Y":3},{"X":0,"Y":2},{"X":1,"Y":2}],"Health":82,"Death":null,"Color":"#d897cb","HeadType":"tongue","TailType":"round-bum","Latency":"109","Shout":""}]}')
        self.assertEqual(logic.getMove(mock, "huntail"), ("right", logic.Mode.grow), msg=str(structures.Game(mock, "huntail")))

    def test_grow_right_3(self):
        mock = formatJson('{"Turn":109,"Food":[{"X":4,"Y":10},{"X":7,"Y":10},{"X":0,"Y":10},{"X":7,"Y":1},{"X":3,"Y":0},{"X":0,"Y":3},{"X":0,"Y":0},{"X":10,"Y":10},{"X":1,"Y":5}],"Snakes":[{"ID":"gs_gWGFyVKkQj3yPbrJWKgPwVVQ","Name":"craig95 / Logiese Swart Mamba","URL":"","Body":[{"X":5,"Y":1},{"X":5,"Y":2},{"X":5,"Y":3}],"Health":88,"Death":{"Cause":"head-collision","Turn":12},"Color":"#DFFF00","HeadType":"","TailType":"","Latency":"85","Shout":""},{"ID":"gs_8FDpYfF8Km4QjMjYdgPSDgyJ","Name":"benkwokcy / huntail","URL":"","Body":[{"X":7,"Y":6},{"X":7,"Y":7},{"X":7,"Y":8},{"X":8,"Y":8},{"X":9,"Y":8},{"X":9,"Y":9},{"X":10,"Y":9},{"X":10,"Y":8},{"X":10,"Y":7}],"Health":94,"Death":null,"Color":"#d897cb","HeadType":"tongue","TailType":"round-bum","Latency":"233","Shout":""},{"ID":"gs_jTVGS4b4ggYMBmwtCPcJwWRT","Name":"1obo / S-1000","URL":"","Body":[{"X":7,"Y":4},{"X":6,"Y":4},{"X":5,"Y":4},{"X":5,"Y":3},{"X":4,"Y":3},{"X":4,"Y":4},{"X":3,"Y":4},{"X":3,"Y":5},{"X":4,"Y":5},{"X":5,"Y":5},{"X":6,"Y":5},{"X":6,"Y":6},{"X":5,"Y":6},{"X":4,"Y":6}],"Health":96,"Death":null,"Color":"#000000","HeadType":"safe","TailType":"pixel","Latency":"75","Shout":""},{"ID":"gs_WS4PmXywQkFhWmX9jtSv3vrK","Name":"kabmichal / VOS_power","URL":"","Body":[{"X":5,"Y":-1},{"X":5,"Y":0},{"X":5,"Y":1}],"Health":90,"Death":{"Cause":"wall-collision","Turn":10},"Color":"#7f498f","HeadType":"","TailType":"","Latency":"357","Shout":""}]}')
        self.assertEqual(logic.getMove(mock, "huntail"), ("right", logic.Mode.grow), msg=str(structures.Game(mock, "huntail")))

    def test_grow_right_4(self):
        mock = formatJson('{"Turn":137,"Food":[{"X":8,"Y":10},{"X":2,"Y":10}],"Snakes":[{"ID":"gs_TMQVQvQKcfSTmqGcDpWHw9FK","Name":"hateehc99 / The first REAL destruction of all snakes","URL":"","Body":[{"X":1,"Y":-1},{"X":1,"Y":0},{"X":1,"Y":1}],"Health":98,"Death":{"Cause":"wall-collision","Turn":2},"Color":"#50DEDA","HeadType":"beluga","TailType":"round-bum","Latency":"144","Shout":""},{"ID":"gs_CDVhB3M938SbqXx9b7P4QbSJ","Name":"olivermking / Python Battlesnake","URL":"","Body":[{"X":11,"Y":1},{"X":10,"Y":1},{"X":9,"Y":1},{"X":8,"Y":1},{"X":7,"Y":1},{"X":6,"Y":1}],"Health":99,"Death":{"Cause":"wall-collision","Turn":22},"Color":"#FFE873","HeadType":"safe","TailType":"round-bum","Latency":"0","Shout":""},{"ID":"gs_kp4yDQdvm4wk34fkc3xdm69Q","Name":"benkwokcy / huntail","URL":"","Body":[{"X":1,"Y":10},{"X":0,"Y":10},{"X":0,"Y":9},{"X":0,"Y":8},{"X":0,"Y":7}],"Health":41,"Death":null,"Color":"#d897cb","HeadType":"tongue","TailType":"round-bum","Latency":"168","Shout":""},{"ID":"gs_W4RrPXc98tQCrfhbkPwFfDRF","Name":"mmilholm / Cool_as_ice","URL":"","Body":[{"X":8,"Y":9},{"X":8,"Y":8},{"X":8,"Y":7},{"X":8,"Y":6},{"X":8,"Y":5},{"X":7,"Y":5},{"X":6,"Y":5},{"X":6,"Y":4},{"X":6,"Y":3},{"X":7,"Y":3},{"X":8,"Y":3},{"X":9,"Y":3},{"X":10,"Y":3},{"X":10,"Y":4},{"X":10,"Y":5},{"X":10,"Y":6},{"X":10,"Y":7},{"X":10,"Y":8},{"X":10,"Y":9},{"X":10,"Y":10},{"X":9,"Y":10},{"X":9,"Y":9}],"Health":88,"Death":null,"Color":"#1ecdc7","HeadType":"","TailType":"","Latency":"73","Shout":""}]}')
        self.assertEqual(logic.getMove(mock, "huntail"), ("right", logic.Mode.hungry), msg=str(structures.Game(mock, "huntail")))

    def test_grow_right_5(self):
        mock = {'game': {'id': '51f6284f-ff6e-44e0-bc82-f9d1545ad5a9'}, 'turn': 72, 'board': {'height': 11, 'width': 11, 'food': [{'x': 8, 'y': 1}], 'snakes': [{'id': 'gs_JVFwBpqGd8fP9HmKmpqPDCXB', 'name': 'wanghy2007 / hwsnake', 'health': 79, 'body': [{'x': 0, 'y': 2}, {'x': 0, 'y': 3}, {'x': 0, 'y': 4}, {'x': 0, 'y': 5}, {'x': 0, 'y': 6}, {'x': 0, 'y': 7}, {'x': 0, 'y': 8}, {'x': 0, 'y': 9}, {'x': 1, 'y': 9}, {'x': 2, 'y': 9}], 'shout': ''}, {'id': 'gs_6rBwmYggDRxXhp3WcDktJS9R', 'name': 'within / Erratic', 'health': 28, 'body': [{'x': 9, 'y': 3}, {'x': 10, 'y': 3}, {'x': 10, 'y': 4}], 'shout': ''}, {'id': 'gs_FYkgCSmHhbcv6hjrrDTcqbQc', 'name': 'nanstey / CheckSnake', 'health': 54, 'body': [{'x': 1, 'y': 3}, {'x': 1, 'y': 4}, {'x': 1, 'y': 5}, {'x': 1, 'y': 6}, {'x': 2, 'y': 6}, {'x': 3, 'y': 6}], 'shout': ''}, {'id': 'gs_XGvTq4Ft7GhdRRPwqk9J4DF9', 'name': 'benkwokcy / huntail', 'health': 80, 'body': [{'x': 4, 'y': 0}, {'x': 4, 'y': 1}, {'x': 3, 'y': 1}, {'x': 3, 'y': 2}, {'x': 2, 'y': 2}], 'shout': ''}]}, 'you': {'id': 'gs_XGvTq4Ft7GhdRRPwqk9J4DF9', 'name': 'benkwokcy / huntail', 'health': 80, 'body': [{'x': 4, 'y': 0}, {'x': 4, 'y': 1}, {'x': 3, 'y': 1}, {'x': 3, 'y': 2}, {'x': 2, 'y': 2}], 'shout': ''}}
        self.assertEqual(logic.getMove(mock, "huntail"), ("right", logic.Mode.grow), msg=str(structures.Game(mock, "huntail")))

    def test_grow_right_6(self):
        mock = formatJson('{"Turn":6,"Food":[{"X":1,"Y":10},{"X":6,"Y":4},{"X":8,"Y":9}],"Snakes":[{"ID":"gs_Gyv7MYW9rG63WgtYjXQx8Kk8","Name":"rlkennedyreid / robins-second-snek","URL":"","Body":[{"X":1,"Y":2},{"X":1,"Y":3},{"X":1,"Y":4},{"X":1,"Y":5}],"Health":98,"Death":{"Cause":"snake-collision","Turn":3},"Color":"#1ecd3f","HeadType":"","TailType":"","Latency":"0","Shout":""},{"ID":"gs_WvxxWK3h7WGvVKTFgGbFJmmX","Name":"abstractalgebra / Denny","URL":"","Body":[{"X":1,"Y":3},{"X":1,"Y":4},{"X":1,"Y":5}],"Health":94,"Death":null,"Color":"#ff00ff","HeadType":"","TailType":"","Latency":"342","Shout":""},{"ID":"gs_J3qgC49xfVcBqCM8pQFQ7cDC","Name":"xylliu / dumb-snakev03","URL":"","Body":[{"X":6,"Y":8},{"X":6,"Y":7},{"X":7,"Y":7},{"X":7,"Y":8}],"Health":98,"Death":null,"Color":"#1e4fcd","HeadType":"","TailType":"","Latency":"80","Shout":""},{"ID":"gs_xbGKVtBw4CbvgydvgtS9ktk6","Name":"mocoso / SimplePython","URL":"","Body":[{"X":8,"Y":4},{"X":8,"Y":5},{"X":8,"Y":6},{"X":9,"Y":6}],"Health":98,"Death":null,"Color":"#1ecdc7","HeadType":"","TailType":"","Latency":"79","Shout":""},{"ID":"gs_kDfvvxXv89VfWKJxdWBDKqgc","Name":"jb613 / Snake1e","URL":"","Body":[{"X":9,"Y":-1},{"X":9,"Y":0},{"X":9,"Y":1}],"Health":98,"Death":{"Cause":"wall-collision","Turn":2},"Color":"#741ecd","HeadType":"","TailType":"","Latency":"93","Shout":""},{"ID":"gs_4qtCpRbd7PcbBXGyw3FqwYbQ","Name":"benkwokcy / huntail","URL":"","Body":[{"X":1,"Y":1},{"X":1,"Y":0},{"X":0,"Y":0}],"Health":94,"Death":null,"Color":"#d897cb","HeadType":"tongue","TailType":"round-bum","Latency":"101","Shout":""}]}')
        self.assertEqual(logic.getMove(mock, "huntail"), ("right", logic.Mode.grow), msg=str(structures.Game(mock, "huntail")))

    def test_grow_left(self):
        mock = formatJson('{"Turn":40,"Food":[{"X":2,"Y":2},{"X":2,"Y":9},{"X":2,"Y":7},{"X":4,"Y":3},{"X":10,"Y":0},{"X":4,"Y":8}],"Snakes":[{"ID":"gs_CJgbP8p4Fcw9SvPDQX94RVCP","Name":"vadimbrodsky / Solid SNEK","URL":"","Body":[{"X":6,"Y":2},{"X":7,"Y":2},{"X":7,"Y":3},{"X":7,"Y":4},{"X":8,"Y":4}],"Health":76,"Death":null,"Color":"#628f49","HeadType":"","TailType":"","Latency":"83","Shout":""},{"ID":"gs_4dFwRDjXHdXYVKTdMgMVFFYD","Name":"dupdup / dupdup","URL":"","Body":[{"X":1,"Y":-1},{"X":1,"Y":0},{"X":1,"Y":1},{"X":1,"Y":2}],"Health":93,"Death":{"Cause":"wall-collision","Turn":10},"Color":"#8f7f49","HeadType":"","TailType":"","Latency":"0","Shout":""},{"ID":"gs_rWbGDXVkpG8WWXBkjRXxkMwV","Name":"ttttin / TTTTin","URL":"","Body":[{"X":1,"Y":-1},{"X":1,"Y":0},{"X":1,"Y":1}],"Health":94,"Death":{"Cause":"wall-collision","Turn":6},"Color":"#491010","HeadType":"","TailType":"","Latency":"0","Shout":""},{"ID":"gs_SffRBY6GW9f7XpwgXHq3d64H","Name":"cindyunrau / worm","URL":"","Body":[{"X":5,"Y":-1},{"X":5,"Y":0},{"X":5,"Y":1}],"Health":98,"Death":{"Cause":"wall-collision","Turn":2},"Color":"#493810","HeadType":"","TailType":"","Latency":"0","Shout":""},{"ID":"gs_MFJ3XSdKcJmmfvvttTpyQj9W","Name":"declanmcintosh / Kevin","URL":"","Body":[{"X":1,"Y":-1},{"X":1,"Y":0},{"X":1,"Y":1}],"Health":98,"Death":{"Cause":"wall-collision","Turn":2},"Color":"#7f498f","HeadType":"","TailType":"","Latency":"0","Shout":""},{"ID":"gs_yTgqKdj4Ph4WkwvMpx8vXd6S","Name":"benkwokcy / huntail","URL":"","Body":[{"X":5,"Y":3},{"X":5,"Y":4},{"X":5,"Y":5},{"X":5,"Y":6},{"X":5,"Y":7}],"Health":82,"Death":null,"Color":"#d897cb","HeadType":"tongue","TailType":"round-bum","Latency":"106","Shout":""}]}')
        self.assertEqual(logic.getMove(mock, "huntail"), ("left", logic.Mode.grow), msg=str(structures.Game(mock, "huntail")))

    def test_grow_left_2(self):
        mock = formatJson('{"Turn":117,"Food":[{"X":2,"Y":6},{"X":10,"Y":1}],"Snakes":[{"ID":"gs_DxKT9DffdpJYHqH86XhCKpb7","Name":"lovedjohni / Waypple_Snake","URL":"","Body":[{"X":1,"Y":-1},{"X":1,"Y":0},{"X":1,"Y":1},{"X":1,"Y":1}],"Health":99,"Death":{"Cause":"wall-collision","Turn":2},"Color":"#cd1e91","HeadType":"","TailType":"","Latency":"0","Shout":""},{"ID":"gs_fQW46YKCttG8YFQtV69DTBcc","Name":"kylestang / Dragonborn","URL":"","Body":[{"X":7,"Y":6},{"X":7,"Y":5},{"X":7,"Y":4},{"X":7,"Y":3},{"X":7,"Y":2},{"X":7,"Y":1},{"X":6,"Y":1},{"X":5,"Y":1},{"X":5,"Y":0},{"X":6,"Y":0},{"X":7,"Y":0},{"X":8,"Y":0},{"X":8,"Y":1},{"X":8,"Y":2},{"X":8,"Y":3},{"X":8,"Y":4},{"X":8,"Y":5},{"X":9,"Y":5},{"X":9,"Y":6},{"X":9,"Y":7},{"X":9,"Y":8},{"X":9,"Y":9}],"Health":92,"Death":null,"Color":"#050352","HeadType":"fang","TailType":"curled","Latency":"79","Shout":""},{"ID":"gs_4BQ8Yf6yYjhFXGyHhw8XhKmX","Name":"jstep / Krom the Destroyer(s)","URL":"","Body":[{"X":9,"Y":-1},{"X":9,"Y":0},{"X":9,"Y":1}],"Health":90,"Death":{"Cause":"wall-collision","Turn":10},"Color":"#3e1049","HeadType":"","TailType":"","Latency":"0","Shout":""},{"ID":"gs_mBPMB3mcpGBMvJdkpdTFwdGD","Name":"rashidx / VeriGoodSnek","URL":"","Body":[{"X":5,"Y":-1},{"X":5,"Y":0},{"X":5,"Y":1}],"Health":90,"Death":{"Cause":"wall-collision","Turn":10},"Color":"#104947","HeadType":"","TailType":"","Latency":"298","Shout":""},{"ID":"gs_DJCR7ryjMQJmRvtJx3KmTk4B","Name":"idafagerlund / Python 2.0","URL":"","Body":[{"X":1,"Y":-1},{"X":1,"Y":0},{"X":1,"Y":1}],"Health":90,"Death":{"Cause":"wall-collision","Turn":10},"Color":"#164910","HeadType":"","TailType":"","Latency":"305","Shout":""},{"ID":"gs_3Cg74yJPtp9WqyB9fQVYKMKB","Name":"benkwokcy / huntail","URL":"","Body":[{"X":3,"Y":6},{"X":3,"Y":7},{"X":4,"Y":7},{"X":4,"Y":8},{"X":3,"Y":8}],"Health":50,"Death":null,"Color":"#d897cb","HeadType":"tongue","TailType":"round-bum","Latency":"149","Shout":""}]}')
        self.assertEqual(logic.getMove(mock, "huntail"), ("left", logic.Mode.grow), msg=str(structures.Game(mock, "huntail")))


    def test_grow_left_3(self):
        mock = {'game': {'id': '29bd1de8-3769-4a33-9039-c4851867d50e'}, 'turn': 49, 'board': {'height': 11, 'width': 11, 'food': [{'x': 0, 'y': 2}, {'x': 7, 'y': 1}, {'x': 4, 'y': 3}], 'snakes': [{'id': 'gs_PvrWhd7SYkkwfckh4BQt8JM3', 'name': 'joshhartmann11 / Jake The Snake', 'health': 97, 'body': [{'x': 8, 'y': 9}, {'x': 7, 'y': 9}, {'x': 7, 'y': 10}, {'x': 6, 'y': 10}, {'x': 6, 'y': 9}, {'x': 6, 'y': 8}], 'shout': ''}, {'id': 'gs_TfV9VKdxV34q6HwGTtFdbw8K', 'name': 'benkwokcy / huntail', 'health': 51, 'body': [{'x': 10, 'y': 7}, {'x': 10, 'y': 6}, {'x': 10, 'y': 5}], 'shout': ''}]}, 'you': {'id': 'gs_TfV9VKdxV34q6HwGTtFdbw8K', 'name': 'benkwokcy / huntail', 'health': 51, 'body': [{'x': 10, 'y': 7}, {'x': 10, 'y': 6}, {'x': 10, 'y': 5}], 'shout': ''}}
        self.assertEqual(logic.getMove(mock, "huntail"), ("left", logic.Mode.grow), msg=str(structures.Game(mock, "huntail")))
        
    def test_grow_left_4(self):
        mock = formatJson('{"Turn":4,"Food":[{"X":3,"Y":10},{"X":7,"Y":10},{"X":2,"Y":2},{"X":0,"Y":6},{"X":3,"Y":0},{"X":7,"Y":6}],"Snakes":[{"ID":"gs_MvjfjPM7jMXKrVjygHv9MXCd","Name":"jjrpayne / mellow mike","URL":"","Body":[{"X":9,"Y":1},{"X":9,"Y":2},{"X":9,"Y":3}],"Health":96,"Death":null,"Color":"#8f7f49","HeadType":"","TailType":"","Latency":"0","Shout":""},{"ID":"gs_9mCQ7hwK7DRPDk3VrwSDTvgV","Name":"sagargandhi33 / professor-severus-snake","URL":"","Body":[{"X":5,"Y":-1},{"X":5,"Y":0},{"X":5,"Y":1}],"Health":98,"Death":{"Cause":"wall-collision","Turn":2},"Color":"#491010","HeadType":"","TailType":"","Latency":"0","Shout":""},{"ID":"gs_bKWK96XvG9qhTp7WryYBcKfV","Name":"petah / Tail Chase","URL":"","Body":[{"X":1,"Y":1},{"X":2,"Y":1},{"X":2,"Y":0}],"Health":96,"Death":null,"Color":"#4caf50","HeadType":"pixel","TailType":"hook","Latency":"32","Shout":""},{"ID":"gs_WRH6kFYSqVKtH63CWdBJxrGK","Name":"kaichao15 / Kai","URL":"","Body":[{"X":5,"Y":5},{"X":5,"Y":6},{"X":5,"Y":7}],"Health":96,"Death":null,"Color":"#628f49","HeadType":"","TailType":"","Latency":"0","Shout":""},{"ID":"gs_cJGkRppFbY47gwwbp4RtbV8P","Name":"cmaricle / shelly","URL":"","Body":[{"X":1,"Y":5},{"X":1,"Y":6},{"X":1,"Y":7}],"Health":96,"Death":null,"Color":"#493810","HeadType":"","TailType":"","Latency":"0","Shout":""},{"ID":"gs_9T9xWTB94RDQJ6JrXwhqyXRW","Name":"benkwokcy / huntail","URL":"","Body":[{"X":8,"Y":0},{"X":9,"Y":0},{"X":10,"Y":0}],"Health":96,"Death":null,"Color":"#d897cb","HeadType":"tongue","TailType":"round-bum","Latency":"208","Shout":""}]}')
        self.assertEqual(logic.getMove(mock, "huntail"), ("left", logic.Mode.grow), msg=str(structures.Game(mock, "huntail")))

    def test_grow_up(self):
        mock = { "board": { "height": 11, "width": 11, "food": [ {"x": 1, "y": 3}, {"x": 2, "y": 5}, {"x": 2, "y": 10}, {"x": 6, "y": 8}, ], "snakes": [ { "id": "huntail", "name": "huntail", "health": 90, "body": [{"x": 0, "y": 3}, {"x": 0, "y": 4}, {"x": 0, "y": 5}], }, { "id": "", "name": "testenemy", "health": 90, "body": [{"x": 1, "y": 4}, {"x": 2, "y": 4}, {"x": 3, "y": 4}], } ], }, "you": { "id": "huntail", "name": "huntail", "health": 90, "body": [{"x": 0, "y": 3}, {"x": 0, "y": 4}, {"x": 0, "y": 5}], }, }
        self.assertEqual(logic.getMove(mock, "huntail"), ("up", logic.Mode.grow), msg=str(structures.Game(mock, "huntail")))

def formatJson(response: str) -> dict:
    """Convert the raw json response from Battlesnake Online Engine
    into a dictionary that is accepted by our Game board matrix. 

    You can grab these json responses from your browser at
    Developer Tools -> Network -> Websockets -> Messages. 

    These responses can be imported here and turned into unit tests.
    """

    def formatList(l):
        """Takes a list of dictionaries and turns the keys to lowercase."""
        return [{k.lower():v for k,v in p.items()} for p in l]

    inputDict = json.loads(response)
    outputDict = {
        "board": {"height": 11, "width": 11, "food": [], "snakes": []}
    }

    outputDict["board"]["food"] = formatList(inputDict["Food"])
    for snake in inputDict["Snakes"]:
        if snake["Death"]:
            continue
        outputDict["board"]["snakes"].append(
            {
                "id": "",
                "name": snake["Name"],
                "health": snake["Health"],
                "body": formatList(snake["Body"])
            }
        )
          
    return outputDict

if __name__ == "__main__":
    unittest.main()
