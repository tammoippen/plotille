# Phase 6-7 Implementation Review

## Overall Assessment

Good progress on Tasks 5.2-7.1, but there are **critical bugs** that prevent the documentation from building, plus the Brython implementation needs completion of Task 7.2. The infrastructure is mostly in place but needs fixes before it can work.

**Current Status:**
- ✅ Task 5.2: Font bundling skipped (correct per YAGNI)
- ✅ Task 6.1: Brython runtime added
- ✅ Task 6.2: Plotille source copied successfully
- ✅ Task 7.1: Textarea enhancement added
- ❌ Task 7.2: **NOT COMPLETED** - This is required for Brython to actually work

---

## Critical Issues (Build-Breaking)

### 1. Documentation Build Crashes ❌ **CRITICAL**

**Issue:** Running `python scripts/generate_docs.py` crashes with:
```
IsADirectoryError: [Errno 21] Is a directory: '.'
```

**Root Cause:** When static examples fail to execute (because numpy/PIL aren't installed), they don't get added to `output_paths` dict. Then `generate_category_page()` calls:
```python
output_path = output_paths.get(info.name, Path())
```

This returns `Path()` which is `.` (current directory). Later, `generate_static_example_markdown()` checks:
```python
if output_path.exists():
    output = output_path.read_text()
```

`Path('.')` exists (as a directory), so it tries to read a directory as a file → crash.

**Fix Required in `scripts/generate_docs.py`:**

Change `generate_category_page()`:

```python
def generate_category_page(
    category: str,
    examples: list[ExampleInfo],
    output_paths: dict[str, Path],
    docs_dir: Path,
) -> Path:
    """Generate a markdown page for a category of examples."""
    # ... existing code ...

    # Add each example
    for info in examples:
        if info.is_interactive:
            markdown = generate_interactive_example_markdown(info)
        else:
            # FIX: Pass None if output doesn't exist, not Path()
            output_path = output_paths.get(info.name)  # Returns None if not found
            markdown = generate_static_example_markdown(info, output_path)

        content.append(markdown)

    # ... rest of function ...
```

And update `generate_static_example_markdown()`:

```python
def generate_static_example_markdown(
    info: ExampleInfo,
    output_path: Path | None,  # Allow None
) -> str:
    """Generate markdown for a static example with pre-rendered output."""
    source_code = info.path.read_text()

    # Strip license header
    source_code = strip_license_header(source_code)

    # Read pre-rendered output
    # FIX: Check for None and valid file
    if output_path and output_path.is_file():
        output = output_path.read_text()
    else:
        output = "Output not available (dependencies not installed during build)"

    deps = ", ".join(sorted(info.imports - {"plotille"}))

    # ... rest of function ...
```

**Test:**
```bash
python scripts/generate_docs.py
# Should complete without errors
```

---

## Major Issues (Functionality Broken)

### 2. Task 7.2 Not Completed ⚠️ **REQUIRED**

**Issue:** The current `runExample()` function in `brython-setup.js` uses incorrect Brython API and won't work properly:

```javascript
// Current implementation (from Task 6.1) - INCORRECT:
window.__BRYTHON__.python_to_js(code);  // This API doesn't exist
const result = eval(window.__BRYTHON__.imported['__main__']);  // Wrong approach
```

**Impact:** Clicking `[EXEC]` buttons will either:
- Do nothing
- Show errors
- Not capture output correctly

**What's Missing:** Task 7.2 in the implementation plan specifies a completely different approach that:
- Creates a `<script type="text/python">` element
- Uses `brython({ids: [script.id]})` to execute it
- Properly captures stdout via StringIO wrapper
- Shows "Running..." indicator

**Fix Required:**

Follow Task 7.2 in `docs/plans/documentation-system-implementation.md` (lines 1859-1975).

Replace the `runExample()` function in `docs/javascripts/brython-setup.js` with the version specified in Task 7.2.

**Key differences in Task 7.2 version:**
1. Wraps code with stdout redirection to StringIO
2. Creates script element dynamically
3. Uses proper Brython execution: `brython({debug: 1, ids: [script.id]})`
4. Captures output via console.log monkey-patching
5. Cleans up script element after execution
6. Shows "Running..." indicator during execution

**Test after fix:**
1. Visit http://127.0.0.1:8000/test-brython/
2. Click `[RUN]` button
3. Should see "Hello from Brython!" and "4" in output
4. Visit cookbook pages and test plotille examples

---

### 3. CodeMirror Check is Misleading ⚠️

**Issue:** In `docs/javascripts/codemirror-setup.js`:

```javascript
if (typeof CodeMirror === 'undefined') {
    console.error('CodeMirror not loaded');
    return;
}
```

But CodeMirror is **not** being loaded (per Task 7.1's YAGNI decision). This check will always fail and print an error, making it look like something is broken when it's actually working as intended.

**Fix Required in `docs/javascripts/codemirror-setup.js`:**

Remove the CodeMirror check entirely:

```javascript
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
```

**Test:** Check browser console - should not show "CodeMirror not loaded" error.

---

### 4. Test Page in Navigation ⚠️

**Issue:** `test-brython.md` is in the main navigation at `mkdocs.yml`:

```yaml
nav:
  - Home: index.md
  - Cookbook:
      - Basic Plots: cookbook/basic.md
      - Advanced Examples: cookbook/advanced.md
  - Test: test-brython.md  # <-- This shouldn't be in production nav
```

**Reason:** Test pages are for development only, not for end users.

**Fix Required in `mkdocs.yml`:**

Remove the Test entry:

```yaml
nav:
  - Home: index.md
  - Cookbook:
      - Basic Plots: cookbook/basic.md
      - Advanced Examples: cookbook/advanced.md
```

**Note:** The test page will still exist at `/test-brython/` URL for development/testing, it just won't appear in the navigation sidebar.

---

## Minor Issues

### 5. `__pycache__` in Plotille Copy ⚠️

**Issue:** The copy script copies `__pycache__` directories:

```bash
ls /Users/tammo/repos/plotille/site/src/lib/plotille/
# Shows __pycache__ with 50 entries
```

**Impact:** Adds ~500KB of unnecessary bytecode files to the documentation site.

**Fix Required in `scripts/copy_plotille_for_brython.py`:**

Add ignore pattern:

```python
#!/usr/bin/env python3
"""Copy plotille source files for Brython access."""
import shutil
from pathlib import Path


def ignore_pycache(directory, files):
    """Ignore __pycache__ directories and .pyc files."""
    return ['__pycache__'] + [f for f in files if f.endswith('.pyc')]


def main():
    project_root = Path(__file__).parent.parent
    source_dir = project_root / "plotille"
    dest_dir = project_root / "docs" / "src" / "lib" / "plotille"

    # Remove old copy
    if dest_dir.exists():
        shutil.rmtree(dest_dir)

    # Copy plotille source (excluding __pycache__)
    shutil.copytree(source_dir, dest_dir, ignore=ignore_pycache)
    print(f"Copied plotille to {dest_dir}")


if __name__ == "__main__":
    main()
```

**Test:**
```bash
python scripts/copy_plotille_for_brython.py
ls docs/src/lib/plotille/
# Should NOT show __pycache__
```

---

## Verification Checklist

After applying all fixes, verify:

### Build Process
- [ ] `python scripts/generate_docs.py` completes without errors
- [ ] All example files are processed correctly
- [ ] Static examples show "Output not available" message (expected until numpy/PIL installed in CI)
- [ ] No `__pycache__` directories in `docs/src/lib/plotille/`

### Browser Functionality (after Task 7.2)
- [ ] Visit http://127.0.0.1:8000/test-brython/
- [ ] Click `[RUN]` button shows output
- [ ] No "CodeMirror not loaded" error in console
- [ ] Visit cookbook pages - examples are editable
- [ ] Tab key inserts 4 spaces in code editors
- [ ] Click `[EXEC]` on simple examples (no plotille imports) - should work
- [ ] Click `[EXEC]` on plotille examples - will probably fail (expected until Brython compatibility verified)

### Navigation
- [ ] Test page is NOT in sidebar navigation
- [ ] Home, Basic Plots, and Advanced Examples appear in sidebar

---

## Summary

**Critical Fixes Needed:**
1. Fix `IsADirectoryError` in `generate_static_example_markdown()` - **Build breaking**
2. Complete Task 7.2: Proper Brython execution - **Functionality broken**

**Important Fixes:**
3. Remove misleading CodeMirror check
4. Remove test page from navigation
5. Exclude `__pycache__` from plotille copy

**Files to Modify:**
1. `scripts/generate_docs.py` - Fix #1
2. `docs/javascripts/brython-setup.js` - Fix #2 (implement Task 7.2)
3. `docs/javascripts/codemirror-setup.js` - Fix #3
4. `mkdocs.yml` - Fix #4
5. `scripts/copy_plotille_for_brython.py` - Fix #5

**Estimated Time:** 1-2 hours

**Next Steps After Fixes:**
1. Apply all fixes
2. Test build: `python scripts/generate_docs.py`
3. Test in browser: visit examples and click `[EXEC]` buttons
4. Commit: `git commit -m "Fix build errors and complete Task 7.2"`
5. Proceed to Phase 8: API Documentation (Task 8.1)

---

## Notes on Brython Compatibility

Even after Task 7.2 is completed, plotille may not work perfectly in Brython because:

- Brython has limited stdlib support (no full `io.StringIO`, limited `sys`, etc.)
- Plotille uses some features that may not be available in browser
- Unicode/braille character handling may differ

**Expected behavior after fixes:**
- ✅ Simple Python code (print, math, loops) should work
- ❓ Plotille examples may work partially or not at all
- ✅ Infrastructure is correct and ready for debugging/adjustments

**If plotille doesn't work in Brython:**
- This is documented as a known limitation in the original plan
- Static examples with pre-rendered output cover this case
- Future work could involve creating a simplified browser-compatible version

The immediate goal is to **get the infrastructure working correctly**, then we can address plotille compatibility separately if needed.
