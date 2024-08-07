# About this repository

This repo contains Internationalization puzzles used for a workshop on internationalization and localization at TOPdesk.
 
This site is hosted at https://i18n-puzzles.com

# Developer info

## Local Development

Python with Flask and Jinja frontend for code challenge.

Originally developed by Martin Tichem for the Beta Banenmarkt. 
Amended by Martijn van Iersel to make it suitable for the internationalization puzzles (i18n-puzzles.com)

Set PUZZLE_PATH to the path where the puzzles can be found.

To run in dev mode:
```
$ PUZZLE_PATH=puzzles FLASK_APP=site/main.py FLASK_DEBUG=true flask run --port 5000
```

## Production mode

To run in prod mode (port 8080):
```
$ python main.py
```

Docker deployment to https://hub.docker.com/orgs/topdesk/repositories:
```
$ docker build -t topdesk/betabanenmarkt-coding-challenge .
$ docker push topdesk/betabanenmarkt-coding-challenge
```