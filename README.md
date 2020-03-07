# huntail

A snake AI for Battlesnake 2020.

## About

### Overview:

- If the snake is hungry or smaller than its opponents, it will eat. Otherwise, it moves around defensively.
  - If the snake is really hungry, it will take more risks to get food.
  - If the food is hard to reach and the snake isn't starving, it can postpone eating until a better time.
- The snake likes to stay in a large open area, especially areas
- The snake prefers safer moves over riskier moves.

### Features:

- Heuristics:
  - Size of connected areas. Size is found using UnionFind and DFS/Flood Fill.
  - Risk score assigned to each square. Score scheme are manually adjusted to incentivize certain moves.

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