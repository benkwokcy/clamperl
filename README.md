# huntail-python

A snake AI server for Battlesnake 2020, using Python 3.7, Bottle, and Heroku. 

This is a greedy eater snake which calculates at most one move into the future. It takes the shortest path to the nearest food, assuming that food satisfies certain risk conditions. These conditions include the expected risk of the next two moves in that direction, the distance of other snakes to that food, the size of the connected area, and whether this area contains a snake tail. If no food is satisfactory, it will take the safest defensive move. It also has the ability to trap and kill smaller snakes venture against the sides of the arena. This version was peaking at rank 18 out of 160 snakes on the online arena just prior to the event cancellation. As Python has become too much of a performance limit, I've a complete rewrite into Java (see huntail-java).

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
