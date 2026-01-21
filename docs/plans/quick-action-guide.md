# Quick Action Guide - CSS Simplification

## Goal
Replace custom amber phosphor theme with standard Material theme + minimal terminal styling.

---

## Step 1: Replace terminal.css (5 minutes)

**Delete everything** in `docs/stylesheets/terminal.css` and replace with:

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

**Result:** 120 lines instead of 547. Only terminal styling, no global overrides.

---

## Step 2: Update mkdocs.yml (2 minutes)

Find and **remove** any of these if present:
- `custom_dir: docs/overrides` (only if overrides was just for theme)
- `palette.scheme: plotille`
- Any custom color palette definitions

Ensure it looks like:

```yaml
theme:
  name: material
  features:
    - content.code.copy
    - navigation.sections
    - navigation.top
    - search.suggest
    - search.highlight

# Keep only terminal.css
extra_css:
  - stylesheets/terminal.css
```

---

## Step 3: Update .gitignore (1 minute)

Add these lines:

```gitignore
# Documentation build artifacts
docs/Lib/
docs/assets/example-outputs/
```

---

## Step 4: Remove build artifacts from git (2 minutes)

```bash
git rm -r --cached docs/Lib/
git rm -r --cached docs/assets/example-outputs/
```

---

## Step 5: Test (2 minutes)

```bash
python scripts/generate_docs.py
make doc-serve
```

Open http://127.0.0.1:8000

**What you should see:**
- ✅ Standard Material theme (light/dark based on system preference)
- ✅ Normal navigation, search, everything works
- ✅ Terminal windows in cookbook pages look like VS Code terminals
- ✅ Everything is readable
- ✅ No amber glow, no scanlines, no custom fonts everywhere

---

## Step 6: Commit (1 minute)

```bash
git add .
git commit -m "Simplify to standard Material theme with minimal terminal styling"
```

---

## Total Time: ~15 minutes

## Expected Outcome

**Before:**
- Custom amber phosphor theme everywhere
- 547 lines of CSS fighting Material
- Readability issues
- Build artifacts in git

**After:**
- Standard Material theme (professional, accessible)
- 120 lines of CSS (only for terminals)
- Perfect readability
- Clean git repository

## What If Something Breaks?

**Problem:** Terminal windows don't render
**Solution:** Check that markdown templates in `scripts/generate_docs.py` use the class names: `terminal-window`, `terminal-header`, `terminal-body`, `code-editor`, `terminal-output`

**Problem:** mkdocs build fails
**Solution:** Check `mkdocs.yml` syntax, ensure all required plugins are installed

**Problem:** Examples don't execute
**Solution:** This is unrelated to CSS - check Brython setup in `docs/javascripts/`

---

## Questions?

See detailed docs:
- `docs/plans/css-simplification-plan.md` - Full explanation
- `docs/plans/implementation-plan-updates.md` - How this changes original plan
