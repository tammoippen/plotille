# Documentation Implementation Review

## Overall Assessment

Excellent progress on Tasks 4.2, 4.3, and 5.1! The structure is solid and the amber phosphor theme foundation is in place. However, there are several issues that need to be addressed before proceeding to the next phase.

**Dev server is running at:** http://127.0.0.1:8000

---

## Critical Issues (Must Fix Before Proceeding)

### 1. Color Contrast Problems - CRITICAL ❌

**Issue:** The current color scheme has severe readability issues:
- White/light text on yellow backgrounds is not readable
- H1 headers appear to have black font with yellow shadow/glow, making them unreadable
- Material theme overrides are creating poor contrast combinations

**Root Cause:** The CSS is setting Material theme primary colors to amber, which Material then uses for backgrounds in some components. This creates amber-on-amber or light-on-amber combinations.

**Fix Required in `docs/stylesheets/terminal.css`:**

```css
/* Global overrides for Material theme */
[data-md-color-scheme="plotille"] {
    /* Keep amber for accents, but use proper backgrounds */
    --md-primary-fg-color: var(--amber-base);
    --md-primary-fg-color--light: var(--amber-bright);
    --md-primary-fg-color--dark: var(--amber-dim);
    --md-accent-fg-color: var(--amber-bright);

    /* Force dark backgrounds with amber text */
    --md-default-bg-color: var(--amber-black);
    --md-default-fg-color: var(--amber-base);
    --md-code-bg-color: var(--amber-dark);
    --md-code-fg-color: var(--amber-base);

    /* Add these to prevent light backgrounds */
    --md-typeset-a-color: var(--amber-bright);
    --md-typeset-color: var(--amber-base);
}

/* Ensure headers are always readable */
h1, h2, h3, h4, h5, h6 {
    font-family: 'VT323', monospace;
    color: var(--amber-bright) !important;
    background: transparent !important;
    text-shadow: 0 0 8px var(--amber-glow);
    letter-spacing: 0.05em;
}

/* Force main content area to be dark */
.md-main,
.md-content,
.md-content__inner {
    background-color: var(--amber-black) !important;
    color: var(--amber-base) !important;
}

/* Ensure sidebar is dark */
.md-sidebar {
    background-color: var(--amber-black) !important;
}

/* Links should be bright amber and underlined for visibility */
a {
    color: var(--amber-bright) !important;
    text-decoration: underline;
}

a:hover {
    color: var(--amber-bright) !important;
    text-shadow: 0 0 10px var(--amber-glow);
}
```

**Test:** After applying, verify that:
- All text is readable (amber on black, never black on amber)
- Headers are bright amber with glow effect
- No white or light backgrounds appear anywhere
- Links are clearly visible

---

### 2. `__init__.py` Being Treated as Example ❌

**Issue:** The file `examples/__init__.py` is being processed and appears in `basic.md` as "## __init__" with empty content.

**Fix Required in `scripts/generate_docs.py`:**

In the `main()` function, modify the loop to skip `__init__.py`:

```python
# Analyze all Python files
examples = []
for example_file in sorted(examples_dir.glob("*.py")):
    # Skip __init__.py files
    if example_file.name == "__init__.py":
        continue
    info = analyze_example(example_file)
    examples.append(info)
```

**Test:** Run `python scripts/generate_docs.py` and verify `__init__` no longer appears in `docs/cookbook/basic.md`.

---

### 3. Performance Example Should Not Be in Cookbook ❌

**Issue:** `performance_example.py` appears in `basic.md` but it's not a useful example for users - it's for internal performance testing.

**Fix Required in `scripts/generate_docs.py`:**

Add performance examples to the skip list:

```python
# Analyze all Python files
examples = []
SKIP_EXAMPLES = {"__init__.py", "performance_example.py"}

for example_file in sorted(examples_dir.glob("*.py")):
    # Skip files that aren't user-facing examples
    if example_file.name in SKIP_EXAMPLES:
        continue
    info = analyze_example(example_file)
    examples.append(info)
```

**Test:** Verify `performance_example` no longer appears in the generated cookbook pages.

---

### 4. License Headers in Examples ❌

**Issue:** All examples include the full MIT license header (23 lines), which clutters the documentation. Users don't need to see this in the browser.

**Fix Required in `scripts/generate_docs.py`:**

