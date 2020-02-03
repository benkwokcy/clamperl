moveRight = {
    "board": {"height": 1, "width": 2, "food": [], "snakes": []},
    "you": {"id": "", "name": "testsnake", "health": 90, "body": [{"x": 0, "y": 0}]},
}

moveLeft = {
    "board": {"height": 1, "width": 2, "food": [], "snakes": []},
    "you": {"id": "", "name": "testsnake", "health": 90, "body": [{"x": 1, "y": 0}]},
}

moveDown = {
    "board": {"height": 2, "width": 1, "food": [], "snakes": []},
    "you": {"id": "", "name": "testsnake", "health": 90, "body": [{"x": 0, "y": 0}]},
}

moveUp = {
    "board": {"height": 2, "width": 1, "food": [], "snakes": []},
    "you": {"id": "", "name": "testsnake", "health": 90, "body": [{"x": 0, "y": 1}]},
}

eatUp = {
    "board": {"height": 3, "width": 1, "food": [{"x": 0, "y": 0}], "snakes": []},
    "you": {"id": "", "name": "testsnake", "health": 40, "body": [{"x": 0, "y": 1}]},
}

eatDown = {
    "board": {"height": 3, "width": 1, "food": [{"x": 0, "y": 2}], "snakes": []},
    "you": {"id": "", "name": "testsnake", "health": 40, "body": [{"x": 0, "y": 1}]},
}

moveRightToOpenArea = {
    "board": {"height": 11, "width": 11, "food": [], "snakes": []},
    "you": {
        "id": "",
        "name": "testsnake",
        "health": 60,
        "body": [
            {"x": 4, "y": 0},
            {"x": 4, "y": 1},
            {"x": 4, "y": 2},
            {"x": 4, "y": 3},
            {"x": 3, "y": 3},
            {"x": 3, "y": 4},
            {"x": 2, "y": 4},
            {"x": 2, "y": 3},
            {"x": 1, "y": 3},
            {"x": 1, "y": 4},
            {"x": 0, "y": 4},
            {"x": 0, "y": 3},
            {"x": 0, "y": 2},
            {"x": 0, "y": 1},
            {"x": 0, "y": 0},
            {"x": 1, "y": 0},
            {"x": 1, "y": 1},
        ],
    },
}

avoidEnemyMoveUp = {
    "board": {
        "height": 11,
        "width": 11,
        "food": [
            {"x": 1, "y": 3},
            {"x": 2, "y": 5},
            {"x": 2, "y": 10},
            {"x": 6, "y": 8},
        ],
        "snakes": [
            {
                "id": "",
                "name": "testenemy",
                "health": 90,
                "body": [{"x": 1, "y": 4}, {"x": 2, "y": 4}, {"x": 3, "y": 4}],
            }
        ],
    },
    "you": {
        "id": "",
        "name": "testsnake",
        "health": 90,
        "body": [{"x": 0, "y": 3}, {"x": 0, "y": 4}, {"x": 0, "y": 5}],
    },
}

avoidEnemyMoveRight = {
    "board": {
        "height": 3,
        "width": 3,
        "food": [],
        "snakes": [
            {"id": "", "name": "testenemy", "health": 90, "body": [{"x": 0, "y": 0}]},
            {"id": "", "name": "testenemy2", "health": 90, "body": [{"x": 0, "y": 1}]}
        ],
    },
    "you": {"id": "", "name": "testsnake", "health": 90, "body": [{"x": 1, "y": 0}]},
}

avoidEnemyMoveRight2 = {
    "board": {
        "height": 11,
        "width": 11,
        "food": [
            {"x": 2, "y": 7},
            {"x": 5, "y": 10},
        ],
        "snakes": [
            {
                "id": "",
                "name": "testenemy",
                "health": 90,
                "body": [{"x": 0, "y": 6}, {"x": 0, "y": 5}, {"x": 1, "y": 5}],
            },
            {
                "id": "",
                "name": "testenemy2",
                "health": 90,
                "body": [{"x": 4, "y": 2}, {"x": 3, "y": 2}, {"x": 2, "y": 2}],
            },
            {
                "id": "",
                "name": "testenemy3",
                "health": 90,
                "body": [{"x": 8, "y": 8}, {"x": 7, "y": 8}, {"x": 7, "y": 6}, {"x": 7, "y": 5}, {"x": 7, "y": 4}, {"x": 7, "y": 3}, {"x": 7, "y": 2}, {"x": 7, "y": 1}],
            },
        ],
    },
    "you": {
        "id": "",
        "name": "testsnake",
        "health": 90,
        "body": [{"x": 1, "y": 7}, {"x": 1, "y": 8}, {"x": 2, "y": 8}],
    },
}
