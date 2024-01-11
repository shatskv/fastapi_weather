include .env
export $(shell sed 's/=.*//' .env)
run:
	poetry run python3 weather/server.py
.PHONY: tests
tests:
	poetry run pytest
