# Implementation Plan Updates - Simplified CSS Approach

## Changes to Original Plan

This document updates `documentation-system-implementation.md` to reflect the simplified approach of using standard Material theme instead of custom amber phosphor CRT aesthetic.

---

## Phase 5: Terminal Window Styling (REVISED)

### Task 5.1: Create Minimal Terminal Window Styling (REPLACES OLD TASK 5.1)

**What:** Style only the terminal window components for interactive examples. Use standard Material theme for everything else.

**Files to create:**
- `docs/stylesheets/terminal.css` (minimal, ~120 lines)

**Actions:**

1. Create `docs/stylesheets/terminal.css`:

```css
/*
 * ABOUTME: Terminal window styling for plotille interactive examples.
 * ABOUTME: Uses standard Material theme for everything except terminal components.
 */

:root {
    --terminal-bg: #1e1e1e;
    --terminal-fg: #d4d4d4;
    --terminal-border: #3e3e3e;
    --terminal-header-bg: #2d2d2d;
    --terminal-button-bg: #0e639c;
    --terminal-button-hover: #1177bb;
}

.terminal-window {
    background: var(--terminal-bg);
    border: 1px solid var(--terminal-border);
    border-radius: 6px;
    margin: 1.5rem 0;
    overflow: hidden;
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
}

.terminal-header {
    background: var(--terminal-header-bg);
    padding: 0.5rem 1rem;
    border-bottom: 1px solid var(--terminal-border);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.terminal-title {
    color: var(--terminal-fg);
    font-size: 0.85rem;
    font-weight: 500;
}

.terminal-run-btn {
    background: var(--terminal-button-bg);
    color: #ffffff;
    border: none;
    padding: 0.25rem 0.75rem;
    border-radius: 3px;
    cursor: pointer;
    font-size: 0.85rem;
    font-weight: 500;
    transition: background 0.2s;
}

.terminal-run-btn:hover {
    background: var(--terminal-button-hover);
}

.terminal-body {
    padding: 1rem;
    background: var(--terminal-bg);
}

.code-editor-wrapper {
    border: 1px solid var(--terminal-border);
    border-radius: 4px;
    overflow: hidden;
}

.code-editor {
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    background: var(--terminal-bg);
    color: var(--terminal-fg);
    width: 100%;
    min-height: 300px;
    padding: 1rem;
    border: none;
    resize: vertical;
    line-height: 1.5;
    tab-size: 4;
}

.code-editor:focus {
    outline: none;
    box-shadow: 0 0 0 2px var(--terminal-button-bg);
}

.terminal-output {
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    color: var(--terminal-fg);
    white-space: pre-wrap;
    margin-top: 1rem;
    line-height: 1.4;
    max-height: 600px;
    overflow-y: auto;
}

.terminal-prompt {
    color: #4ec9b0;
    display: block;
    margin-bottom: 0.5rem;
}

.output-content {
    margin-top: 0.5rem;
}

.output-content.error {
    color: #f48771;
}

.hero-terminal {
    margin: 2rem 0;
}

.hero-plot {
    font-size: 0.75rem;
}
```

2. Update `mkdocs.yml` to use standard Material theme:

```yaml
site_name: plotille
site_url: https://plotille.tammo.io
site_description: Plot in the terminal using braille dots
site_author: Tammo Ippen
repo_url: https://github.com/tammoippen/plotille
repo_name: tammoippen/plotille

theme:
  name: material
  features:
    - content.code.copy
    - navigation.sections
    - navigation.top
    - search.suggest
    - search.highlight

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          options:
            docstring_style: google
            show_source: true
            show_signature_annotations: true
            separate_signature: true

markdown_extensions:
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.superfences
  - admonition
  - pymdownx.details

extra_css:
  - stylesheets/terminal.css

extra_javascript:
  - brython.js
  - brython_stdlib.js
  - ansi_up.js
  - javascripts/codemirror-setup.js
  - javascripts/brython-setup.js

nav:
  - Home: index.md
  - Cookbook:
      - Basic Plots: cookbook/basic.md
      - Advanced Examples: cookbook/advanced.md
```

