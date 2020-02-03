from app import logic
from testing import mocks

import unittest

class TestGetMove(unittest.TestCase):

    def test_avoid_wall_down(self):
        assert logic.getMove(mocks.moveDown) == "down"

    def test_avoid_wall_up(self):
        assert logic.getMove(mocks.moveUp) == "up"

    def test_avoid_wall_left(self):
        assert logic.getMove(mocks.moveLeft) == "left"

    def test_avoid_wall_right(self):
        assert logic.getMove(mocks.moveRight) == "right"

    def test_eat_down(self):
        assert logic.getMove(mocks.eatDown) == "down"

    def test_eat_up(self):
        assert logic.getMove(mocks.eatUp) == "up"

    def test_avoid_trap_right(self):
        assert logic.getMove(mocks.moveRightToOpenArea) == "right", logic.getMove(mocks.moveRightToOpenArea)

    def test_avoid_enemy_right(self):
        assert logic.getMove(mocks.avoidEnemyMoveRight) == "right"

if __name__ == "__main__":
    unittest.main()
