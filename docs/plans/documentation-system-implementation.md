# Plotille Documentation System - Implementation Plan

## Overview

This plan implements a comprehensive documentation system for plotille with:
- Example-driven structure (cookbook first, API reference second)
- Interactive browser-based examples using Brython
- Amber phosphor CRT terminal aesthetic
- Auto-deployment to plotille.tammo.io via GitHub Pages
- Strict doctest enforcement

**Key Principles:**
- TDD: Write tests before implementation
- YAGNI: Only build what's specified, no extras
- DRY: Extract common patterns
- Frequent commits: After each completed task

## Prerequisites

You'll be working with:
- **MkDocs**: Static site generator for Python projects
- **mkdocstrings**: Auto-generates API docs from docstrings
- **Brython**: Browser-based Python runtime
- **CodeMirror 6**: Code editor component
- **GitHub Actions**: CI/CD pipeline

## Phase 1: Project Setup & Dependencies

### Task 1.1: Install MkDocs and Core Plugins

**What:** Set up MkDocs with necessary plugins.

**Files to modify:**
- `pyproject.toml`

**Actions:**

1. Add documentation dependencies to `[dependency-groups]` section in `pyproject.toml`:

```toml
[dependency-groups]
dev = [
  # ... existing dev dependencies ...
  "mkdocs>=1.5.0",
  "mkdocs-material>=9.5.0",
  "mkdocstrings[python]>=0.24.0",
  "mkdocs-gen-files>=0.5.0",
  "mkdocs-literate-nav>=0.6.0",
]
```

2. Install dependencies:
```bash
pip install -e ".[dev]"
```

**Test:**
```bash
mkdocs --version  # Should output version info
python -c "import mkdocstrings; print('OK')"  # Should print OK
```

**Commit:** `Add MkDocs and documentation dependencies`

---

### Task 1.2: Create Basic MkDocs Configuration

**What:** Set up minimal MkDocs config to verify installation works.

**Files to create:**
- `mkdocs.yml`

**Actions:**

1. Create `mkdocs.yml` in project root:

```yaml
site_name: plotille
site_url: https://plotille.tammo.io
site_description: Plot in the terminal using braille dots
site_author: Tammo Ippen
repo_url: https://github.com/tammoippen/plotille
repo_name: tammoippen/plotille

theme:
  name: material
  palette:
    scheme: default
  features:
    - content.code.copy
    - navigation.sections

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          options:
            docstring_style: google
            show_source: true
            show_root_heading: true
            show_root_full_path: false
            show_signature_annotations: true
            separate_signature: true

markdown_extensions:
  - pymdownx.highlight
  - pymdownx.superfences
  - pymdownx.tabbed

nav:
  - Home: index.md
```

2. Create minimal `docs/` directory:
```bash
mkdir -p docs
```

3. Create placeholder `docs/index.md`:

```markdown
# plotille

Terminal plotting with braille dots.

Documentation coming soon.
```

**Test:**
```bash
mkdocs serve  # Should start dev server on http://127.0.0.1:8000
# Open in browser, verify page loads
```

**Commit:** `Add basic MkDocs configuration`

---

### Task 1.3: Add Doctest to Test Suite

**What:** Configure pytest to run doctests on all modules.

**Files to modify:**
- `pyproject.toml`

**Actions:**

1. Update pytest configuration in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = "--cov=plotille --cov-branch --cov-report term-missing --cov-report xml --cov-report html:cov_html --doctest-modules --doctest-continue-on-failure"
testpaths = ["tests", "plotille"]
```

**Test:**
```bash
pytest --doctest-modules plotille/
# Should run (may have 0 doctests initially, that's OK)
```

**Commit:** `Enable doctest in pytest configuration`

---

## Phase 2: Example Analysis & Classification System

### Task 2.1: Create Example Parser Script

**What:** Build a script that analyzes example files to classify them as interactive vs. static.

**Files to create:**
- `scripts/generate_docs.py`

**Actions:**

1. Create `scripts/` directory:
```bash
mkdir -p scripts
```

2. Create `scripts/generate_docs.py`:

```python
#!/usr/bin/env python3
"""
Generate documentation from examples.

This script:
1. Scans examples/ directory
2. Classifies examples by dependencies
3. Generates markdown files for MkDocs
"""
import ast
import sys
from pathlib import Path
from typing import NamedTuple


class ExampleInfo(NamedTuple):
    """Information about an example file."""
    path: Path
    name: str
    description: str
    imports: set[str]
    is_interactive: bool


def extract_imports(source_code: str) -> set[str]:
    """
    Extract all imported module names from Python source.

    Args:
        source_code: Python source code as string

    Returns:
        Set of top-level module names imported

    >>> extract_imports("import numpy\\nfrom PIL import Image")
    {'numpy', 'PIL'}
    >>> extract_imports("import plotille\\nfrom plotille import Canvas")
    {'plotille'}
    """
    try:
        tree = ast.parse(source_code)
    except SyntaxError:
        return set()

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                # Get top-level module name
                imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split('.')[0])

    return imports


def extract_description(source_code: str) -> str:
    """
    Extract description from module docstring or initial comments.

    Args:
        source_code: Python source code

    Returns:
        Description string or empty string

    >>> extract_description('\"\"\"Test module\"\"\"\\nprint("hi")')
    'Test module'
    >>> extract_description('# A comment\\nprint("hi")')
    'A comment'
    """
    try:
        tree = ast.parse(source_code)
        docstring = ast.get_docstring(tree)
        if docstring:
            return docstring.strip().split('\n')[0]  # First line only
    except SyntaxError:
        pass

    # Fall back to first comment
    lines = source_code.split('\n')
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('#'):
            return stripped[1:].strip()

    return ""


def is_interactive(imports: set[str]) -> bool:
    """
    Determine if example can run in Brython (no external deps).

    Args:
        imports: Set of imported module names

    Returns:
        True if example is Brython-compatible

    >>> is_interactive({'plotille', 'math', 'random'})
    True
    >>> is_interactive({'plotille', 'numpy'})
    False
    >>> is_interactive({'PIL', 'plotille'})
    False
    """
    # These are NOT available in Brython
    blocked_modules = {'numpy', 'PIL', 'pandas', 'matplotlib', 'scipy'}

    # Check if any blocked modules are used
    return not bool(imports & blocked_modules)


def analyze_example(example_path: Path) -> ExampleInfo:
    """
    Analyze a single example file.

    Args:
        example_path: Path to example .py file

    Returns:
        ExampleInfo with analysis results
    """
    source_code = example_path.read_text()
    imports = extract_imports(source_code)
    description = extract_description(source_code)
    name = example_path.stem

    return ExampleInfo(
        path=example_path,
        name=name,
        description=description or f"Example: {name}",
        imports=imports,
        is_interactive=is_interactive(imports)
    )


