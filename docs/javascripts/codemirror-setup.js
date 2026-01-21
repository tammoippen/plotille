/**
 * Textarea enhancement for plotille documentation.
 *
 * Enhances textarea elements with monospace font and tab key support.
 * Note: Full CodeMirror integration skipped per YAGNI principle.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Find all code editor textareas
    const editors = document.querySelectorAll('.code-editor');

    editors.forEach(textarea => {
        const editorId = textarea.id;

        // Style the textarea
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
