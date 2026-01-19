.PHONY: style tests install docs docs-setup docs-serve

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

docs-setup:
	@echo "Installing Brython runtime..."
	@rm -f docs/brython.js docs/brython_stdlib.js docs/unicode.txt docs/demo.html docs/README.txt docs/index.html
	@cd docs && echo "Y" | uv run python -m brython install
	@rm -f docs/demo.html docs/README.txt docs/index.html
	@echo "✓ Brython installed to docs/"

docs: docs-setup
	uv run python scripts/generate_docs.py

docs-serve: docs
	uv run mkdocs serve --dev-addr 127.0.0.1:8000