Add a function to strip license headers:

```python
def strip_license_header(source_code: str) -> str:
    """
    Remove MIT license header from source code.

    Args:
        source_code: Python source code possibly containing license header

    Returns:
        Source code with license header removed
    """
    lines = source_code.split('\n')

    # Look for MIT license pattern
    if '# The MIT License' in source_code:
        # Find the end of the license block (first non-comment/non-blank line after license)
        in_license = False
        start_index = 0

        for i, line in enumerate(lines):
            stripped = line.strip()

            # Start of license
            if 'MIT License' in line:
                in_license = True
                start_index = i
                continue

            # End of license block (first non-comment, non-blank line)
            if in_license and stripped and not stripped.startswith('#'):
                # Remove everything from start_index to just before this line
                return '\n'.join(lines[i:])

        # If we didn't find the end, remove first 23 lines (typical license length)
        if in_license:
            return '\n'.join(lines[23:])

    return source_code
```

Then update `generate_interactive_example_markdown()` and `generate_static_example_markdown()`:

```python
def generate_interactive_example_markdown(info: ExampleInfo) -> str:
    """Generate markdown for an interactive example."""
    source_code = info.path.read_text()

    # Strip license header
    source_code = strip_license_header(source_code)

    # Escape backticks in code for markdown
    escaped_code = source_code.replace("```", "\\`\\`\\`")

    # ... rest of function ...
```

```python
def generate_static_example_markdown(info: ExampleInfo, output_path: Path) -> str:
    """Generate markdown for a static example with pre-rendered output."""
    source_code = info.path.read_text()

    # Strip license header
    source_code = strip_license_header(source_code)

    # Read pre-rendered output
    # ... rest of function ...
```

**Test:** Verify examples in cookbook pages start with `import` statements, not license headers.

---

### 5. Hero Plot is Empty ❌

**Issue:** The home page has `<pre class="hero-plot" id="hero-animation"></pre>` but it's empty. According to the plan (Task 10.1), the hero should display an actual plotille sine wave.

**Fix Required in `scripts/generate_docs.py`:**

Add the `generate_hero_plot()` function:

```python
def generate_hero_plot() -> str:
    """
    Generate a sample plot for the hero animation.

    Returns:
        String containing plotille plot output
    """
    try:
        import plotille
        import math

        X = [i / 10 for i in range(-31, 32)]
        Y = [math.sin(x) for x in X]

        plot_output = plotille.plot(
            X, Y,
            width=60,
            height=10,
            X_label='X',
            Y_label='',
        )

        return plot_output
    except Exception as e:
        # Fallback if generation fails
        return f"Error generating plot: {e}"
```

Then update `generate_home_page()`:

```python
def generate_home_page(docs_dir: Path) -> Path:
    """Generate the home/index page."""
    # Generate the hero plot
    hero_plot = generate_hero_plot()

    # Change to f-string to include hero_plot
    content = f"""# plotille

<div class="hero-terminal">
    <div class="terminal-header">
        <span class="terminal-title">[root@plotille ~]$</span>
    </div>
    <div class="terminal-body">
        <pre class="hero-plot" id="hero-animation">{hero_plot}</pre>
    </div>
</div>

Plot in the terminal using braille dots, with no dependencies.

## Features

- **Scatter plots, line plots, histograms** - Basic plotting functions
- **Complex figures** - Compose multiple plots with legends
- **Canvas drawing** - Direct pixel manipulation for custom visualizations
- **Image rendering** - Display images using braille dots or background colors
- **Color support** - Multiple color modes: names, byte values, RGB
- **No dependencies** - Pure Python with no external requirements

## Quick Start

Install plotille:

```bash
pip install plotille
```

Create your first plot:

```python
import plotille
import math

X = [i/10 for i in range(-30, 30)]
Y = [math.sin(x) for x in X]

print(plotille.plot(X, Y, height=20, width=60))
```

## Explore

Browse the [cookbook](cookbook/basic.md) to see interactive examples you can edit and run in your browser.

"""

    index_file = docs_dir / "index.md"
    index_file.write_text(content)
    return index_file
```

**Test:** Verify home page shows a sine wave plot in the hero terminal.

---

### 6. Navigation Incomplete ⚠️

**Issue:** `mkdocs.yml` only lists `- Home: index.md`. The cookbook pages should be in the navigation.

