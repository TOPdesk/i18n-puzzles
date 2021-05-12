#!/bin/bash

make build
docker stop i18n-challenges
docker rm i18n-challenges
docker run \
	-p 8080:8080 \
	-v /srv/code-challenge:/srv/code-challenge \
	-d \
	--restart always \
	--name i18n-challenges \
	amarillion/i18n-challenges

