# huntail

A snake AI for Battlesnake 2020.

## About

This snake has a passive middle-of-the-road playstyle. It will eat just enough to keep up in size with other snakes, otherwise it will usually chase its tail. It tries to avoid other snakes but will act more boldly if it is starving. Hopefully, we can make up for this lack of strategy with good execution.

The snake runs on one thread in a Heroku hobby dyno. It relies on heuristics rather than by enumerating future states. It only explicitly computes states that are one move into the future. One nice thing is it's been very easy to adjust the snake's tactics by tweaking the weighting of its heuristics. However, I'm noticing more and more losses which could be solved with more future sight. I've made some primitive attempts at parallization and will try to look into this more.

My main workflow is to watch arena games where the snake loses, find the board state where it went wrong, think about what move I would have made, turn that board state into a test case, and tweak the heuristics until it passes. If you want to change the snake's strategy and tests start failing, feel free to change the tests so they adhere to the strategy you have in mind!

## File Structure

- server.py - launch web server
- tests.py - run tests
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