def main() -> int:
    """Main entry point for testing."""
    # Find examples directory
    project_root = Path(__file__).parent.parent
    examples_dir = project_root / "examples"

    if not examples_dir.exists():
        print(f"Error: {examples_dir} not found", file=sys.stderr)
        return 1

    # Analyze all Python files
    examples = []
    for example_file in sorted(examples_dir.glob("*.py")):
        info = analyze_example(example_file)
        examples.append(info)

    # Print summary
    print(f"Found {len(examples)} examples")
    print(f"Interactive: {sum(1 for e in examples if e.is_interactive)}")
    print(f"Static: {sum(1 for e in examples if not e.is_interactive)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
```

**Test:**

1. Create a simple test file `tests/test_generate_docs.py`:

```python
"""Tests for documentation generation script."""
import sys
from pathlib import Path

# Add scripts to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import generate_docs


def test_extract_imports_simple():
    """Test extracting imports from simple code."""
    code = "import numpy\nimport plotille"
    imports = generate_docs.extract_imports(code)
    assert imports == {'numpy', 'plotille'}


def test_extract_imports_from():
    """Test extracting from-imports."""
    code = "from PIL import Image"
    imports = generate_docs.extract_imports(code)
    assert imports == {'PIL'}


def test_extract_description_docstring():
    """Test extracting description from docstring."""
    code = '"""This is a test"""\nprint("hi")'
    desc = generate_docs.extract_description(code)
    assert desc == "This is a test"


def test_extract_description_comment():
    """Test extracting description from comment."""
    code = "# This is a comment\nprint('hi')"
    desc = generate_docs.extract_description(code)
    assert desc == "This is a comment"


def test_is_interactive_pure():
    """Test interactive detection for pure plotille."""
    imports = {'plotille', 'math', 'random'}
    assert generate_docs.is_interactive(imports) is True


def test_is_interactive_numpy():
    """Test interactive detection with numpy."""
    imports = {'plotille', 'numpy'}
    assert generate_docs.is_interactive(imports) is False


def test_is_interactive_pillow():
    """Test interactive detection with PIL."""
    imports = {'PIL', 'plotille'}
    assert generate_docs.is_interactive(imports) is False
```

2. Run tests:
```bash
pytest tests/test_generate_docs.py -v
# All tests should pass
```

3. Test script manually:
```bash
python scripts/generate_docs.py
# Should print summary of examples found
```

**Commit:** `Add example analysis script with tests`

---

### Task 2.2: Add Example Categorization Logic

**What:** Extend the script to categorize examples into logical groups.

**Files to modify:**
- `scripts/generate_docs.py`

**Actions:**

1. Add categorization logic to `scripts/generate_docs.py`:

```python
# Add after ExampleInfo class definition

def categorize_example(info: ExampleInfo) -> str:
    """
    Categorize example into a section.

    Args:
        info: ExampleInfo to categorize

    Returns:
        Category name: 'basic', 'figures', 'canvas', or 'advanced'

    >>> from pathlib import Path
    >>> info = ExampleInfo(Path("scatter.py"), "scatter", "", {'plotille'}, True)
    >>> categorize_example(info)
    'basic'
    >>> info = ExampleInfo(Path("img.py"), "img", "", {'PIL', 'plotille'}, False)
    >>> categorize_example(info)
    'advanced'
    """
    name_lower = info.name.lower()

    # Canvas examples
    if 'canvas' in name_lower or 'draw' in name_lower:
        return 'canvas'

    # Figure examples (multi-plot)
    if 'figure' in name_lower or 'subplot' in name_lower:
        return 'figures'

    # Advanced (external deps or complex)
    if not info.is_interactive or 'image' in name_lower or 'img' in name_lower:
        return 'advanced'

    # Default to basic
    return 'basic'


# Add test for categorization in main()
def main() -> int:
    """Main entry point for testing."""
    project_root = Path(__file__).parent.parent
    examples_dir = project_root / "examples"

    if not examples_dir.exists():
        print(f"Error: {examples_dir} not found", file=sys.stderr)
        return 1

    # Analyze all Python files
    examples = []
    for example_file in sorted(examples_dir.glob("*.py")):
        info = analyze_example(example_file)
        examples.append(info)

    # Categorize
    categories: dict[str, list[ExampleInfo]] = {}
    for info in examples:
        category = categorize_example(info)
        categories.setdefault(category, []).append(info)

    # Print summary
    print(f"Found {len(examples)} examples")
    for category, items in sorted(categories.items()):
        interactive_count = sum(1 for e in items if e.is_interactive)
        print(f"  {category}: {len(items)} examples ({interactive_count} interactive)")

    return 0
```

**Test:**

1. Add test to `tests/test_generate_docs.py`:

```python
def test_categorize_basic():
    """Test basic example categorization."""
    from pathlib import Path
    info = generate_docs.ExampleInfo(
        Path("scatter.py"), "scatter", "", {'plotille'}, True
    )
    assert generate_docs.categorize_example(info) == 'basic'


def test_categorize_canvas():
    """Test canvas example categorization."""
    from pathlib import Path
    info = generate_docs.ExampleInfo(
        Path("canvas_test.py"), "canvas_test", "", {'plotille'}, True
    )
    assert generate_docs.categorize_example(info) == 'canvas'


def test_categorize_advanced():
    """Test advanced example categorization."""
    from pathlib import Path
    info = generate_docs.ExampleInfo(
        Path("image.py"), "image", "", {'PIL', 'plotille'}, False
    )
    assert generate_docs.categorize_example(info) == 'advanced'
```

2. Run tests:
```bash
pytest tests/test_generate_docs.py -v
python scripts/generate_docs.py
# Should show categorized summary
```

**Commit:** `Add example categorization logic`

---

## Phase 3: Static Example Pre-rendering

### Task 3.1: Implement Example Execution and Output Capture

**What:** Add ability to execute examples and capture their terminal output.

**Files to modify:**
- `scripts/generate_docs.py`

**Actions:**

1. Add execution logic to `scripts/generate_docs.py`:

```python
# Add imports at top
import subprocess
import shutil
from dataclasses import dataclass

# Add after ExampleInfo


@dataclass
class ExampleOutput:
    """Captured output from running an example."""
    stdout: str
    stderr: str
    returncode: int
    success: bool


def execute_example(example_path: Path, timeout: int = 30) -> ExampleOutput:
    """
    Execute an example and capture its output.

    Args:
        example_path: Path to example Python file
        timeout: Maximum execution time in seconds

    Returns:
        ExampleOutput with captured stdout/stderr
    """
    try:
        result = subprocess.run(
            [sys.executable, str(example_path)],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=example_path.parent,
        )

        return ExampleOutput(
            stdout=result.stdout,
            stderr=result.stderr,
            returncode=result.returncode,
            success=result.returncode == 0,
        )
    except subprocess.TimeoutExpired:
        return ExampleOutput(
            stdout="",
            stderr=f"Example timed out after {timeout} seconds",
            returncode=-1,
            success=False,
        )
    except Exception as e:
        return ExampleOutput(
            stdout="",
            stderr=f"Error executing example: {e}",
            returncode=-1,
            success=False,
        )


def save_example_output(
    info: ExampleInfo,
    output: ExampleOutput,
    output_dir: Path,
) -> Path:
    """
    Save example output to a file.

    Args:
        info: ExampleInfo for the example
        output: ExampleOutput to save
        output_dir: Directory to save output files

    Returns:
        Path to saved output file
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{info.name}.txt"

    content = output.stdout
    if not output.success and output.stderr:
        content += f"\n\nErrors:\n{output.stderr}"

    output_file.write_text(content)
    return output_file
```

**Test:**

1. Add test to `tests/test_generate_docs.py`:

```python
def test_execute_example(tmp_path):
    """Test executing a simple example."""
    # Create a simple test example
    test_example = tmp_path / "test.py"
    test_example.write_text('print("Hello from example")')

    output = generate_docs.execute_example(test_example)

    assert output.success is True
    assert output.returncode == 0
    assert "Hello from example" in output.stdout


def test_execute_example_error(tmp_path):
    """Test executing an example that fails."""
    test_example = tmp_path / "test.py"
    test_example.write_text('raise ValueError("test error")')

    output = generate_docs.execute_example(test_example)

    assert output.success is False
    assert output.returncode != 0
    assert "ValueError" in output.stderr


def test_save_example_output(tmp_path):
    """Test saving example output."""
    from pathlib import Path

    info = generate_docs.ExampleInfo(
        Path("test.py"), "test", "desc", set(), True
    )
    output = generate_docs.ExampleOutput(
        stdout="test output", stderr="", returncode=0, success=True
    )

    output_dir = tmp_path / "outputs"
    saved_path = generate_docs.save_example_output(info, output, output_dir)

    assert saved_path.exists()
    assert saved_path.read_text() == "test output"
```

2. Run tests:
```bash
pytest tests/test_generate_docs.py::test_execute_example -v
pytest tests/test_generate_docs.py::test_save_example_output -v
```

**Commit:** `Add example execution and output capture`

---

### Task 3.2: Generate Pre-rendered Output for Static Examples

**What:** Execute all static examples during doc generation and save outputs.

**Files to modify:**
- `scripts/generate_docs.py`

**Actions:**

1. Add generation function to `scripts/generate_docs.py`:

```python
def generate_static_outputs(
    examples: list[ExampleInfo],
    output_dir: Path,
) -> dict[str, Path]:
    """
    Execute static examples and save their outputs.

    Args:
        examples: List of ExampleInfo to process
        output_dir: Directory to save outputs

    Returns:
        Dict mapping example name to output file path
    """
    outputs = {}

    static_examples = [e for e in examples if not e.is_interactive]

    print(f"\nGenerating outputs for {len(static_examples)} static examples...")

    for info in static_examples:
        print(f"  Executing {info.name}...", end=" ")

        output = execute_example(info.path)

        if output.success:
            output_path = save_example_output(info, output, output_dir)
            outputs[info.name] = output_path
            print("✓")
        else:
            print(f"✗ (failed)")
            if output.stderr:
                print(f"    Error: {output.stderr[:100]}")

    return outputs


# Update main() to call this function
def main() -> int:
    """Main entry point."""
    project_root = Path(__file__).parent.parent
    examples_dir = project_root / "examples"
    output_dir = project_root / "docs" / "assets" / "example-outputs"

    if not examples_dir.exists():
        print(f"Error: {examples_dir} not found", file=sys.stderr)
        return 1

    # Analyze all Python files
    examples = []
    for example_file in sorted(examples_dir.glob("*.py")):
        info = analyze_example(example_file)
        examples.append(info)

    # Categorize
    categories: dict[str, list[ExampleInfo]] = {}
    for info in examples:
        category = categorize_example(info)
        categories.setdefault(category, []).append(info)

    # Print summary
    print(f"Found {len(examples)} examples")
    for category, items in sorted(categories.items()):
        interactive_count = sum(1 for e in items if e.is_interactive)
        print(f"  {category}: {len(items)} examples ({interactive_count} interactive)")

    # Generate static outputs
    outputs = generate_static_outputs(examples, output_dir)
    print(f"\nGenerated {len(outputs)} static outputs")

    return 0
```

**Test:**

Run the script manually to verify it executes examples:

```bash
python scripts/generate_docs.py
# Should execute static examples and save outputs to docs/assets/example-outputs/
ls docs/assets/example-outputs/
# Verify output files were created
```

**Commit:** `Add static example pre-rendering`

---

## Phase 4: Markdown Generation for Examples

### Task 4.1: Create Markdown Templates

**What:** Build templates for rendering examples as markdown.

**Files to modify:**
- `scripts/generate_docs.py`

**Actions:**

1. Add template functions to `scripts/generate_docs.py`:

```python
def generate_interactive_example_markdown(info: ExampleInfo) -> str:
    """
    Generate markdown for an interactive example.

    Args:
        info: ExampleInfo for the example

    Returns:
        Markdown string with interactive code editor
    """
    source_code = info.path.read_text()

    # Escape backticks in code for markdown
    escaped_code = source_code.replace('```', '\\`\\`\\`')

    return f"""## {info.name}

{info.description}

<div class="terminal-window interactive-example" data-example="{info.name}">
    <div class="terminal-header">
        <span class="terminal-title">[python3 {info.name}.py]</span>
        <button class="terminal-run-btn" onclick="runExample('{info.name}')">[EXEC]</button>
    </div>
    <div class="terminal-body">
        <div class="code-editor-wrapper">
            <textarea class="code-editor" id="editor-{info.name}">{escaped_code}</textarea>
        </div>
        <div class="terminal-output" id="output-{info.name}">
            <span class="terminal-prompt">root@plotille:~$ python3 {info.name}.py</span>
            <div class="output-content"></div>
        </div>
    </div>
</div>

"""


def generate_static_example_markdown(
    info: ExampleInfo,
    output_path: Path,
) -> str:
    """
    Generate markdown for a static example with pre-rendered output.

    Args:
        info: ExampleInfo for the example
        output_path: Path to pre-rendered output file

    Returns:
        Markdown string with code and output
    """
    source_code = info.path.read_text()

    # Read pre-rendered output
    if output_path.exists():
        output = output_path.read_text()
    else:
        output = "Output not available"

    deps = ', '.join(sorted(info.imports - {'plotille'}))

    return f"""## {info.name}

{info.description}

!!! info "External Dependencies"
    This example requires: **{deps}**

    Output is pre-rendered below. To run interactively, install dependencies locally.

**Code:**

```python
{source_code}
```

**Output:**

<div class="terminal-window static-example">
    <div class="terminal-header">
        <span class="terminal-title">[output: {info.name}.py]</span>
    </div>
    <div class="terminal-body">
        <pre class="terminal-output">{output}</pre>
    </div>
</div>

"""
```

**Test:**

1. Add test to `tests/test_generate_docs.py`:

```python
def test_generate_interactive_example_markdown():
    """Test generating markdown for interactive example."""
    from pathlib import Path

    info = generate_docs.ExampleInfo(
        path=Path("test.py"),
        name="test",
        description="Test example",
        imports={'plotille'},
        is_interactive=True,
    )

    # Mock the file reading
    import unittest.mock as mock
    with mock.patch.object(Path, 'read_text', return_value='print("hi")'):
        markdown = generate_docs.generate_interactive_example_markdown(info)

    assert '## test' in markdown
    assert 'Test example' in markdown
    assert 'interactive-example' in markdown
    assert 'print("hi")' in markdown


def test_generate_static_example_markdown(tmp_path):
    """Test generating markdown for static example."""
    from pathlib import Path

    info = generate_docs.ExampleInfo(
        path=Path("test.py"),
        name="test",
        description="Test example",
        imports={'plotille', 'numpy'},
        is_interactive=False,
    )

    # Create mock output file
    output_path = tmp_path / "test.txt"
    output_path.write_text("Example output here")

    import unittest.mock as mock
    with mock.patch.object(Path, 'read_text', return_value='print("hi")'):
        markdown = generate_docs.generate_static_example_markdown(info, output_path)

    assert '## test' in markdown
    assert 'Test example' in markdown
    assert 'numpy' in markdown
    assert 'Example output here' in markdown
```

2. Run tests:
```bash
pytest tests/test_generate_docs.py::test_generate_interactive_example_markdown -v
pytest tests/test_generate_docs.py::test_generate_static_example_markdown -v
```

**Commit:** `Add markdown generation templates for examples`

---

### Task 4.2: Generate Category Pages

**What:** Create markdown files for each category of examples.

**Files to modify:**
- `scripts/generate_docs.py`

**Actions:**

1. Add page generation to `scripts/generate_docs.py`:

```python
def generate_category_page(
    category: str,
    examples: list[ExampleInfo],
    output_paths: dict[str, Path],
    docs_dir: Path,
) -> Path:
    """
    Generate a markdown page for a category of examples.

    Args:
        category: Category name
        examples: List of examples in this category
        output_paths: Dict of pre-rendered output paths
        docs_dir: Documentation directory

    Returns:
        Path to generated markdown file
    """
    category_titles = {
        'basic': 'Basic Plots',
        'figures': 'Complex Figures',
        'canvas': 'Canvas Drawing',
        'advanced': 'Advanced Examples',
    }

    title = category_titles.get(category, category.title())

    # Build page content
    content = [f"# {title}\n"]

    # Add description
    descriptions = {
        'basic': 'Simple plotting examples to get started with plotille.',
        'figures': 'Multi-plot figures and complex visualizations.',
        'canvas': 'Direct canvas manipulation for custom drawings.',
        'advanced': 'Examples using external libraries like NumPy and Pillow.',
    }

    if category in descriptions:
        content.append(f"{descriptions[category]}\n")

    # Add each example
    for info in examples:
        if info.is_interactive:
            markdown = generate_interactive_example_markdown(info)
        else:
            output_path = output_paths.get(info.name, Path())
            markdown = generate_static_example_markdown(info, output_path)

        content.append(markdown)

    # Write file
    category_dir = docs_dir / "cookbook"
    category_dir.mkdir(parents=True, exist_ok=True)

    output_file = category_dir / f"{category}.md"
    output_file.write_text('\n'.join(content))

    return output_file


# Update main() to generate pages
def main() -> int:
    """Main entry point."""
    project_root = Path(__file__).parent.parent
    examples_dir = project_root / "examples"
    output_dir = project_root / "docs" / "assets" / "example-outputs"
    docs_dir = project_root / "docs"

    if not examples_dir.exists():
        print(f"Error: {examples_dir} not found", file=sys.stderr)
        return 1

    # Analyze all Python files
    examples = []
    for example_file in sorted(examples_dir.glob("*.py")):
        info = analyze_example(example_file)
        examples.append(info)

    # Categorize
    categories: dict[str, list[ExampleInfo]] = {}
    for info in examples:
        category = categorize_example(info)
        categories.setdefault(category, []).append(info)

    # Print summary
    print(f"Found {len(examples)} examples")
    for category, items in sorted(categories.items()):
        interactive_count = sum(1 for e in items if e.is_interactive)
        print(f"  {category}: {len(items)} examples ({interactive_count} interactive)")

    # Generate static outputs
    output_paths = generate_static_outputs(examples, output_dir)
    print(f"\nGenerated {len(output_paths)} static outputs")

    # Generate category pages
    print("\nGenerating category pages...")
    for category, items in sorted(categories.items()):
        page_path = generate_category_page(category, items, output_paths, docs_dir)
        print(f"  {category}: {page_path}")

    print("\n✓ Documentation generation complete")
    return 0
```

**Test:**

```bash
python scripts/generate_docs.py
# Should generate markdown files in docs/cookbook/
ls docs/cookbook/
# Verify .md files exist: basic.md, figures.md, canvas.md, advanced.md
```

**Commit:** `Add category page generation`

---

### Task 4.3: Generate Home Page

**What:** Create the hero home page with animated introduction.

**Files to create:**
- `docs/index.md`

**Actions:**

1. Update `scripts/generate_docs.py` to generate home page:

```python
def generate_home_page(docs_dir: Path) -> Path:
    """
    Generate the home/index page.

    Args:
        docs_dir: Documentation directory

    Returns:
        Path to generated index.md
    """
    content = """# plotille

<div class="hero-terminal">
    <div class="terminal-header">
        <span class="terminal-title">[root@plotille ~]$</span>
    </div>
    <div class="terminal-body">
        <pre class="hero-plot" id="hero-animation"></pre>
    </div>
</div>

Plot in the terminal using braille dots, with no dependencies.

## Features

- **Scatter plots, line plots, histograms** - Basic plotting functions
- **Complex figures** - Compose multiple plots with legends
- **Canvas drawing** - Direct pixel manipulation for custom visualizations
- **Image rendering** - Display images using braille dots or background colors
- **Color support** - Multiple color modes: names, byte values, RGB
- **No dependencies** - Pure Python with no external requirements

## Quick Start

Install plotille:

```bash
pip install plotille
```

Create your first plot:

```python
import plotille
import math

X = [i/10 for i in range(-30, 30)]
Y = [math.sin(x) for x in X]

print(plotille.plot(X, Y, height=20, width=60))
```

## Explore

Browse the [cookbook](cookbook/basic.md) to see interactive examples you can edit and run in your browser.

"""

    index_file = docs_dir / "index.md"
    index_file.write_text(content)
    return index_file


# Add to main()
def main() -> int:
    """Main entry point."""
    # ... existing code ...

    # Generate category pages
    print("\nGenerating category pages...")
    for category, items in sorted(categories.items()):
        page_path = generate_category_page(category, items, output_paths, docs_dir)
        print(f"  {category}: {page_path}")

    # Generate home page
    print("\nGenerating home page...")
    index_path = generate_home_page(docs_dir)
    print(f"  index: {index_path}")

    print("\n✓ Documentation generation complete")
    return 0
```

**Test:**

```bash
python scripts/generate_docs.py
# Verify docs/index.md was created
cat docs/index.md
# Should show hero content
```

**Commit:** `Add home page generation`

---

## Phase 5: Amber Phosphor Theme

### Task 5.1: Create Custom CSS for Terminal Aesthetic

**What:** Build CSS for the amber phosphor CRT theme.

**Files to create:**
- `docs/stylesheets/terminal.css`

**Actions:**

1. Create directory:
```bash
mkdir -p docs/stylesheets
```

2. Create `docs/stylesheets/terminal.css`:

```css
/*
 * Plotille Documentation Theme
 * Amber Phosphor CRT Terminal Aesthetic
 */

/* Import retro terminal fonts */
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=VT323&display=swap');

:root {
    /* Amber phosphor color palette */
    --amber-black: #0a0a0a;
    --amber-dark: #1a1200;
    --amber-dim: #cc8800;
    --amber-base: #ffb000;
    --amber-bright: #ffd000;
    --amber-glow: rgba(255, 176, 0, 0.4);

    /* Spacing */
    --terminal-padding: 1rem;
    --terminal-border: 2px;
}

/* Global overrides for Material theme */
[data-md-color-scheme="plotille"] {
    --md-primary-fg-color: var(--amber-base);
    --md-primary-fg-color--light: var(--amber-bright);
    --md-primary-fg-color--dark: var(--amber-dim);
    --md-accent-fg-color: var(--amber-bright);

    --md-default-bg-color: var(--amber-black);
    --md-default-fg-color: var(--amber-base);
    --md-code-bg-color: var(--amber-dark);
    --md-code-fg-color: var(--amber-base);
}

/* Typography */
body {
    font-family: 'IBM Plex Mono', monospace;
    background: var(--amber-black);
    color: var(--amber-base);
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'VT323', monospace;
    color: var(--amber-bright);
    text-shadow: 0 0 8px var(--amber-glow);
    letter-spacing: 0.05em;
}

/* CRT scanline effect */
body::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(
        transparent 50%,
        rgba(0, 0, 0, 0.1) 50%
    );
    background-size: 100% 4px;
    pointer-events: none;
    z-index: 9999;
    animation: scanline 8s linear infinite;
}

@keyframes scanline {
    0% {
        transform: translateY(0);
    }
    100% {
        transform: translateY(4px);
    }
}

/* Phosphor glow on text */
.md-content {
    text-shadow: 0 0 2px var(--amber-glow);
}

/* Terminal window styling */
.terminal-window {
    background: var(--amber-black);
    border: var(--terminal-border) solid var(--amber-dim);
    border-radius: 4px;
    margin: 1.5rem 0;
    box-shadow: 0 0 20px var(--amber-glow);
    overflow: hidden;
}

.terminal-header {
    background: var(--amber-dark);
    padding: 0.5rem var(--terminal-padding);
    border-bottom: 1px solid var(--amber-dim);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.terminal-title {
    font-family: 'IBM Plex Mono', monospace;
    color: var(--amber-base);
    font-size: 0.9rem;
}

.terminal-run-btn {
    font-family: 'VT323', monospace;
    background: var(--amber-dim);
    color: var(--amber-black);
    border: 1px solid var(--amber-base);
    padding: 0.25rem 0.75rem;
    cursor: pointer;
    font-size: 1rem;
    transition: all 0.2s;
}

.terminal-run-btn:hover {
    background: var(--amber-base);
    box-shadow: 0 0 10px var(--amber-glow);
}

.terminal-body {
    padding: var(--terminal-padding);
    background: var(--amber-black);
}

.terminal-output {
    font-family: 'IBM Plex Mono', monospace;
    color: var(--amber-base);
    white-space: pre;
    margin-top: 1rem;
    line-height: 1.4;
}

.terminal-prompt {
    color: var(--amber-bright);
    display: block;
    margin-bottom: 0.5rem;
}

.terminal-prompt::after {
    content: '';
    display: inline-block;
    width: 8px;
    height: 14px;
    background: var(--amber-base);
    margin-left: 4px;
    animation: blink 1s step-end infinite;
}

@keyframes blink {
    50% {
        opacity: 0;
    }
}

/* Code editor styling */
.code-editor-wrapper {
    border: 1px solid var(--amber-dim);
    border-radius: 2px;
}

.code-editor {
    font-family: 'IBM Plex Mono', monospace;
    background: var(--amber-dark);
    color: var(--amber-base);
    width: 100%;
    min-height: 300px;
    padding: 1rem;
    border: none;
    resize: vertical;
}

/* Static example output */
.static-example .terminal-output {
    max-height: 600px;
    overflow-y: auto;
}

/* Hero terminal animation */
.hero-terminal {
    margin: 2rem 0;
    font-size: 0.8rem;
}

.hero-plot {
    min-height: 300px;
    margin: 0;
}

/* Braille dot decorations */
.braille-divider {
    text-align: center;
    color: var(--amber-dim);
    font-size: 1.5rem;
    margin: 2rem 0;
    opacity: 0.3;
}

/* Navigation styled as terminal prompt */
.md-sidebar--primary {
    background: var(--amber-black);
}

.md-nav__link {
    font-family: 'IBM Plex Mono', monospace;
    color: var(--amber-base);
}

.md-nav__link--active {
    color: var(--amber-bright);
}

.md-nav__link::before {
    content: '> ';
    color: var(--amber-dim);
    opacity: 0;
    transition: opacity 0.2s;
}

.md-nav__link--active::before,
.md-nav__link:hover::before {
    opacity: 1;
}

/* Code blocks */
.highlight {
    background: var(--amber-dark) !important;
    border: 1px solid var(--amber-dim);
}

.highlight pre {
    color: var(--amber-base);
}

/* Admonitions (info boxes) */
.admonition {
    background: var(--amber-dark);
    border-left: 4px solid var(--amber-base);
    color: var(--amber-base);
}
```

**Test:**

1. Update `mkdocs.yml` to use custom CSS:

```yaml
theme:
  name: material
  palette:
    scheme: plotille
  custom_dir: docs/overrides
  features:
    - content.code.copy
    - navigation.sections

extra_css:
  - stylesheets/terminal.css
```

2. Test the site:
```bash
mkdocs serve
# Open browser to http://127.0.0.1:8000
# Verify amber color scheme appears
```

**Commit:** `Add amber phosphor terminal theme CSS`

---

### Task 5.2: Add Terminal Font Files (Optional Fallback)

**What:** Optionally bundle fonts locally for offline use.

**Files to create:**
- `docs/stylesheets/fonts.css` (if bundling fonts)

**Actions:**

This task is optional. If you want to bundle fonts locally instead of using Google Fonts CDN:

1. Download IBM Plex Mono and VT323 font files
2. Place in `docs/fonts/` directory
3. Update CSS `@font-face` declarations
4. Update import in `terminal.css`

For now, **skip this task** and rely on Google Fonts CDN for simplicity (YAGNI).

**Commit:** (Skip)

---

## Phase 6: Brython Integration

### Task 6.1: Add Brython Runtime and Setup

**What:** Include Brython library and initialize runtime.

**Files to create:**
- `docs/javascripts/brython-setup.js`

**Actions:**

1. Create directory:
```bash
mkdir -p docs/javascripts
```

2. Create `docs/javascripts/brython-setup.js`:

```javascript
/**
 * Brython setup and initialization for plotille documentation.
 */

// Initialize Brython when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Check if Brython is loaded
    if (typeof brython === 'undefined') {
        console.error('Brython not loaded');
        return;
    }

    // Initialize Brython
    brython({
        debug: 1,  // Show errors in console
        pythonpath: ['/src/lib']
    });

    console.log('Brython initialized');
});

/**
 * Execute Python code in an example.
 *
 * @param {string} exampleName - Name of the example to run
 */
function runExample(exampleName) {
    const editor = document.getElementById(`editor-${exampleName}`);
    const outputDiv = document.querySelector(`#output-${exampleName} .output-content`);

    if (!editor || !outputDiv) {
        console.error(`Example ${exampleName} not found`);
        return;
    }

    const code = editor.value;

    // Clear previous output
    outputDiv.textContent = '';
    outputDiv.classList.remove('error');

    // Create output capture
    let capturedOutput = [];

    // Redirect stdout
    const originalWrite = console.log;
    console.log = function(...args) {
        capturedOutput.push(args.join(' '));
        originalWrite.apply(console, args);
    };

    try {
        // Execute Python code
        window.__BRYTHON__.python_to_js(code);
        const result = eval(window.__BRYTHON__.imported['__main__']);

        // Display output
        if (capturedOutput.length > 0) {
            outputDiv.textContent = capturedOutput.join('\n');
        } else if (result !== undefined) {
            outputDiv.textContent = String(result);
        } else {
            outputDiv.textContent = '(no output)';
        }
    } catch (error) {
        // Display error
        outputDiv.classList.add('error');
        outputDiv.textContent = `Error: ${error.message}\n\n${error.stack || ''}`;
    } finally {
        // Restore stdout
        console.log = originalWrite;
    }
}

// Make runExample globally available
window.runExample = runExample;
```

3. Update `mkdocs.yml` to include Brython:

```yaml
extra_javascript:
  - https://cdn.jsdelivr.net/npm/brython@3.12.0/brython.min.js
  - https://cdn.jsdelivr.net/npm/brython@3.12.0/brython_stdlib.js
  - javascripts/brython-setup.js

extra_css:
  - stylesheets/terminal.css
```

**Test:**

1. Create a simple test page `docs/test-brython.md`:

```markdown
# Brython Test

<div class="terminal-window interactive-example">
    <div class="terminal-header">
        <span class="terminal-title">[python3 test.py]</span>
        <button class="terminal-run-btn" onclick="runExample('test1')">RUN</button>
    </div>
    <div class="terminal-body">
        <textarea class="code-editor" id="editor-test1">print("Hello from Brython!")
print(2 + 2)</textarea>
        <div class="terminal-output" id="output-test1">
            <span class="terminal-prompt">root@plotille:~$</span>
            <div class="output-content"></div>
        </div>
    </div>
</div>
```

2. Update `mkdocs.yml` nav to include test page:

```yaml
nav:
  - Home: index.md
  - Test: test-brython.md
```

3. Test:
```bash
mkdocs serve
# Visit http://127.0.0.1:8000/test-brython/
# Click RUN button, verify "Hello from Brython!" appears
```

**Commit:** `Add Brython runtime integration`

---

### Task 6.2: Implement Plotille Mock for Brython

**What:** Since plotille won't work directly in Brython, create a browser-compatible version.

**Considerations:**

This is complex. Plotille uses features that may not work in Brython. For the initial implementation:

**Option A:** Bundle the actual plotille source and hope it works in Brython
**Option B:** Create a simplified browser-compatible version
**Option C:** Use a server-side execution API (more complex)

**Recommended approach:** Try Option A first (simplest per YAGNI). If plotille doesn't work in Brython, we'll need to discuss alternatives.

**Files to create:**
- `docs/javascripts/plotille-brython.js` (loader script)

**Actions:**

1. Copy plotille source to docs for Brython access:

```bash
# Create a script to copy plotille sources
cat > scripts/copy_plotille_for_brython.py << 'EOF'
#!/usr/bin/env python3
"""Copy plotille source files for Brython access."""
import shutil
from pathlib import Path

def main():
    project_root = Path(__file__).parent.parent
    source_dir = project_root / "plotille"
    dest_dir = project_root / "docs" / "src" / "lib" / "plotille"

    # Remove old copy
    if dest_dir.exists():
        shutil.rmtree(dest_dir)

    # Copy plotille source
    shutil.copytree(source_dir, dest_dir)
    print(f"Copied plotille to {dest_dir}")

if __name__ == "__main__":
    main()
EOF

chmod +x scripts/copy_plotille_for_brython.py
```

2. Run the copy script:
```bash
python scripts/copy_plotille_for_brython.py
```

3. Update `scripts/generate_docs.py` to run this during generation:

```python
# Add at the end of main() before return
def main() -> int:
    # ... existing code ...

    # Copy plotille for Brython
    print("\nCopying plotille for Brython...")
    copy_script = project_root / "scripts" / "copy_plotille_for_brython.py"
    subprocess.run([sys.executable, str(copy_script)], check=True)

    print("\n✓ Documentation generation complete")
    return 0
```

**Test:**

This requires actual testing with examples. We'll validate this in the next phase when integrating CodeMirror.

**Commit:** `Add plotille source copying for Brython access`

---

## Phase 7: CodeMirror Integration

### Task 7.1: Add CodeMirror 6 Setup

**What:** Integrate CodeMirror 6 for code editing with Python syntax highlighting.

**Files to create:**
- `docs/javascripts/codemirror-setup.js`

**Actions:**

1. Update `mkdocs.yml` to include CodeMirror from CDN:

```yaml
extra_javascript:
  - https://cdn.jsdelivr.net/npm/brython@3.12.0/brython.min.js
  - https://cdn.jsdelivr.net/npm/brython@3.12.0/brython_stdlib.js
  # CodeMirror 6
  - https://cdn.jsdelivr.net/npm/codemirror@6.0.1/dist/index.min.js
  - https://cdn.jsdelivr.net/npm/@codemirror/lang-python@6.1.3/dist/index.min.js
  - https://cdn.jsdelivr.net/npm/@codemirror/theme-one-dark@6.1.2/dist/index.min.js
  - javascripts/codemirror-setup.js
  - javascripts/brython-setup.js
```

2. Create `docs/javascripts/codemirror-setup.js`:

```javascript
/**
 * CodeMirror 6 setup for plotille documentation.
 *
 * Converts textarea elements into CodeMirror editors with Python highlighting.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Wait for CodeMirror to load
    if (typeof CodeMirror === 'undefined') {
        console.error('CodeMirror not loaded');
        return;
    }

    // Find all code editor textareas
    const editors = document.querySelectorAll('.code-editor');

    editors.forEach(textarea => {
        const editorId = textarea.id;
        const initialCode = textarea.value;

        // Create CodeMirror editor
        // Note: This uses basic textarea for now
        // Full CodeMirror 6 integration would require bundling
        // For simplicity, we'll enhance the textarea with basic features

        textarea.style.fontFamily = "'IBM Plex Mono', monospace";
        textarea.style.fontSize = '14px';
        textarea.style.lineHeight = '1.5';
        textarea.style.tabSize = '4';

        // Add tab key support
        textarea.addEventListener('keydown', function(e) {
            if (e.key === 'Tab') {
                e.preventDefault();
                const start = this.selectionStart;
                const end = this.selectionEnd;
                const value = this.value;

                // Insert 4 spaces
                this.value = value.substring(0, start) + '    ' + value.substring(end);
                this.selectionStart = this.selectionEnd = start + 4;
            }
        });

        console.log(`Editor initialized: ${editorId}`);
    });
});
```

**Note:** Full CodeMirror 6 integration from CDN is complex. The above provides basic textarea enhancement. If you need full CodeMirror features (syntax highlighting, autocomplete), you'll need to either:

A) Bundle CodeMirror properly with a build step
B) Use a simpler approach (current implementation)
C) Use CDN but with more complex module loading

For now, **proceed with enhanced textarea** (YAGNI). Full CodeMirror can be added later if needed.

**Test:**

```bash
mkdocs serve
# Visit test-brython page
# Verify code editor has monospace font and tab key works
```

**Commit:** `Add CodeMirror setup with textarea enhancement`

---

### Task 7.2: Improve Brython Execution with Output Capture

**What:** Better stdout capturing for Brython execution.

**Files to modify:**
- `docs/javascripts/brython-setup.js`

**Actions:**

Replace the `runExample` function in `brython-setup.js`:

```javascript
/**
 * Execute Python code in an example with proper output capture.
 *
 * @param {string} exampleName - Name of the example to run
 */
function runExample(exampleName) {
    const editor = document.getElementById(`editor-${exampleName}`);
    const outputDiv = document.querySelector(`#output-${exampleName} .output-content`);

    if (!editor || !outputDiv) {
        console.error(`Example ${exampleName} not found`);
        return;
    }

    const code = editor.value;

    // Clear previous output
    outputDiv.textContent = '';
    outputDiv.classList.remove('error');

    // Show loading indicator
    outputDiv.textContent = 'Running...';

    // Use setTimeout to allow UI update
    setTimeout(() => {
        try {
            // Create a new output buffer
            let outputBuffer = [];

            // Monkey-patch print for output capture
            const printFunc = function(...args) {
                const line = args.join(' ');
                outputBuffer.push(line);
            };

            // Inject print into the Python code
            const wrappedCode = `
import sys
from io import StringIO

__output__ = StringIO()
__old_stdout__ = sys.stdout
sys.stdout = __output__

try:
${code.split('\n').map(line => '    ' + line).join('\n')}
finally:
    sys.stdout = __old_stdout__
    print(__output__.getvalue(), end='')
`;

            // Execute with Brython
            const script = document.createElement('script');
            script.type = 'text/python';
            script.id = `brython-script-${exampleName}`;
            script.textContent = wrappedCode;

            // Add output capture
            window.__brython_output__ = '';
            const oldLog = console.log;
            console.log = function(...args) {
                window.__brython_output__ += args.join(' ') + '\n';
                oldLog.apply(console, args);
            };

            document.body.appendChild(script);

            // Run Brython on this script
            if (window.brython) {
                brython({debug: 1, ids: [script.id]});
            }

            // Restore console.log
            console.log = oldLog;

            // Small delay to capture output
            setTimeout(() => {
                const output = window.__brython_output__ || '(no output)';
                outputDiv.textContent = output;

                // Clean up
                script.remove();
                delete window.__brython_output__;
            }, 100);

        } catch (error) {
            // Display error
            outputDiv.classList.add('error');
            outputDiv.textContent = `Error: ${error.message}`;
            console.error('Brython execution error:', error);
        }
    }, 10);
}
```

**Test:**

```bash
mkdocs serve
# Test the example execution again
# Verify output is captured correctly
```

**Commit:** `Improve Brython output capture`

---

## Phase 8: API Documentation with mkdocstrings

### Task 8.1: Configure mkdocstrings for API Reference

**What:** Set up automatic API documentation generation from docstrings.

**Files to modify:**
- `mkdocs.yml`

**Actions:**

1. Update `mkdocs.yml` plugins section:

```yaml
plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          options:
            docstring_style: google
            show_source: true
            show_root_heading: true
            show_root_full_path: false
            show_signature_annotations: true
            separate_signature: true
            show_symbol_type_heading: true
            show_symbol_type_toc: true
            signature_crossrefs: true
            merge_init_into_class: true
          paths: [plotille]
```

2. Create API reference structure in `docs/api/`:

```bash
mkdir -p docs/api
```

3. Create `docs/api/index.md`:

```markdown
# API Reference

Complete API documentation for plotille.

## High-Level Functions

Quick plotting functions for simple use cases.

- [Plotting Functions](plotting.md) - `plot()`, `scatter()`, `histogram()`
- [Figure Class](figure.md) - Compose complex multi-plot visualizations

## Core Components

- [Canvas](canvas.md) - Low-level drawing primitives
- [Colors](colors.md) - Color handling and themes

## Utilities

- [Input Formatting](formatting.md) - Data preprocessing
- [Data Types](datatypes.md) - Internal data structures
```

4. Create `docs/api/plotting.md`:

```markdown
# Plotting Functions

High-level plotting functions for quick visualizations.

## plot

::: plotille.plot
    options:
      show_root_heading: true
      show_source: true

## scatter

::: plotille.scatter
    options:
      show_root_heading: true
      show_source: true

## hist

::: plotille.hist
    options:
      show_root_heading: true
      show_source: true

## histogram

::: plotille.histogram
    options:
      show_root_heading: true
      show_source: true
```

5. Create `docs/api/figure.md`:

```markdown
# Figure

The Figure class for composing complex visualizations.

::: plotille.Figure
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - plot
        - scatter
        - histogram
        - text
        - axvline
        - axhline
        - axvspan
        - axhspan
        - imgshow
        - show
        - clear
```

6. Create `docs/api/canvas.md`:

```markdown
# Canvas

Low-level canvas for direct drawing.

::: plotille.Canvas
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - point
        - line
        - rect
        - text
        - braille_image
        - image
        - plot
```

**Test:**

```bash
mkdocs serve
# Visit http://127.0.0.1:8000/api/
# Verify API documentation appears with docstrings
```

**Commit:** `Add mkdocstrings API reference configuration`

---

### Task 8.2: Enhance Docstrings with Examples (Sample)

**What:** Add doctest examples to key functions as a template.

**Files to modify:**
- `plotille/_graphs.py` (or wherever `plot()` is defined)

**Actions:**

This task demonstrates enhancing ONE function as an example. You'll repeat this pattern for other functions.

1. Find the `plot()` function (likely in `plotille/__init__.py` or `plotille/_graphs.py`)

2. Enhance its docstring with a doctest example:

```python
def plot(
    X,
    Y,
    width=80,
    height=40,
    X_label='X',
    Y_label='Y',
    linesep=os.linesep,
    interp='linear',
    x_min=None,
    x_max=None,
    y_min=None,
    y_max=None,
    lc=None,
    bg=None,
    color_mode='names',
    origin=True,
    marker=None,
):
    """
    Create plot with X, Y values and linear interpolation between points.

    Parameters:
        X: List[float]         X values.
        Y: List[float]         Y values. X and Y must have the same number of entries.
        width: int             The number of characters for the width (columns) of the canvas.
        height: int            The number of characters for the height (rows) of the canvas.
        X_label: str           Label for X-axis.
        Y_label: str           Label for Y-axis. max 8 characters.
        linesep: str           The requested line separator. default: os.linesep
        interp: Optional[str]  Specify interpolation; values None, 'linear'
        x_min, x_max: float    Limits for the displayed X values.
        y_min, y_max: float    Limits for the displayed Y values.
        lc: multiple           Give the line color.
        bg: multiple           Give the background color.
        color_mode: str        Specify color input mode; 'names' (default), 'byte' or 'rgb'
                              see plotille.color.__docs__
        origin: bool           Whether to print the origin. default: True
        marker: str            Instead of braille dots set a marker char for actual values.

    Returns:
        str: plot over `X`, `Y`.

    Examples:
        Simple line plot:

        >>> import plotille
        >>> X = [1, 2, 3, 4, 5]
        >>> Y = [1, 4, 2, 3, 5]
        >>> result = plotille.plot(X, Y, width=40, height=10)
        >>> '⠀' in result  # Contains braille dots
        True
        >>> 'X' in result  # Contains axis label
        True

        Plot with custom range:

        >>> result = plotille.plot([0, 1], [0, 1], width=20, height=5,
        ...                         x_min=0, x_max=1, y_min=0, y_max=1)
        >>> len(result) > 0
        True
    """
    # ... existing implementation ...
```

**Test:**

```bash
# Run doctests
pytest --doctest-modules plotille/_graphs.py -v
# Or wherever plot() is defined

# Should show doctests passing
```

**Commit:** `Add doctest examples to plot() function`

---

### Task 8.3: Add Doctests to Core Functions (Iterative)

**What:** Systematically add doctest examples to all public functions.

**Files to modify:**
- All files in `plotille/` directory with public functions

**Actions:**

This is a large task. Break it down:

1. Create a checklist of functions to document:

```bash
# Generate list of public functions
python -c "
import plotille
import inspect

members = inspect.getmembers(plotille, inspect.isfunction)
public = [name for name, _ in members if not name.startswith('_')]
for name in sorted(public):
    print(f'- [ ] {name}')
" > docs/plans/doctest-checklist.md
```

2. For each function:
   - Read existing docstring
   - Add at least one `>>>` example showing basic usage
   - Add edge case examples if relevant
   - Run `pytest --doctest-modules` to verify
   - Commit with message like `Add doctests to scatter() function`

3. Prioritize by importance:
   - High-level functions first (`plot`, `scatter`, `hist`, etc.)
   - Then `Figure` methods
   - Then `Canvas` methods
   - Finally utility functions

**Test:**

After each function:
```bash
pytest --doctest-modules plotille/ -v
# All doctests should pass
```

**This is iterative:** Do a few functions, commit, repeat. Don't do all at once.

**Commit pattern:** `Add doctests to <function_name>()`

---

## Phase 9: Navigation and Site Structure

### Task 9.1: Update Navigation in mkdocs.yml

**What:** Define the site navigation structure.

**Files to modify:**
- `mkdocs.yml`

**Actions:**

Update the `nav` section in `mkdocs.yml`:

```yaml
nav:
  - Home: index.md
  - Cookbook:
      - Basic Plots: cookbook/basic.md
      - Complex Figures: cookbook/figures.md
      - Canvas Drawing: cookbook/canvas.md
      - Advanced Examples: cookbook/advanced.md
  - API Reference:
      - Overview: api/index.md
      - Plotting Functions: api/plotting.md
      - Figure: api/figure.md
      - Canvas: api/canvas.md
```

**Test:**

```bash
mkdocs serve
# Verify navigation structure appears correctly
# All links work
```

**Commit:** `Configure site navigation structure`

---

### Task 9.2: Customize Navigation Sidebar Styling

**What:** Style the navigation to match terminal aesthetic.

**Files to modify:**
- `docs/stylesheets/terminal.css`

**Actions:**

Add to `docs/stylesheets/terminal.css`:

```css
/* Navigation as terminal directory listing */
.md-nav {
    font-family: 'IBM Plex Mono', monospace;
}

.md-nav__title {
    font-family: 'VT323', monospace;
    color: var(--amber-bright);
    font-size: 1.2rem;
    text-shadow: 0 0 5px var(--amber-glow);
}

.md-nav__list {
    list-style: none;
}

.md-nav__item {
    position: relative;
}

.md-nav__link {
    color: var(--amber-base);
    padding-left: 1.5rem;
    transition: color 0.2s, text-shadow 0.2s;
}

.md-nav__link:hover {
    color: var(--amber-bright);
    text-shadow: 0 0 8px var(--amber-glow);
}

/* Terminal prompt indicator for active item */
.md-nav__link--active {
    color: var(--amber-bright);
    font-weight: 600;
}

.md-nav__link--active::before {
    content: 'root@plotille:~$';
    position: absolute;
    left: -8rem;
    color: var(--amber-dim);
    font-size: 0.85rem;
    opacity: 0.7;
}

/* Folder icons using braille */
.md-nav__item--nested > .md-nav__link::before {
    content: '⠿ ';
    color: var(--amber-dim);
}

.md-nav__item:not(.md-nav__item--nested) > .md-nav__link::before {
    content: '⣿ ';
    color: var(--amber-dim);
    font-size: 0.6rem;
}
```

**Test:**

```bash
mkdocs serve
# Check navigation sidebar styling
# Verify braille icons appear
# Test hover effects
```

**Commit:** `Add terminal-styled navigation sidebar`

---

## Phase 10: Hero Animation

### Task 10.1: Create Animated Hero Plot

**What:** Animate a plotille graph appearing on the home page.

**Files to create:**
- `docs/javascripts/hero-animation.js`

**Actions:**

1. Create `docs/javascripts/hero-animation.js`:

```javascript
/**
 * Animated hero plot for home page.
 *
 * Draws a sine wave using braille dots, character by character.
 */

function animateHeroPlot() {
    const heroPlot = document.getElementById('hero-animation');

    if (!heroPlot) {
        return;
    }

    // Example plotille output (sine wave)
    // This would ideally be generated server-side
    const plotOutput = `    5.00┤                                    ⡰⠊⠉⠉⠉⢉⡭⠋
        ┤                                 ⢀⡠⠊        ⢸
        ┤                              ⢀⡠⠊⠁           ⢸
        ┤                           ⢀⡠⠊⠁              ⢸
        ┤                        ⢀⡠⠊⠁                 ⢸
    0.00┼⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⢤⡠⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⢼⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤
        ┤                 ⢠⠊⠁                          ⢸
        ┤              ⢀⡠⠊                             ⢸
        ┤           ⢀⡠⠊⠁                               ⢸
        ┤        ⢀⡠⠊⠁                                  ⢸
   -5.00┤⣀⣀⣀⡠⠤⠊⠁                                     ⠈⠉⠉⠉⠑⠒⠤⣀⣀⣀
        └────────────────────────────────────────────────────────
        -3.14                     X                         3.14`;

    // Animate character by character
    const chars = plotOutput.split('');
    let index = 0;

    heroPlot.textContent = '';

    const interval = setInterval(() => {
        if (index < chars.length) {
            heroPlot.textContent += chars[index];
            index++;
        } else {
            clearInterval(interval);
        }
    }, 5); // 5ms per character = ~1 second for 200 chars
}

// Run animation when page loads
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(animateHeroPlot, 500); // Slight delay after page load
});
```

2. Update `mkdocs.yml` to include the script:

```yaml
extra_javascript:
  - https://cdn.jsdelivr.net/npm/brython@3.12.0/brython.min.js
  - https://cdn.jsdelivr.net/npm/brython@3.12.0/brython_stdlib.js
  - javascripts/codemirror-setup.js
  - javascripts/brython-setup.js
  - javascripts/hero-animation.js
```

**Better approach:** Generate the hero plot dynamically during doc build.

3. Update `scripts/generate_docs.py` to generate hero plot:

```python
def generate_hero_plot() -> str:
    """
    Generate a sample plot for the hero animation.

    Returns:
        String containing plotille plot output
    """
    try:
        import plotille
        import math

        X = [i / 10 for i in range(-31, 32)]
        Y = [math.sin(x) for x in X]

        plot_output = plotille.plot(
            X, Y,
            width=60,
            height=10,
            X_label='X',
            Y_label='',
        )

        return plot_output
    except Exception as e:
        # Fallback if generation fails
        return "Error generating plot"


# Update generate_home_page()
def generate_home_page(docs_dir: Path) -> Path:
    """Generate the home/index page."""
    hero_plot = generate_hero_plot()

    content = f"""# plotille

<div class="hero-terminal">
    <div class="terminal-header">
        <span class="terminal-title">[root@plotille ~]$</span>
    </div>
    <div class="terminal-body">
        <pre class="hero-plot" id="hero-animation">{hero_plot}</pre>
    </div>
</div>

Plot in the terminal using braille dots, with no dependencies.

## Features

- **Scatter plots, line plots, histograms** - Basic plotting functions
- **Complex figures** - Compose multiple plots with legends
- **Canvas drawing** - Direct pixel manipulation for custom visualizations
- **Image rendering** - Display images using braille dots or background colors
- **Color support** - Multiple color modes: names, byte values, RGB
- **No dependencies** - Pure Python with no external requirements

## Quick Start

Install plotille:

```bash
pip install plotille
```

Create your first plot:

```python
import plotille
import math

X = [i/10 for i in range(-30, 30)]
Y = [math.sin(x) for x in X]

print(plotille.plot(X, Y, height=20, width=60))
```

## Explore

Browse the [cookbook](cookbook/basic/) to see interactive examples you can edit and run in your browser.

"""

    index_file = docs_dir / "index.md"
    index_file.write_text(content)
    return index_file
```

**Test:**

```bash
python scripts/generate_docs.py
mkdocs serve
# Visit home page, verify plot appears in hero section
```

**Commit:** `Add hero plot to home page`

---

## Phase 11: GitHub Actions CI/CD

### Task 11.1: Create Documentation Build Workflow

**What:** Automate doc building and deployment on push to main.

**Files to create:**
- `.github/workflows/docs.yml`

**Actions:**

1. Create directory:
```bash
mkdir -p .github/workflows
```

2. Create `.github/workflows/docs.yml`:

```yaml
name: Build and Deploy Documentation

on:
  push:
    branches:
      - master  # Adjust if your main branch is named differently
  workflow_dispatch:  # Allow manual trigger

permissions:
  contents: write  # Needed to push to gh-pages

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for proper git info

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      - name: Run tests (including doctests)
        run: |
          pytest --doctest-modules plotille/ -v

      - name: Generate documentation
        run: |
          python scripts/generate_docs.py

      - name: Build MkDocs site
        run: |
          mkdocs build --strict

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
          cname: plotille.tammo.io
```

**Test:**

You can't fully test this until you push to GitHub, but you can verify the workflow syntax:

```bash
# Install actionlint for workflow validation (optional)
# brew install actionlint  # macOS
# Or download from https://github.com/rhysd/actionlint

# Validate workflow
actionlint .github/workflows/docs.yml

# Or just verify it's valid YAML
python -c "import yaml; yaml.safe_load(open('.github/workflows/docs.yml'))"
```

**Commit:** `Add GitHub Actions workflow for documentation`

---

### Task 11.2: Configure GitHub Pages Settings

**What:** Set up GitHub repository for Pages deployment.

**Actions (to be done in GitHub web interface):**

1. Push the changes to GitHub:
```bash
git push origin master  # Or your main branch
```

2. Go to repository Settings → Pages

3. Under "Build and deployment":
   - Source: "Deploy from a branch"
   - Branch: Select `gh-pages` and `/ (root)`
   - Click "Save"

4. Under "Custom domain":
   - Enter: `plotille.tammo.io`
   - Click "Save"
   - Wait for DNS check to complete

5. Enable "Enforce HTTPS" once DNS check passes

**DNS Configuration (at your domain registrar):**

Add CNAME record:
```
Host: plotille
Points to: tammoippen.github.io
```

**Test:**

After workflow runs and DNS propagates:
- Visit https://plotille.tammo.io
- Verify site loads with documentation
- Check that HTTPS works

**Commit:** (No code changes, just documentation of steps)

---

## Phase 12: Testing and Polish

### Task 12.1: Manual Testing Checklist

**What:** Comprehensive testing of the documentation site.

**Actions:**

Create a testing checklist `docs/plans/testing-checklist.md`:

```markdown
# Documentation Testing Checklist

## Visual Design
- [ ] Amber phosphor color scheme applies throughout
- [ ] IBM Plex Mono font loads correctly
- [ ] VT323 font loads for headers
- [ ] Scanline effect is visible but not distracting
- [ ] Terminal windows have proper styling
- [ ] Navigation sidebar matches terminal aesthetic
- [ ] Responsive design works on mobile

## Navigation
- [ ] All navigation links work
- [ ] Breadcrumbs function correctly
- [ ] Search works (if enabled)
- [ ] Active page is highlighted in sidebar
- [ ] Braille dot icons appear in navigation

## Home Page
- [ ] Hero plot displays correctly
- [ ] Quick start code block renders
- [ ] Links to cookbook work

## Cookbook Pages
- [ ] All four category pages exist (basic, figures, canvas, advanced)
- [ ] Examples are categorized correctly
- [ ] Interactive examples have working editors
- [ ] Run buttons work for interactive examples
- [ ] Output displays correctly
- [ ] Static examples show pre-rendered output
- [ ] Dependency warnings show for static examples

## Interactive Examples
- [ ] Code editor is editable
- [ ] Tab key inserts spaces
- [ ] Run button executes code
- [ ] Output appears in terminal-styled div
- [ ] Errors display clearly
- [ ] Can modify code and re-run
- [ ] Multiple examples on same page don't interfere

## API Reference
- [ ] All API pages exist
- [ ] Docstrings render correctly
- [ ] Type hints display properly
- [ ] Function signatures are clear
- [ ] Examples in docstrings render
- [ ] Cross-references link correctly
- [ ] Source code links work

## Doctests
- [ ] All doctests pass: `pytest --doctest-modules plotille/`
- [ ] Coverage is reasonable (aim for 80%+ of public functions)

## Build Process
- [ ] `python scripts/generate_docs.py` completes without errors
- [ ] `mkdocs build` completes without warnings
- [ ] Generated site is in `site/` directory
- [ ] No broken links in built site

## CI/CD
- [ ] GitHub Actions workflow runs successfully
- [ ] Documentation deploys to gh-pages branch
- [ ] Site is accessible at plotille.tammo.io
- [ ] HTTPS works
- [ ] Custom domain configured correctly

## Performance
- [ ] Page load time is reasonable (<3s)
- [ ] No console errors in browser
- [ ] Brython loads correctly
- [ ] Fonts load without flash of unstyled text

## Browser Compatibility
- [ ] Works in Chrome/Chromium
- [ ] Works in Firefox
- [ ] Works in Safari
- [ ] Works in Edge
```

Work through this checklist systematically, fixing issues as you find them.

**Commit pattern:** `Fix: <issue description>` for each fix

---

### Task 12.2: Add Error Styling for Interactive Examples

**What:** Better error display when code fails.

**Files to modify:**
- `docs/stylesheets/terminal.css`

**Actions:**

Add error styling to `terminal.css`:

```css
/* Error output styling */
.terminal-output .error {
    color: #ff6b6b;
    background: rgba(255, 0, 0, 0.1);
    border-left: 3px solid #ff6b6b;
    padding-left: 0.5rem;
}

.output-content.error {
    color: #ff6b6b;
}

/* Loading state */
.terminal-output .loading::after {
    content: '...';
    animation: loading 1.5s infinite;
}

@keyframes loading {
    0%, 100% { opacity: 0; }
    50% { opacity: 1; }
}
```

**Test:**

Create a test example that intentionally errors:

```markdown
# Error Test

<div class="terminal-window interactive-example">
    <div class="terminal-header">
        <span class="terminal-title">[python3 error.py]</span>
        <button class="terminal-run-btn" onclick="runExample('error1')">RUN</button>
    </div>
    <div class="terminal-body">
        <textarea class="code-editor" id="editor-error1">
raise ValueError("Test error message")
        </textarea>
        <div class="terminal-output" id="output-error1">
            <span class="terminal-prompt">root@plotille:~$</span>
            <div class="output-content"></div>
        </div>
    </div>
</div>
```

Verify error displays with red styling.

**Commit:** `Add error styling for interactive examples`

---

### Task 12.3: Add README Section About Documentation

**What:** Update project README to link to the new documentation site.

**Files to modify:**
- `README.md`

**Actions:**

Add a documentation section near the top of `README.md`:

```markdown
## Documentation

📚 **Full documentation available at [plotille.tammo.io](https://plotille.tammo.io)**

Features:
- **Interactive examples** - Edit and run code in your browser
- **Complete API reference** - Auto-generated from source
- **Cookbook** - Examples organized by complexity

```

**Commit:** `Add documentation link to README`

---

## Phase 13: Refinement and Edge Cases

### Task 13.1: Handle Empty/Missing Examples Gracefully

**What:** Ensure generation script handles edge cases.

**Files to modify:**
- `scripts/generate_docs.py`

**Actions:**

Add validation to generation script:

```python
def main() -> int:
    """Main entry point."""
    project_root = Path(__file__).parent.parent
    examples_dir = project_root / "examples"
    output_dir = project_root / "docs" / "assets" / "example-outputs"
    docs_dir = project_root / "docs"

    if not examples_dir.exists():
        print(f"Error: {examples_dir} not found", file=sys.stderr)
        return 1

    # Analyze all Python files
    examples = []
    for example_file in sorted(examples_dir.glob("*.py")):
        try:
            info = analyze_example(example_file)
            examples.append(info)
        except Exception as e:
            print(f"Warning: Failed to analyze {example_file.name}: {e}",
                  file=sys.stderr)
            continue

    if not examples:
        print("Warning: No examples found", file=sys.stderr)
        # Generate placeholder pages
        for category in ['basic', 'figures', 'canvas', 'advanced']:
            category_dir = docs_dir / "cookbook"
            category_dir.mkdir(parents=True, exist_ok=True)
            placeholder = category_dir / f"{category}.md"
            placeholder.write_text(f"# {category.title()}\n\nNo examples yet.\n")
        return 0

    # ... rest of existing code ...
```

**Test:**

```bash
# Test with no examples (temporarily)
mv examples examples.backup
mkdir examples
python scripts/generate_docs.py
# Should handle gracefully

# Restore
rmdir examples
mv examples.backup examples
```

**Commit:** `Add error handling for missing examples`

---

### Task 13.2: Add Source File Headers

**What:** Ensure all documentation source files have descriptive headers.

**Files to check:**
- `scripts/generate_docs.py`
- `docs/javascripts/*.js`
- `docs/stylesheets/*.css`

**Actions:**

Add headers following the CLAUDE.md rule about ABOUTME comments:

Example for `scripts/generate_docs.py`:

```python
#!/usr/bin/env python3
# ABOUTME: Generates plotille documentation from examples and source code.
# ABOUTME: Analyzes examples, executes static ones, and creates markdown pages.
"""
Generate documentation from examples.

This script:
1. Scans examples/ directory
2. Classifies examples by dependencies
3. Generates markdown files for MkDocs
"""
```

Check each file and add appropriate headers.

**Commit:** `Add ABOUTME headers to documentation files`

---

### Task 13.3: Performance Optimization - Lazy Load Brython

**What:** Only load Brython on pages that need it.

**Files to modify:**
- `mkdocs.yml`
- `docs/javascripts/brython-setup.js`

**Actions:**

1. Update `mkdocs.yml` to conditionally load Brython:

```yaml
# Move Brython scripts to be loaded only when needed
extra_javascript:
  - javascripts/codemirror-setup.js
  - javascripts/hero-animation.js
  # Brython loaded conditionally
```

2. Update example pages to load Brython:

In `scripts/generate_docs.py`, update `generate_interactive_example_markdown()`:

```python
def generate_interactive_example_markdown(info: ExampleInfo) -> str:
    """Generate markdown for an interactive example."""
    source_code = info.path.read_text()
    escaped_code = source_code.replace('```', '\\`\\`\\`')

    # Add script tag to load Brython on this page
    brython_loader = '''
<script src="https://cdn.jsdelivr.net/npm/brython@3.12.0/brython.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/brython@3.12.0/brython_stdlib.js"></script>
<script src="/javascripts/brython-setup.js"></script>
'''

    return f"""{brython_loader}

## {info.name}

{info.description}

<div class="terminal-window interactive-example" data-example="{info.name}">
    ...
</div>

"""
```

**Note:** This optimization is optional (YAGNI). Only implement if page load time is actually slow.

**Commit:** (Optional) `Optimize: Lazy load Brython on interactive pages`

---

## Phase 14: Finalization

### Task 14.1: Write Documentation for Contributors

**What:** Document the doc system for future maintainers.

**Files to create:**
- `docs/contributing.md`
- `CONTRIBUTING.md` (link to above)

**Actions:**

1. Create `docs/contributing.md`:

```markdown
# Contributing to plotille

Thank you for contributing to plotille!

## Documentation System

The documentation is built with MkDocs and auto-deployed to https://plotille.tammo.io

### Structure

- `docs/` - Documentation source files (markdown)
- `examples/` - Example scripts (auto-imported to docs)
- `scripts/generate_docs.py` - Documentation generation script
- `mkdocs.yml` - MkDocs configuration

### Local Development

1. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

2. Generate docs from examples:
   ```bash
   python scripts/generate_docs.py
   ```

3. Serve locally:
   ```bash
   mkdocs serve
   ```

4. Visit http://127.0.0.1:8000

### Adding Examples

1. Create a new `.py` file in `examples/`
2. Add a docstring or comment at the top describing it
3. Run `python scripts/generate_docs.py`
4. The example will automatically appear in the cookbook

Examples using only plotille + stdlib will be interactive in the browser.
Examples using numpy, Pillow, etc. will show pre-rendered output.

### Updating API Documentation

API docs are auto-generated from docstrings using mkdocstrings.

1. Update docstrings in `plotille/` source files
2. Add examples using doctest format (`>>>`)
3. Run tests: `pytest --doctest-modules plotille/`
4. Rebuild docs: `mkdocs build`

All doctest examples must pass before deploying.

### Deployment

Documentation auto-deploys on push to `master`:
1. GitHub Actions runs tests
2. Generates documentation
3. Builds MkDocs site
4. Deploys to gh-pages branch
5. Available at https://plotille.tammo.io

### Theme Customization

The documentation uses a custom amber phosphor CRT theme:
- Colors: `docs/stylesheets/terminal.css`
- JavaScript: `docs/javascripts/`
- Theme: Material for MkDocs with heavy customization
```

2. Create `CONTRIBUTING.md` at project root:

```markdown
# Contributing

See the full contributing guide: https://plotille.tammo.io/contributing/
```

3. Update `mkdocs.yml` nav:

```yaml
nav:
  - Home: index.md
  - Cookbook:
      - Basic Plots: cookbook/basic.md
      - Complex Figures: cookbook/figures.md
      - Canvas Drawing: cookbook/canvas.md
      - Advanced Examples: cookbook/advanced.md
  - API Reference:
      - Overview: api/index.md
      - Plotting Functions: api/plotting.md
      - Figure: api/figure.md
      - Canvas: api/canvas.md
  - Contributing: contributing.md
```

**Commit:** `Add contributing documentation`

---

### Task 14.2: Final Testing and Launch

**What:** Complete final testing before announcement.

**Actions:**

1. Work through complete testing checklist (Task 12.1)

2. Test on multiple browsers and devices

3. Check performance with browser DevTools

4. Verify all links work (use link checker):
```bash
# Optional: install link checker
# pip install linkchecker

# Build site
mkdocs build

# Check links
# linkchecker site/index.html
```

5. Get a fresh pair of eyes to review (if possible)

**Commit:** `Final polish and testing`

---

### Task 14.3: Create Announcement

**What:** Prepare announcement of new documentation.

**Files to create:**
- `docs/plans/launch-announcement.md`

**Actions:**

Create launch announcement draft:

```markdown
# plotille Documentation Launch

New comprehensive documentation site now available at **https://plotille.tammo.io**!

## What's New

🖥️ **Interactive Examples** - Edit and run plotille code directly in your browser
📚 **Complete API Reference** - Auto-generated from source with examples
🎨 **Terminal Aesthetic** - Amber phosphor CRT theme
🔍 **Searchable** - Find functions and examples quickly
📱 **Responsive** - Works on mobile and desktop

## Highlights

- **Cookbook-first approach** - Learn by example
- **Live code editing** - Powered by Brython
- **Tested documentation** - All examples verified with doctests
- **Auto-deployed** - Always up to date with latest release

Check it out: https://plotille.tammo.io

---

Technical details:
- Built with MkDocs + mkdocstrings
- Custom amber phosphor terminal theme
- Interactive examples via Brython
- Deployed via GitHub Actions to GitHub Pages
```

**Commit:** `Add launch announcement`

---

## Summary and Next Steps

You've now implemented a complete documentation system for plotille!

### What You Built

1. ✅ **Documentation generator** - Analyzes and categorizes examples
2. ✅ **Static pre-rendering** - Executes examples during build
3. ✅ **Interactive examples** - Brython-powered browser execution
4. ✅ **API reference** - Auto-generated with mkdocstrings
5. ✅ **Terminal aesthetic** - Amber phosphor CRT theme
6. ✅ **CI/CD pipeline** - Auto-deploy on push to main
7. ✅ **Doctest integration** - Tested documentation examples

### Commands Reference

```bash
# Generate documentation
python scripts/generate_docs.py

# Serve locally
mkdocs serve

# Build for production
mkdocs build

# Run doctests
pytest --doctest-modules plotille/

# Deploy (via CI)
git push origin master
```

### Maintenance

- **Add examples**: Just add `.py` files to `examples/`
- **Update API docs**: Edit docstrings in `plotille/` source
- **Theme changes**: Edit `docs/stylesheets/terminal.css`
- **Behavior changes**: Edit `docs/javascripts/*.js`

### Known Limitations

1. **Brython compatibility**: Some Python features may not work in browser
2. **External dependencies**: numpy/Pillow examples show pre-rendered output only
3. **Performance**: Loading Brython adds ~500KB to page size
4. **Browser support**: Requires modern browser with ES6 support

### Future Enhancements (Optional)

- Full CodeMirror 6 integration with syntax highlighting
- Version switching (using mike plugin)
- More sophisticated Brython output capture
- Screenshot generation for social media sharing
- Dark/light theme toggle
- More examples and tutorials

---

## Troubleshooting

### Common Issues

**Problem**: `mkdocs serve` shows errors
**Solution**: Check `mkdocs.yml` syntax with YAML linter

**Problem**: Examples don't execute
**Solution**: Check browser console for JavaScript errors

**Problem**: Doctest failures
**Solution**: Run `pytest --doctest-modules plotille/ -v` to see which tests fail

**Problem**: GitHub Pages 404
**Solution**: Verify gh-pages branch exists and contains built site

**Problem**: Custom domain not working
**Solution**: Check DNS propagation and CNAME file in gh-pages branch

**Problem**: Fonts not loading
**Solution**: Check network tab in browser DevTools, verify Google Fonts CDN accessible

---

## Testing Strategy for Each Phase

Follow Test-Driven Development:

1. **Unit tests first** - Write tests for utility functions
2. **Integration tests** - Test script end-to-end
3. **Manual testing** - Verify in browser
4. **Commit frequently** - After each passing test

### Example TDD Flow

```bash
# 1. Write test
echo "def test_new_feature(): assert False" >> tests/test_generate_docs.py

# 2. Run test (should fail)
pytest tests/test_generate_docs.py::test_new_feature -v

# 3. Implement feature
# ... edit code ...

# 4. Run test (should pass)
pytest tests/test_generate_docs.py::test_new_feature -v

# 5. Commit
git add -A
git commit -m "Add feature X with tests"
```

---

**End of Implementation Plan**

This plan provides complete step-by-step instructions for implementing the plotille documentation system. Follow each task sequentially, test thoroughly, and commit frequently. Good luck!
