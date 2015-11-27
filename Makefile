REQUIREMENTS_INSTALLED := $(CURDIR)/.installed
DOCKER_IMG = ejn

.PHONY: requirements build bootstrap run stop destroy shell

all: run


$(REQUIREMENTS_INSTALLED): requirements.txt
	@echo "Installing python-requirements..."
	pip install -U -r requirements.txt | grep --line-buffered -v '^   '

	@touch $@


requirements: $(REQUIREMENTS_INSTALLED)


build:
	@docker-compose build --pull $(DOCKER_IMG)


bootstrap: requirements build


run:
	@docker-compose run --rm --service-ports $(DOCKER_IMG)


stop:
	@docker-compose stop


destroy: stop
	@docker-compose rm -f


shell:
	@docker-compose run --rm --service-ports $(DOCKER_IMG) /bin/bash
