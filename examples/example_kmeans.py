import numpy as np

from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from skimage.measure import EllipseModel

import plotille
from plotille import _colors


fig = plotille.Figure()
fig.width = 50
fig.height = 20

n_samples = 200
random_state = 170
X, y = make_blobs(n_samples=n_samples, random_state=random_state)

y_pred = KMeans(n_clusters=3, random_state=random_state).fit_predict(X)

color_list = list(filter(lambda color: "bright" in color, sorted(_colors._FOREGROUNDS.keys())))
marker_list = ['x', 'o', '+', '*', '#', '^']

for cluster_index in range(3):
    x_indices = np.where(cluster_index == y_pred)[0]
    cx = X[x_indices, 0]
    cy = X[x_indices, 1]

    ell = EllipseModel()
    ell.estimate(X[x_indices])
    xc, yc, a, b, theta = ell.params

    fig.scatter(cx, cy, lc=color_list[cluster_index])

    fig.ellipse(xcenter=xc, ycenter=yc, xamplitude=a,  yamplitude=b, angle=theta)

print(fig.show(legend=False))
