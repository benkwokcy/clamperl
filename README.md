# huntail

A snake AI for Battlesnake 2020. Based off the Python starter snake, which uses the bottle web framework to serve requests and the gunicorn web server for running bottle on Heroku.

## How to Run

Running locally:

```bash
python server.py
```

Deploying to Heroku:

```bash
git push heroku master
heroku open
heroku logs --tail # view server logs
```
