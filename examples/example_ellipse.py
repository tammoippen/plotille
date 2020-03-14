import plotille


if __name__ == "__main__":

    fig = plotille.Figure()
    fig.width = 50
    fig.height = 20

    fig.ellipse(xCenter=0, yCenter=0, xAmplitude=0.5,  yAmplitude=0.5)
    print(fig.show(legend=True))

    # first set
    fig.ellipse(xCenter=0, yCenter=0)

    fig.ellipse(xCenter=0, yCenter=0, xAmplitude=0.5, yAmplitude=0.5, label='Ellipse 2')

    print(fig.show(legend=True))

    # second set, offset
    fig.clear()
    fig.ellipse(xCenter=0, yCenter=0)
    fig.set_x_limits(min_=-10, max_=10)
    fig.set_y_limits(min_=-10, max_=10)

    for xx in [-4, 0, 4]:
        for yy in [-4, 0, 4]:
            fig.ellipse(xCenter=xx, yCenter=yy, xAmplitude=1, yAmplitude=1, label=("%d,%d" % (xx, yy)))

    fig.scatter([4], [4])

    print(fig.show(legend=True))
