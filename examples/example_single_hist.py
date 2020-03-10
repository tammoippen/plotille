import plotille
import numpy as np

print("Histogram left to right")
print(plotille.hist(np.random.normal(size=10000)))

print("Histogram rotated")
print(plotille.histogram(np.random.normal(size=10000)))
