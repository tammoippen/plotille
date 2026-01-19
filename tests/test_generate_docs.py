"""Tests for documentation generation script."""
import sys
from pathlib import Path

# Add scripts to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import generate_docs


def test_extract_imports_simple() -> None:
    """Test extracting imports from simple code."""
    code = "import numpy\nimport plotille"
    imports = generate_docs.extract_imports(code)
    assert imports == {"numpy", "plotille"}


def test_extract_imports_from() -> None:
    """Test extracting from-imports."""
    code = "from PIL import Image"
    imports = generate_docs.extract_imports(code)
    assert imports == {"PIL"}


def test_extract_description_docstring() -> None:
    """Test extracting description from docstring."""
    code = '"""This is a test"""\nprint("hi")'
    desc = generate_docs.extract_description(code)
    assert desc == "This is a test"


def test_extract_description_comment() -> None:
    """Test extracting description from comment."""
    code = "# This is a comment\nprint('hi')"
    desc = generate_docs.extract_description(code)
    assert desc == "This is a comment"


def test_is_interactive_pure() -> None:
    """Test interactive detection for pure plotille."""
    imports = {"plotille", "math", "random"}
    assert generate_docs.is_interactive(imports) is True


def test_is_interactive_numpy() -> None:
    """Test interactive detection with numpy."""
    imports = {"plotille", "numpy"}
    assert generate_docs.is_interactive(imports) is False


def test_is_interactive_pillow() -> None:
    """Test interactive detection with PIL."""
    imports = {"PIL", "plotille"}
    assert generate_docs.is_interactive(imports) is False


def test_categorize_basic() -> None:
    """Test basic example categorization."""
    from pathlib import Path

    info = generate_docs.ExampleInfo(
        Path("scatter.py"), "scatter", "", {"plotille"}, True
    )
    assert generate_docs.categorize_example(info) == "basic"


def test_categorize_canvas() -> None:
    """Test canvas example categorization."""
    from pathlib import Path

    info = generate_docs.ExampleInfo(
        Path("canvas_test.py"), "canvas_test", "", {"plotille"}, True
    )
    assert generate_docs.categorize_example(info) == "canvas"


def test_categorize_advanced() -> None:
    """Test advanced example categorization."""
    from pathlib import Path

    info = generate_docs.ExampleInfo(
        Path("image.py"), "image", "", {"PIL", "plotille"}, False
    )
    assert generate_docs.categorize_example(info) == "advanced"
