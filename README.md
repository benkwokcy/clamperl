# huntail

A snake AI for Battlesnake 2020.

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

- Snake is doing different things in arena than in my unit tests
  - Moves are not deterministic because of the random shuffling
- Look further in the future.
  - Use multiprocessing to parallelize
- Generalize data structures so I can look up the best move for any snake, not just myself
