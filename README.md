# huntail

A snake AI for Battlesnake 2020. Based off the Python starter snake, which uses the bottle web framework to serve requests and the gunicorn web server for running bottle on Heroku.

## Running Locally

1. Start the server.

```bash
python server.py
```

2. Send requests to localhost:8080.

## Deploying to Heroku

1) Create a new Heroku app:

```
heroku create [APP_NAME]
```

2) Deploy code to Heroku servers:

```
git push heroku master
```

3) Open Heroku app in browser:

```
heroku open
```

or visit [http://APP_NAME.herokuapp.com](http://APP_NAME.herokuapp.com).

4) View server logs with the `heroku logs` command:

```
heroku logs --tail
```