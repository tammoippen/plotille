.PHONY: style tests

style:
	poetry run flake8 tests/ plotille/ examples/

tests:
	poetry run pytest -s -vvv
