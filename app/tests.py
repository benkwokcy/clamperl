import mocks, logic

def avoid_wall_down():
    assert logic.getMove(mocks.moveDown) == "down"

def avoid_wall_up():
    assert logic.getMove(mocks.moveUp) == "up"

def avoid_wall_left():
    assert logic.getMove(mocks.moveLeft) == "left"

def avoid_wall_right():
    assert logic.getMove(mocks.moveRight) == "right"