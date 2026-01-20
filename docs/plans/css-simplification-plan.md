# CSS Simplification Plan - Return to Standard Material Theme

## Philosophy

**Old approach (wrong):** Override everything with amber phosphor CRT aesthetic
**New approach (correct):** Use Material's default theme, style only terminal windows

**Principle:** The documentation is standard Material. The interactive examples are terminal windows. That's the only distinction.

---

## Step 1: Create Minimal terminal.css

Replace the entire `docs/stylesheets/terminal.css` with this minimal version:

```css
/*
 * ABOUTME: Terminal window styling for plotille interactive examples.
 * ABOUTME: Uses standard Material theme for everything except terminal components.
 */

/* Terminal window components only - no global overrides */

:root {
    /* Terminal-specific colors (not site-wide) */
    --terminal-bg: #1e1e1e;
    --terminal-fg: #d4d4d4;
    --terminal-border: #3e3e3e;
    --terminal-header-bg: #2d2d2d;
    --terminal-button-bg: #0e639c;
    --terminal-button-hover: #1177bb;
}

/* Terminal window structure */
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

/* Code editor (textarea) */
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

/* Terminal output */
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
    color: #4ec9b0; /* Teal for prompt */
    display: block;
    margin-bottom: 0.5rem;
}

.output-content {
    margin-top: 0.5rem;
}

.output-content.error {
    color: #f48771; /* Soft red for errors */
}

/* Hero terminal on home page */
.hero-terminal {
    margin: 2rem 0;
}

.hero-plot {
    font-size: 0.75rem;
}
```

**That's it. 120 lines total. No global overrides.**

---

## Step 2: Update mkdocs.yml

Remove custom theme configuration, use Material defaults:

```yaml
site_name: plotille
site_url: https://plotille.tammo.io
site_description: Plot in the terminal using braille dots
site_author: Tammo Ippen
repo_url: https://github.com/tammoippen/plotille
repo_name: tammoippen/plotille

theme:
  name: material
  # Remove: custom_dir, palette.scheme overrides
  # Keep only essential features
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

# Only load minimal terminal CSS
extra_css:
  - stylesheets/terminal.css

# Keep Brython and scripts
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

---

## Step 3: Remove Unnecessary Files

**Delete these (if they exist):**
- `docs/overrides/` (if only used for theme overrides, not Brython)

**Keep:**
- `docs/overrides/main.html` if it contains Brython executor (check first)

**Update `.gitignore`:**

```gitignore
# Site build output
site/

# Documentation build artifacts
docs/Lib/
docs/assets/example-outputs/
```

---

## Step 4: Clean Git History

Remove build artifacts from git:

```bash
# Remove tracked build artifacts
git rm -r --cached docs/Lib/
git rm -r --cached docs/assets/example-outputs/

# Commit the cleanup
git add .gitignore
git commit -m "Remove build artifacts and simplify CSS to standard Material theme"
```

---

## Step 5: Test the Simplified Version

```bash
# Rebuild docs
python scripts/generate_docs.py

# Serve and check
make doc-serve
```

**What you should see:**
- Standard Material theme (light or dark based on system preference)
- Normal readable text, standard colors
- Navigation works normally
- Search works normally
- Code blocks use Material's syntax highlighting
- Terminal windows (interactive examples) look like actual terminals (dark with monospace)
- Clear visual distinction: "this is a terminal" vs "this is documentation"

---

## What Gets Removed vs What Stays

### ❌ REMOVE (was in old terminal.css):
- All global color overrides (`[data-md-color-scheme="plotille"]`)
- Global font changes (VT323, IBM Plex Mono everywhere)
- CRT scanline effects
- Phosphor glow effects
- Global text shadows
- Navigation styling overrides
- Header styling overrides
- Search results styling overrides
- Code block syntax highlighting overrides (use Material's defaults)
- Admonition overrides
- Link color overrides
- Sidebar overrides

### ✅ KEEP (in new terminal.css):
- `.terminal-window` structure
- `.terminal-header` styling
- `.terminal-title` styling
- `.terminal-run-btn` styling
- `.terminal-body` styling
- `.code-editor` textarea styling
- `.terminal-output` styling
- `.terminal-prompt` styling
- `.hero-terminal` styling (if kept on home page)

---

## Updated Implementation Plan - Phase 5

Replace the old Task 5.1 with this:

### Task 5.1: Create Minimal Terminal Window Styling

**What:** Style only the terminal window components for interactive examples.

**Files to create:**
- `docs/stylesheets/terminal.css`

**Actions:**

1. Create `docs/stylesheets/terminal.css` with minimal terminal-only styling (see Step 1 above)

2. Update `mkdocs.yml` to use standard Material theme (see Step 2 above)

**Philosophy:**
- Use Material's defaults for everything
- Only style terminal windows to look like actual terminals
- No global theme overrides
- No custom fonts site-wide
- No special effects (scanlines, glows, etc.)

**Visual design:**
- Documentation: Standard Material theme (clean, professional, readable)
- Terminal windows: Dark background (#1e1e1e), light text (#d4d4d4), monospace font
- Clear visual separation between docs and interactive code

**Test:**
```bash
mkdocs serve
# Visit http://127.0.0.1:8000
# Verify:
#   - Standard Material theme throughout
#   - Terminal windows look distinct (dark, monospace)
#   - Everything is readable
#   - No custom colors bleeding into navigation/search/etc.
```

**Commit:** `Add minimal terminal window styling`

---

## Benefits of This Approach

**Readability:**
- Material's theme is professionally designed and tested
- High contrast, accessible colors
- No custom syntax highlighting to maintain

**Maintainability:**
- 120 lines of CSS vs 547 lines
- Only terminal components, easy to understand
- No fighting with Material's defaults
- Easy to update when Material releases new versions

**Performance:**
- No global overrides means faster rendering
- No complex animations or effects
- Smaller CSS file

**User Experience:**
- Familiar documentation UI (Material is widely used)
- Clear distinction: "I'm reading docs" vs "I'm in a terminal"
- No accessibility issues from custom color schemes

**Development:**
- Easier to debug
- Material's theme switcher works (light/dark mode)
- Search, navigation, all features work as designed

---

## Migration Checklist

- [ ] Create new minimal `docs/stylesheets/terminal.css` (120 lines)
- [ ] Update `mkdocs.yml` to remove custom theme config
- [ ] Add `docs/Lib/` and `docs/assets/example-outputs/` to `.gitignore`
- [ ] Run `git rm -r --cached` on build artifacts
- [ ] Delete old 547-line terminal.css
- [ ] Test locally: `make doc-serve`
- [ ] Verify terminal windows still look good
- [ ] Verify Material theme works everywhere else
- [ ] Commit: "Simplify to standard Material theme with minimal terminal styling"

---

## Result

**Before:** Custom amber phosphor theme everywhere, 547 lines of CSS, readability issues
**After:** Standard Material theme, 120 lines of CSS for terminal windows only, clean and readable

The documentation looks professional. The terminal windows look like terminals. No confusion, no maintenance burden.
