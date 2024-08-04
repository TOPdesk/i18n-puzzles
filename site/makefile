
IMAGE=amarillion/i18n-challenges
VERSION=1.2.0

build:
	docker build -t ${IMAGE}:${VERSION} .
	docker tag ${IMAGE}:${VERSION} ${IMAGE}

push:
	docker login
	docker push ${IMAGE}
