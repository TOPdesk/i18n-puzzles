#!/bin/bash

IMAGE=amarillion/i18n-challenges
VERSION=1.2.0

docker build -t ${IMAGE}:${VERSION} .
docker tag ${IMAGE}:${VERSION} ${IMAGE}

docker stop i18n-challenges
docker rm i18n-challenges
docker run \
	-p 5000:8080 \
	-v /srv/code-challenge:/srv/code-challenge \
	-d \
	--restart always \
	--name i18n-challenges \
	amarillion/i18n-challenges

