import plotille
import numpy as np
X = np.linspace(0, 2*np.pi, 20)
print(plotille.plot(X, np.sin(X), height=30, width=60))
