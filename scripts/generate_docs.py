#!/usr/bin/env python3
# ABOUTME: Generate documentation from examples.
# ABOUTME: Scans examples directory and classifies them by dependencies.

import ast
import subprocess
import sys
from dataclasses import dataclass
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
                imports.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split(".")[0])

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
            return docstring.strip().split("\n")[0]  # First line only
    except SyntaxError:
        pass

    # Fall back to first comment
    lines = source_code.split("\n")
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
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
    blocked_modules = {"numpy", "PIL", "pandas", "matplotlib", "scipy"}

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
        is_interactive=is_interactive(imports),
    )


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
    if "canvas" in name_lower or "draw" in name_lower:
        return "canvas"

    # Figure examples (multi-plot)
    if "figure" in name_lower or "subplot" in name_lower:
        return "figures"

    # Advanced (external deps or complex)
    if not info.is_interactive or "image" in name_lower or "img" in name_lower:
        return "advanced"

    # Default to basic
    return "basic"


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
    escaped_code = source_code.replace("```", "\\`\\`\\`")

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

    deps = ", ".join(sorted(info.imports - {"plotille"}))

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
        "basic": "Basic Plots",
        "figures": "Complex Figures",
        "canvas": "Canvas Drawing",
        "advanced": "Advanced Examples",
    }

    title = category_titles.get(category, category.title())

    # Build page content
    content = [f"# {title}\n"]

    # Add description
    descriptions = {
        "basic": "Simple plotting examples to get started with plotille.",
        "figures": "Multi-plot figures and complex visualizations.",
        "canvas": "Direct canvas manipulation for custom drawings.",
        "advanced": "Examples using external libraries like NumPy and Pillow.",
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
    output_file.write_text("\n".join(content))

    return output_file


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


if __name__ == "__main__":
    sys.exit(main())
