# huntail

A snake AI for Battlesnake 2020.

## About

Logic Overview:

- If the snake is hungry, it will eat. Otherwise, it moves around defensively.
  - If the snake is really hungry, it will take more risks to get food.
  - If the snake isn't that hungry, it might act defensively until it's easier to reach food.
- The snake likes to stay in a large open area.
- The snake prefers safer moves over riskier moves.

Structures Overview:

- Game information is stored in the Game object.
- Each square on the Game board has a State.
- Each state has a number (the risk number) that tells us how dangerous it is.
- These risk scores incentivize the snake to take certain moves/paths.

## File Structure

- server.py - launch web server
- tests.py - run unit tests
- /app
  - logic.py - higher level logic configuring how my snake behaves
  - structures.py - data structures simulating the game state
- app.json - tell Heroku descriptive details about the app
- Procfile - tells Heroku the entry point for the app
- requirements.txt - tells Heroku what dependencies to install when deploying
- runtime.txt - tells Heroku which Python version to use

## Instructions

Running locally:

```bash
python3 server.py
```

Running tests:

```bash
python3 test.py
```

Deploying to Heroku:

```bash
git push heroku
```

## To Do

- Look at more future possibilities and parallelize
- Generalize data structures so I can look up the best move for any snake, not just myself
- Watch more games and add tests
