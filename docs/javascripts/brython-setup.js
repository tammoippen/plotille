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

// Make runExample globally available
window.runExample = runExample;
