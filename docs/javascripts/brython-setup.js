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
