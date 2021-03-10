Python with Flask and Jinja frontend for code challenge.

To run in dev mode:
```
$ FLASK_APP=main.py FLASK_ENV=development flask run --port 5000
```

To run in prod mode (port 8080):
```
$ python main.py
```

Docker deployment to https://hub.docker.com/orgs/topdesk/repositories:
```
$ docker build -t topdesk/betabanenmarkt-coding-challenge .
$ docker push topdesk/betabanenmarkt-coding-challenge
```