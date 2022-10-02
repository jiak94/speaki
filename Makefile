BOLD := \033[1m
RESET := \033[0m

default: help

.PHONY : help
help:  ## Shows this help
	@echo "$(BOLD)WMS Adapter Makefile$(RESET)"
	@echo "Please use 'make $(BOLD)target$(RESET)' where $(BOLD)target$(RESET) is one of:"
	@grep -h ':\s\+##' Makefile | column -tn -s# | awk -F ":" '{ print "  $(BOLD)" $$1 "$(RESET)" $$2 }'

.PHONY: lint
lint:  ## Runs all linters (check-isort, check-black, flake8)
lint: check-isort check-black flake8

.PHONY: check checks
check / checks:  ## Runs all checkers (lint, tests)
check: checks
checks: lint tests check-commit

.PHONY: check-isort
check-isort:  ## Runs the isort tool in check mode only (won't modify files)
	@echo "$(BOLD)Checking isort(RESET)"
	@isort . --check-only 2>&1

.PHONY: check-black
check-black:  ## Runs the black tool in check mode only (won't modify files)
	@echo "$(BOLD)Checking black$(RESET)"
	@black --target-version py310 --check  . 2>&1

.PHONY: flake8
flake8:  ## Runs the flake8 tool
	@echo "$(BOLD)Running flake8$(RESET)"
	@flake8 --format=abspath

.PHONY: pretty
pretty:  ## Runs all code beautifiers (isort, black)
pretty: isort black

.PHONY: isort
isort:  ## Runs the isort tool and updates files that need to
	@echo "$(BOLD)Running isort$(RESET)"
	@isort . --atomic

.PHONY: black
black:  ## Runs the black tool and updates files that need to
	@echo "$(BOLD)Running black$(RESET)"
	@black --target-version py310 .

.PHONY: setup
setup:  ## Runs the setup.py tool
	@echo "$(BOLD)Running setup$(RESET)"
	@cp templates/env .env

.PHONY: build
build: ## Builds Docker images
	@echo "$(BOLD)Building Docker images$(RESET)"
	@COMMIT=$(shell git rev-parse HEAD) docker-compose build

.PHONY: run
run: ## Runs Docker images
	@echo "$(BOLD)Running Docker images$(RESET)"
	@COMMIT=$(shell git rev-parse HEAD) docker-compose up -d

.PHONY: down
down:  ## Stops a development environment
	@echo "$(BOLD)Stopping development environment$(RESET)"
	@-docker-compose down

.PHONY: tests
tests:  ## Runs all tests
	@echo "$(BOLD)Running tests$(RESET)"
	@poetry run pytest --cov=./ --cov-report=xml

.PHONY: clean
clean:  ## Cleans a development environment
	@docker-compose down -v
