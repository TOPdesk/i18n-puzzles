
IMAGE=amarillion/i18n-challenges
VERSION=1.0.0

build:
	docker build -t ${IMAGE}:${VERSION} .
	docker tag ${IMAGE}:${VERSION} ${IMAGE}

push:
	docker login
	docker push ${IMAGE}
