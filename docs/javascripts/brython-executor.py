# ABOUTME: Python code executed in browser via Brython for running examples.
# ABOUTME: Provides run_code() function callable from JavaScript.

import sys
import traceback

from browser import document, window


class OutputCapture:
    """Capture stdout output in a Brython-compatible way."""

    def __init__(self):
        self.output = []

    def write(self, text):
        self.output.append(str(text))

    def flush(self):
        pass

    def isatty(self):
        return True  # Pretend we're a TTY to enable colors

    def getvalue(self):
        return "".join(self.output)


def run_code(code, output_element_id):
    """
    Execute Python code and display output.

    Args:
        code: Python code string to execute
        output_element_id: ID of DOM element to write output to
    """
    output_elem = document[output_element_id]

    if not output_elem:
        print(f"Error: Output element {output_element_id} not found")
        return

    # Clear previous output
    output_elem.text = ""
    output_elem.classList.remove("error")

    # Show running indicator
    output_elem.text = "Running..."

    # Capture stdout
    capture = OutputCapture()
    old_stdout = sys.stdout
    sys.stdout = capture

    try:
        # Execute the user's code
        exec(code, {"__name__": "__main__"})

        # Get captured output
        raw_output = capture.getvalue()

        # Convert ANSI codes to HTML if AnsiUp is available
        if raw_output:
            if window.ansiUpConverter:
                html_output = window.ansiUpConverter.ansi_to_html(raw_output)
                output_elem.innerHTML = html_output
            else:
                output_elem.text = raw_output
        else:
            output_elem.text = "(no output)"

    except Exception as e:
        # Display error
        output_elem.classList.add("error")
        error_msg = f"Error: {e}\n\n{traceback.format_exc()}"
        output_elem.text = error_msg

    finally:
        # Restore stdout
        sys.stdout = old_stdout


# Make run_code available to JavaScript
window.pythonRunCode = run_code
