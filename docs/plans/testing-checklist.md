# Documentation Testing Checklist

## Visual Design
- [ ] Standard Material theme applies throughout
- [ ] Terminal windows have proper dark styling
- [ ] Terminal windows use monospace fonts
- [ ] Responsive design works on mobile
- [ ] Site is readable and accessible

## Navigation
- [ ] All navigation links work
- [ ] Breadcrumbs function correctly
- [ ] Search works (if enabled)
- [ ] Active page is highlighted in sidebar

## Home Page
- [ ] Hero plot displays correctly
- [ ] Quick start code block renders
- [ ] Links to cookbook work

## Cookbook Pages
- [ ] All four category pages exist (basic, figures, canvas, advanced)
- [ ] Examples are categorized correctly
- [ ] Interactive examples have working editors
- [ ] Run buttons work for interactive examples
- [ ] Output displays correctly
- [ ] Static examples show pre-rendered output
- [ ] Dependency warnings show for static examples

## Interactive Examples
- [ ] Code editor is editable
- [ ] Tab key inserts spaces
- [ ] Run button executes code
- [ ] Output appears in terminal-styled div
- [ ] Errors display clearly
- [ ] Can modify code and re-run
- [ ] Multiple examples on same page don't interfere

## API Reference
- [ ] All API pages exist
- [ ] Docstrings render correctly
- [ ] Type hints display properly
- [ ] Function signatures are clear
- [ ] Examples in docstrings render
- [ ] Cross-references link correctly
- [ ] Source code links work

## Doctests
- [ ] All doctests pass: `pytest --doctest-modules plotille/`
- [ ] Coverage is reasonable (aim for 80%+ of public functions)

## Build Process
- [ ] `python scripts/generate_docs.py` completes without errors
- [ ] `mkdocs build` completes without warnings
- [ ] Generated site is in `site/` directory
- [ ] No broken links in built site

## CI/CD
- [ ] GitHub Actions workflow runs successfully
- [ ] Documentation deploys to gh-pages branch
- [ ] Site is accessible at plotille.tammo.io
- [ ] HTTPS works
- [ ] Custom domain configured correctly

## Performance
- [ ] Page load time is reasonable (<3s)
- [ ] No console errors in browser
- [ ] Brython loads correctly

## Browser Compatibility
- [ ] Works in Chrome/Chromium
- [ ] Works in Firefox
- [ ] Works in Safari
- [ ] Works in Edge
