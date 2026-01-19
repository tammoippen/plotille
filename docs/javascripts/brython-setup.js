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
            const scriptId = `brython-script-${exampleName}`;

            // Remove any existing script with this ID
            const existingScript = document.getElementById(scriptId);
            if (existingScript) {
                existingScript.remove();
            }

            // Wrap code with custom output capture (StringIO doesn't work in Brython)
            // Use exec() to avoid breaking Brython's execution context with indentation
            const wrappedCode = `
import sys

# Custom output capture class (Brython-compatible)
class OutputCapture:
    def __init__(self):
        self.output = []
    def write(self, text):
        self.output.append(text)
    def flush(self):
        pass
    def getvalue(self):
        return ''.join(self.output)

__output__ = OutputCapture()
__old_stdout__ = sys.stdout
sys.stdout = __output__

try:
    exec("""${code.replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/\n/g, '\\n')}""")
finally:
    sys.stdout = __old_stdout__
    print(__output__.getvalue(), end='')
`;

            // Create script element
            const script = document.createElement('script');
            script.type = 'text/python';
            script.id = scriptId;
            script.textContent = wrappedCode;

            // Capture console.log output
            window.__brython_output__ = '';
            const oldLog = console.log;
            console.log = function(...args) {
                window.__brython_output__ += args.join(' ') + '\n';
                oldLog.apply(console, args);
            };

            document.body.appendChild(script);

            // Run Brython on this specific script
            if (window.brython) {
                brython({debug: 1, ids: [scriptId]});
            }

            // Restore console.log immediately
            console.log = oldLog;

            // Wait for output capture
            setTimeout(() => {
                let output = window.__brython_output__;

                // Remove trailing newline added by our capture
                if (output && output.endsWith('\n')) {
                    output = output.slice(0, -1);
                }

                outputDiv.textContent = output || '(no output)';

                // Clean up
                const scriptToRemove = document.getElementById(scriptId);
                if (scriptToRemove) {
                    scriptToRemove.remove();
                }
                delete window.__brython_output__;
            }, 150);

        } catch (error) {
            // Display error
            outputDiv.classList.add('error');
            outputDiv.textContent = `Error: ${error.message}`;
            console.error('Brython execution error:', error);
        }
    }, 10);
}

// Make runExample globally available
window.runExample = runExample;
