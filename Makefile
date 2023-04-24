SHELL := /bin/bash

# make "$(filter-out $@,$(MAKECMDGOALS))" work
%:
	@:


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

.PHONY: client
client:
	python client.py $(filter-out $@,$(MAKECMDGOALS))

.PHONY: waitlogs
waitlogs:
	sls logs --function handler -t

.PHONY: logs
logs:
	sls logs --function handler
