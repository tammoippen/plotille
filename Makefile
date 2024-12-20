.PHONY: style tests install

fmt:
	poetry run ruff format .
	poetry run ruff check --fix .

style:
	poetry run ruff format --check .
	poetry run ruff check .

tests:
	poetry run pytest -s -vvv

install:
	poetry install
