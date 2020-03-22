# huntail-python

#### NOTE: This version is obsolete, see the rewrite in Java at https://github.com/benkwokcy/huntail

A snake AI for Battlesnake 2020, using Python 3.7, Bottle, and Heroku. The snake runs on one thread in a Heroku hobby dyno. It calculates at most one move into the future, the rest is heuristic-based.

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
