import pprint
import unittest

from app import logic, structures
from testing import mocks

def printBoard(mock):

    def _symbol(state):
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
        strings.append("[" + "|".join([_symbol(state) for state in row]) + "]")

    return "\n".join(strings)

class TestGetMove(unittest.TestCase):

    def test_avoid_wall_down(self):
        self.assertEqual(logic.getMove(mocks.moveDown), ("down", logic.Mode.defend))

    def test_avoid_wall_up(self):
        self.assertEqual(logic.getMove(mocks.moveUp), ("up", logic.Mode.defend))

    def test_avoid_wall_left(self):
        self.assertEqual(logic.getMove(mocks.moveLeft), ("left", logic.Mode.defend))

    def test_avoid_wall_right(self):
        self.assertEqual(logic.getMove(mocks.moveRight), ("right", logic.Mode.defend))

    def test_eat_down(self):
        self.assertEqual(logic.getMove(mocks.eatDown), ("down", logic.Mode.eat))

    def test_eat_up(self):
        self.assertEqual(logic.getMove(mocks.eatUp), ("up", logic.Mode.eat))

    def test_avoid_trap_right(self):
        self.assertEqual(logic.getMove(mocks.moveRightToOpenArea), ("right", logic.Mode.defend))

    def test_avoid_enemy_up(self):
        self.assertEqual(logic.getMove(mocks.avoidEnemyMoveUp), ("up", logic.Mode.defend))

    def test_avoid_enemy_right(self):
        self.assertEqual(logic.getMove(mocks.avoidEnemyMoveRight), ("right", logic.Mode.defend))

    def test_avoid_enemy_right2(self):
        self.assertEqual(logic.getMove(mocks.avoidEnemyMoveRight2), ("right", logic.Mode.defend), msg=printBoard(mocks.avoidEnemyMoveRight2))

if __name__ == "__main__":
    unittest.main()
