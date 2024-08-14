FROM python:3.12-slim

WORKDIR /usr/src/app

COPY site/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY site/templates /usr/src/app/templates/
COPY site/static /usr/src/app/static/
COPY site/auth.py site/main.py /usr/src/app/
COPY puzzles /usr/src/puzzles

# To make sure answers.json exists. It's not included in the repo
COPY puzzles/answers.json /usr/src/puzzles/

VOLUME /srv/code-challenge

ENV DATABASE_URL sqlite:////srv/code-challenge/scores.sqlite
ENV PUZZLE_PATH=/usr/src/puzzles

EXPOSE 8080

CMD [ "python", "main.py" ]
