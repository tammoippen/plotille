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

docs-copy-plotille:
	@echo "Copy plotille to docs folder"
	@rm -rf docs/Lib
	@mkdir -p docs/Lib/site-packages/plotille
	@cp plotille/*.py docs/Lib/site-packages/plotille/

docs-brython:
	@echo "Installing Brython runtime..."
	@rm -f docs/brython.js docs/brython_stdlib.js docs/unicode.txt docs/demo.html docs/README.txt docs/index.html
	@echo "Y" | uv run brython-cli install --install-dir docs
	@rm -f docs/demo.html docs/README.txt docs/index.html
	@echo "✓ Brython installed to docs/"

docs/ansi_up.js:
	@echo "Downloading AnsiUp library..."
	@curl -sL -o docs/ansi_up.js https://unpkg.com/ansi_up@6.0.2/ansi_up.js
	@echo "✓ AnsiUp downloaded to docs/"

docs: docs-copy-plotille docs/ansi_up.js docs-brython
	uv run python docs/generate_docs.py

docs-serve: docs
	uv run mkdocs serve --dev-addr 127.0.0.1:8000
