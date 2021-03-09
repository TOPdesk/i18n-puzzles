FROM python:3.8-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY templates /usr/src/app/templates/
COPY main.py /usr/src/app/

EXPOSE 8080

CMD [ "python", "main.py" ]