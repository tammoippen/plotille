/**
 * Brython setup and initialization for plotille documentation.
 */

// Track if Brython is ready
let brythonReady = false;

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

    // Wait for Python executor to be ready
    const checkReady = setInterval(() => {
        if (window.pythonRunCode) {
            brythonReady = true;
            clearInterval(checkReady);
            console.log('Brython initialized and executor ready');
        }
    }, 50);

    // Timeout after 5 seconds
    setTimeout(() => {
        if (!brythonReady) {
            clearInterval(checkReady);
            console.error('Brython executor not ready after 5 seconds');
        }
    }, 5000);
});

/**
 * Execute Python code in an example.
 *
 * @param {string} exampleName - Name of the example to run
 */
function runExample(exampleName) {
    const editor = document.getElementById(`editor-${exampleName}`);
    const outputContainer = document.getElementById(`output-${exampleName}`);
    const outputContent = outputContainer ? outputContainer.querySelector('.output-content') : null;

    if (!editor || !outputContent) {
        console.error(`Example ${exampleName} not found`);
        return;
    }

    // Check if Brython executor is ready
    if (!brythonReady || !window.pythonRunCode) {
        outputContent.textContent = 'Brython not ready yet...';
        outputContent.classList.add('error');
        console.error('Brython executor not ready');
        return;
    }

    const code = editor.value;

    // Give the output content div an ID if it doesn't have one
    if (!outputContent.id) {
        outputContent.id = `output-content-${exampleName}`;
    }

    // Call the Python function to execute the code
    // It will handle output capture and display
    try {
        window.pythonRunCode(code, outputContent.id);
    } catch (error) {
        outputContent.classList.add('error');
        outputContent.textContent = `Error: ${error.message}`;
        console.error('Brython execution error:', error);
    }
}

// Make runExample globally available
window.runExample = runExample;
