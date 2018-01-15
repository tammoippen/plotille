from datetime import datetime

from plotille import Figure

# Epoch second timestamp
t = 1516036975
# Make a list of time stamps over 20 days (86400 seconds per day)
x = [t+(i*86400) for i in range(20)]
y = [i for i in range(20)]
fig = Figure()
fig.axis_round = 2
fig.y_axis_transform = lambda x: "{:.2f}".format(3*x)
fig.x_axis_transform = lambda x: '{:%m-%d-%y}'.format(datetime.fromtimestamp(x))
fig.plot(x, y)
print(fig.show(legend=False))
