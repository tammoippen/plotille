import plotille


import numpy


  
fig = plotille.Figure()
fig.width = 50
fig.height = 20


x = numpy.linspace(0, 2*numpy.pi, 20)
y = numpy.sin(x)
fig.plot(x,y, lc='red')

xs = x[::5]
ys = y[::5]

fig.scatter(xs, ys, lc='green', marker='x', text=["%.3f" % (val) for val in ys])

print(fig.show(legend=True))

