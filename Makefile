.PHONY: style tests install

fmt:
	poetry run ruff format .
	poetry run ruff check --fix .

style:
	poetry run ruff format --check .
	poetry run ruff check .
	poetry run mypy ./plotille
	bunx pyright ./plotille

tests:
	poetry run pytest -s -vvv

install:
	poetry install
