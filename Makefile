.PHONY: style tests install docs docs-serve

fmt:
	uv run --locked ruff format .
	uv run --locked ruff check --fix .

check:
	uv run --locked ruff format --check .
	uv run --locked ruff check .

typing:
	uv run --locked mypy ./plotille
	# uv run --locked ty check ./plotille

tests:
	uv run --locked pytest -s -vvv

install:
	uv install

docs:
	uv run python scripts/generate_docs.py

docs-serve: docs
	uv run mkdocs serve --dev-addr 127.0.0.1:8000
