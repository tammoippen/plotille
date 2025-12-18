.PHONY: style tests install

fmt:
	uv run --locked ruff format .
	uv run --locked ruff check --fix .

check:
	uv run --locked ruff format --check .
	uv run --locked ruff check .

typing:
	uv run --locked mypy ./plotille
	uv run --locked ty check ./plotille

tests:
	uv run --locked pytest -s -vvv

install:
	uv install
