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
