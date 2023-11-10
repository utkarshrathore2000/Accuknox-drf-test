BLACK ?= \033[0;30m
RED ?= \033[0;31m
GREEN ?= \033[0;32m
YELLOW ?= \033[0;33m
BLUE ?= \033[0;34m
PURPLE ?= \033[0;35m
CYAN ?= \033[0;36m
GRAY ?= \033[0;37m
WHITE ?= \033[1;37m
COFF ?= \033[0m

.PHONY: all shell build  migrate quality setup superuser runserver makemigrations lint-django lint-django-fix format

all: help

help:
	@echo -e "\n$(WHITE)Available commands:$(COFF)"
	@echo -e "$(CYAN)make setup$(COFF)            - Sets up the project in your local machine."
	@echo -e "                        This includes building Docker containers and running migrations."
	@echo -e "$(CYAN)make runserver$(COFF)        - Runs the django app in the container, available at http://127.0.0.1:8000"
	@echo -e "$(CYAN)make migrate$(COFF)          - Runs django's migrate command in the container"
	@echo -e "$(CYAN)make makemigrations$(COFF)   - Runs django's makemigrations command in the container"
	@echo -e "$(CYAN)make superuser$(COFF)        - Runs django's createsuperuser command in the container"
	@echo -e "$(CYAN)make shell$(COFF)            - Starts a Linux shell (bash) in the django container"


shell:
	@echo -e "$(CYAN)Starting Bash in the django container:$(COFF)"
	@docker-compose run --rm django bash

build:
	@echo -e "$(CYAN)Creating Docker images:$(COFF)"
	@docker-compose build

makemigrations:
	@echo -e "$(CYAN)Running django makemigrations:$(COFF)"
	@docker-compose run --rm django ./manage.py makemigrations $(cmd)

migrate:
	@echo -e "$(CYAN)Running django migrations:$(COFF)"
	@docker-compose run --rm django ./manage.py migrate $(cmd)
	
runserver:
	@echo -e "$(CYAN)Starting Docker container with the app.$(COFF)"
	@docker-compose up
	@echo -e "$(CYAN)App ready and listening at http://127.0.0.1:8000.$(COFF)"

runserver-d:
	@echo -e "$(CYAN)Starting Docker container with the app.$(COFF)"
	@docker-compose up --build -d
	@echo -e "$(CYAN)App ready and listening at http://127.0.0.1:8000.$(COFF)"


down:
	@docker-compose down

down-v:
	@docker-compose down --volume

test:
	@echo -e "$(CYAN)Run test cases:$(COFF)"
	@docker-compose run --rm django ./manage.py test $(cmd)