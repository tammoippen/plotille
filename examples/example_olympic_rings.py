import plotille


fig = plotille.Figure()
fig.width = 50
fig.height = 20

# the olympic rings
fig.set_x_limits(min_=0, max_=600)
fig.set_y_limits(min_=0, max_=500)

centers = []
centers.append([250, 200, 'blue'])
centers.append([375, 200, 'black'])
centers.append([500, 200, 'red'])
centers.append([310, 250, 'yellow'])
centers.append([435, 250, 'green'])
for ring in centers:
    fig.circle(xcenter=ring[0], ycenter=500-ring[1], radius=50, lc=ring[2])

print(fig.show(legend=False))
