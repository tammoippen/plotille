# plotille

<div class="hero-terminal">
    <div class="terminal-header">
        <span class="terminal-title">[root@plotille ~]$</span>
    </div>
    <div class="terminal-body">
        <pre class="hero-plot" id="hero-animation"></pre>
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

