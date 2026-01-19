#!/usr/bin/env python3
# ABOUTME: Generate documentation from examples.
# ABOUTME: Scans examples directory and classifies them by dependencies.

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
