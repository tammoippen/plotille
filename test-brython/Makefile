.PHONY: setup clean serve test

# Setup the Brython test environment
setup: brython.js Lib/site-packages/plotille ansi_up.js
	@echo "✓ Setup complete!"
	@echo ""
	@echo "To test:"
	@echo "  make serve"
	@echo "  Open http://localhost:8888/test-brython/"

# Install Brython runtime files
brython.js:
	@echo "Installing Brython runtime..."
	uv run python -m brython install

# Copy plotille source (without dependencies)
Lib/site-packages/plotille: ../plotille/*.py
	@echo "Copying plotille source..."
	@rm -rf Lib/site-packages/plotille
	@mkdir -p Lib/site-packages
	@cp -r ../plotille Lib/site-packages/

# Download AnsiUp library
ansi_up.js:
	@echo "Downloading AnsiUp library..."
	curl -L -o ansi_up.js https://unpkg.com/ansi_up@6.0.2/ansi_up.js

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	rm -rf brython.js brython_stdlib.js unicode.txt README.txt demo.html Lib/ ansi_up.js
	@echo "✓ Clean complete"

# Start local web server
serve:
	@echo "Starting web server on http://localhost:8888/test-brython/"
	python -m http.server 8888

# Alias for setup
test: setup
