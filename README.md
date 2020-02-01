# huntail

A snake AI for Battlesnake 2020. Based off the Python starter snake.

## Structure

- /app
  - server.py - uses the bottle web framework to serve requests and the gunicorn web server to run bottle on Heroku.
  - logic.py - logic for calculating moves
  - structures.py - data structures for calculating moves
- app.json - tell Heroku some random details
- Procfile - tells Heroku how to run the app
- requirements.txt - tells Heroku what dependencies to install
- runtime.txt - tells Heroku which Python to use
- README.md - this markdown file :)

## How to Run

Running locally:

```bash
python app/server.py
```

Deploying to Heroku:

```bash
git push heroku master
```

## Issues

1. "from app import logic" vs "import logic". The first way works on Heroku but not locally. The second way works locally but not on Heroku.
