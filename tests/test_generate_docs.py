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


def test_generate_interactive_example_markdown(tmp_path):
    """Test generating markdown for interactive example."""
    from pathlib import Path

    # Create actual test file
    test_py = tmp_path / "test.py"
    test_py.write_text('print("hi")')

    info = generate_docs.ExampleInfo(
        path=test_py,
        name="test",
        description="Test example",
        imports={"plotille"},
        is_interactive=True,
    )

    markdown = generate_docs.generate_interactive_example_markdown(info)

    assert "## test" in markdown
    assert "Test example" in markdown
    assert "interactive-example" in markdown
    assert 'print("hi")' in markdown


def test_generate_static_example_markdown(tmp_path):
    """Test generating markdown for static example."""
    from pathlib import Path
    import unittest.mock as mock

    # Create actual test files
    test_py = tmp_path / "test.py"
    test_py.write_text('print("hi")')

    info = generate_docs.ExampleInfo(
        path=test_py,
        name="test",
        description="Test example",
        imports={"plotille", "numpy"},
        is_interactive=False,
    )

    # Create mock output file
    output_path = tmp_path / "test.txt"
    output_path.write_text("Example output here")

    markdown = generate_docs.generate_static_example_markdown(info, output_path)

    assert "## test" in markdown
    assert "Test example" in markdown
    assert "numpy" in markdown
    assert "Example output here" in markdown