**Fix Required in `mkdocs.yml`:**

Update the `nav` section:

```yaml
nav:
  - Home: index.md
  - Cookbook:
      - Basic Plots: cookbook/basic.md
      - Advanced Examples: cookbook/advanced.md
```

**Note:** Only `basic` and `advanced` categories exist because no examples matched `figures` or `canvas` patterns. This is correct behavior based on the current examples.

**Test:** Verify navigation sidebar shows Home and Cookbook sections.

---

## Expected Issue (Not Yet Implemented)

### 7. `runExample is not defined` Error ✓ Expected

**Issue:** Clicking `[EXEC]` buttons in examples shows:
```
Uncaught ReferenceError: runExample is not defined
```

**Reason:** This is expected! Brython integration (Phase 6) hasn't been implemented yet. The HTML structure is in place, but the JavaScript to make it work comes in Tasks 6.1-6.2 and Task 7.2.

**Do NOT fix this yet.** This will be handled in:
- Task 6.1: Add Brython runtime and setup JavaScript
- Task 7.2: Implement proper Brython execution with output capture

**For now:** The buttons are non-functional, which is correct for this stage.

---

## How to Apply Fixes

### Step 1: Update `scripts/generate_docs.py`

Apply fixes for issues #2, #3, #4, and #5:

1. Add `strip_license_header()` function
2. Update example loop to skip `__init__.py` and `performance_example.py`
3. Update both markdown generation functions to call `strip_license_header()`
4. Add `generate_hero_plot()` function
5. Update `generate_home_page()` to use `generate_hero_plot()` and f-strings

### Step 2: Update `docs/stylesheets/terminal.css`

Apply fix for issue #1 (color contrast):

1. Add `!important` to critical background/foreground rules
2. Add explicit rules for `.md-main`, `.md-content`, `.md-sidebar`
3. Fix link styling for visibility
4. Ensure headers always have proper contrast

### Step 3: Update `mkdocs.yml`

Apply fix for issue #6 (navigation):

1. Add Cookbook section with basic and advanced pages

### Step 4: Regenerate and Test

```bash
# Regenerate documentation with all fixes
python scripts/generate_docs.py

# Verify changes
cat docs/index.md | grep "hero-plot"  # Should contain plot output
grep -c "MIT License" docs/cookbook/basic.md  # Should be 0
grep -c "__init__" docs/cookbook/basic.md  # Should be 0
grep -c "performance_example" docs/cookbook/basic.md  # Should be 0

# Check site in browser (server should auto-reload)
# Visit http://127.0.0.1:8000
```

### Step 5: Commit

```bash
git add scripts/generate_docs.py docs/ mkdocs.yml
git commit -m "Fix color contrast, filter unwanted examples, add hero plot, update nav"
```

---

## Testing Checklist

After applying all fixes, verify in browser at http://127.0.0.1:8000:

### Color & Contrast
- [ ] All text is readable (amber on black throughout)
- [ ] Headers are bright amber, clearly visible
- [ ] No white or light backgrounds anywhere
- [ ] Links are underlined and bright amber
- [ ] Terminal windows have proper amber/black contrast
- [ ] Sidebar is dark with amber text

### Content
- [ ] Home page shows sine wave plot in hero terminal
- [ ] No `__init__` example in basic cookbook
- [ ] No `performance_example` in basic cookbook
- [ ] Examples start with imports, not license headers
- [ ] Navigation shows "Home" and "Cookbook" sections
- [ ] Cookbook has "Basic Plots" and "Advanced Examples" pages

### Expected Non-Working Features (OK for now)
- [ ] `[EXEC]` buttons show "runExample is not defined" error (expected - will be fixed in Phase 6)

---

## Summary

**Total fixes needed:** 6 critical issues

**Files to modify:**
1. `scripts/generate_docs.py` - Issues #2, #3, #4, #5
2. `docs/stylesheets/terminal.css` - Issue #1
3. `mkdocs.yml` - Issue #6

**Estimated time:** 30-45 minutes

Once these fixes are applied and tested, you're ready to proceed with **Phase 6: Brython Integration** (Tasks 6.1-6.2) which will make the `[EXEC]` buttons functional.

Great work so far! The foundation is solid - these are just refinements to get the styling and content filtering right before moving forward.
