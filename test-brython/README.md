# Plotille Brython Compatibility Test

This directory contains a test page to validate that plotille can run in the browser using Brython.

## What is Brython?

Brython (Browser Python) is a Python 3 implementation for client-side web programming. It allows Python code to run directly in the browser without a backend server.

## Setup

The test environment was created with:

```bash
# Install brython as dev dependency
uv add --dev brython

# Create test directory
mkdir test-brython
cd test-brython

# Install brython files (brython.js, brython_stdlib.js)
uv run python -m brython install

# Add plotille package for browser use
uv run python -m brython add_package plotille
```

This copies the plotille source into the test-brython directory so Brython can load it.

## Test Page

The test page (`index.html`) attempts to:
1. Load Brython and its standard library
2. Import plotille's Canvas class
3. Run the house_example.py code
4. Display the output in the browser

## How to Test

1. Start an HTTP server (required for Brython to load modules):
   ```bash
   python -m http.server 8888
   ```

2. Open http://localhost:8888/test-brython/ in your browser

3. Click the "Run Example" button

4. Check if:
   - Import succeeds
   - Example runs without errors
   - Output displays correctly with braille characters

## Expected Challenges

Potential issues that may arise:
- **Module imports**: Brython's import system differs from CPython
- **Standard library compatibility**: Some stdlib modules may not work
- **Type annotations**: Modern Python syntax features may have issues
- **Unicode handling**: Braille characters need proper UTF-8 support
- **Performance**: Browser execution may be slower than CPython

## Success Criteria

For the documentation system to use interactive Brython examples, we need:
- ✓ plotille imports successfully
- ✓ Canvas operations work correctly
- ✓ Braille characters render properly
- ✓ Colors display correctly
- ✓ No critical errors or missing features
- ✓ Performance is acceptable for interactive use

## Results

✅ **Test passed successfully!**

**What works:**
- ✓ plotille imports and runs in Brython without modifications
- ✓ Canvas operations (rect, line, point, text, fill_char) work correctly
- ✓ Figure with multiple plots renders properly
- ✓ ANSI color codes are generated with `os.environ["FORCE_COLOR"] = "1"`
- ✓ AnsiUp ES6 module converts ANSI to HTML successfully
- ✓ Braille characters (U+2800 - U+28FF) display correctly in browser
- ✓ Multiple colors render properly (blue, white, red, yellow, green)
- ✓ Performance is fast enough for interactive use

**Technical details:**
- Brython must be installed with `uv run python -m brython install`
- Plotille must be added with `uv run python -m brython add_package plotille`
- AnsiUp must be loaded as ES6 module: `import { AnsiUp } from './ansi_up.js'`
- Set `os.environ["FORCE_COLOR"] = "1"` to enable ANSI output
- OutputCapture class needs `isatty()` method returning `True`

**Limitations found:**
- None significant for documentation use case
- All plotille features tested work correctly

## Conclusion

**Brython is viable for interactive plotille documentation!**

The documentation system can safely implement:
- Interactive code editors for examples without external dependencies
- Real-time execution in the browser
- Colored terminal output rendering
- No backend server needed for interactive examples

Examples requiring numpy/PIL/etc. will still use static pre-rendering,
but pure plotille examples can be fully interactive.
