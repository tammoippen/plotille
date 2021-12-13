.PHONY: style tests

style:
	poetry run flake8 tests/ plotille/ examples/

tests:
	poetry run pytest -s -vvv

install:
	poetry install
	poetry run pip install -r tests/requirements.txt