3. Update `.gitignore`:

```gitignore
# Site build output
site/

# Documentation build artifacts
docs/Lib/
docs/assets/example-outputs/
```

4. Remove build artifacts from git:

```bash
git rm -r --cached docs/Lib/
git rm -r --cached docs/assets/example-outputs/
```

**Test:**
```bash
python scripts/generate_docs.py
mkdocs serve
# Visit http://127.0.0.1:8000
# Verify:
#   - Standard Material theme (clean, professional)
#   - Terminal windows look like terminals (dark, monospace)
#   - Everything readable and accessible
#   - Search works with default styling
#   - Code blocks use Material's syntax highlighting
```

**Commit:** `Add minimal terminal window styling with standard Material theme`

**Design Goals:**
- **Simplicity:** ~120 lines of CSS vs 547
- **Maintainability:** Only style what's necessary
- **Accessibility:** Use Material's tested, accessible defaults
- **Clarity:** Clear visual distinction between docs and terminals

---

### Task 5.2: REMOVED

Font bundling task is no longer needed - use system/browser default fonts via Material theme.

---

## Phase 10: Hero Animation (SIMPLIFIED)

### Task 10.1: SIMPLIFIED - Static Hero Plot

The original task included JavaScript animation. Simplified version:

**What:** Display a static plotille plot on the home page. No animation needed.

**This is already implemented** in `generate_home_page()` which generates the hero plot. The plot appears in the hero-terminal div which is styled by the minimal terminal.css.

**No additional work needed** for this task. The hero plot is generated during `python scripts/generate_docs.py` and displayed in a terminal window styled by terminal.css.

---

## Removed Sections

The following sections from the original plan are **NO LONGER NEEDED**:

### From Phase 5:
- ❌ All the "amber phosphor color palette" variables
- ❌ Global font imports (VT323, IBM Plex Mono)
- ❌ CRT scanline effects
- ❌ Global Material theme overrides
- ❌ Custom navigation styling
- ❌ Custom header styling
- ❌ Custom search styling
- ❌ Syntax highlighting overrides
- ❌ Admonition overrides

### From Phase 10:
- ❌ JavaScript hero animation (keep static plot)
- ❌ Character-by-character reveal animation
- ❌ `docs/javascripts/hero-animation.js` file

---

## What Stays the Same

These phases are **unchanged**:

- **Phase 1:** Project Setup & Dependencies ✓
- **Phase 2:** Example Analysis & Classification ✓
- **Phase 3:** Static Example Pre-rendering ✓
- **Phase 4:** Markdown Generation ✓
- **Phase 6:** Brython Integration ✓
- **Phase 7:** CodeMirror/Editor Enhancement ✓
- **Phase 8:** API Documentation ✓
- **Phase 9:** Navigation (already minimal) ✓
- **Phase 11:** GitHub Actions CI/CD ✓
- **Phase 12-14:** Testing, refinement, launch ✓

---

## Summary of Changes

**Philosophy Change:**
- **Old:** Custom amber phosphor CRT theme everywhere
- **New:** Standard Material theme, terminal styling only for terminals

**CSS Reduction:**
- **Old:** 547 lines of global overrides
- **New:** 120 lines of terminal-only styling

**Visual Design:**
- **Old:** Amber on black everywhere, CRT effects, custom fonts
- **New:** Material's defaults everywhere, terminal windows look like VS Code terminals

**Maintenance:**
- **Old:** Fight Material's updates, maintain custom syntax highlighting
- **New:** Ride Material's updates, zero maintenance on theme

**Benefits:**
- Simpler implementation
- Better readability
- More accessible
- Easier to maintain
- Faster page loads
- Professional appearance

**Trade-offs:**
- Less "unique" visual identity
- No retro CRT aesthetic

**Conclusion:** The simplified approach better serves the primary goal: **documenting plotille clearly and making it easy for users to try examples interactively.**
