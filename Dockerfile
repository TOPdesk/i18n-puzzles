FROM python:3.8-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY templates /usr/src/app/templates/
COPY main.py /usr/src/app/
COPY i18n-challenges /usr/src/i18n-challenges

VOLUME /srv/code-challenge

ENV DATABASE_URL sqlite:////srv/code-challenge/scores.sqlite
ENV PUZZLE_PATH=/usr/src/i18n-challenges

EXPOSE 8080

CMD [ "python", "main.py" ]