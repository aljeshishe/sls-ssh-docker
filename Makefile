SHELL := /bin/bash

.PHONY: build
build:
	docker build -t serverless-sls-ssh-docker-dev:appimage .

.PHONY: docker
docker:
	docker run -it --entrypoint bash serverless-sls-ssh-docker-dev:appimage

.PHONY: deploy
deploy:
	serverless  deploy --force --verbose

.PHONY: run
run:
	sls invoke --function handler

%:      # thanks to chakrit
	@:    # thanks to William Pursell

.PHONY: client
client:
	python client.py $(filter-out $@,$(MAKECMDGOALS))

.PHONY: logs
logs:
	sls logs --function handler -t
