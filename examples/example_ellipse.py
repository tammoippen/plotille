import plotille


if __name__ == "__main__":

    fig = plotille.Figure()
    fig.width = 50
    fig.height = 20

    fig.ellipse(xcenter=0, ycenter=0, xamplitude=0.5,  yamplitude=0.5)
    print(fig.show(legend=True))

    # first set
    fig.ellipse(xcenter=0, ycenter=0)

    fig.ellipse(xcenter=0, ycenter=0, xamplitude=0.5, yamplitude=0.5, label='Ellipse 2')

    print(fig.show(legend=True))

    # second set, offset
    fig.clear()
    fig.ellipse(xcenter=0, ycenter=0)
    fig.set_x_limits(min_=-10, max_=10)
    fig.set_y_limits(min_=-10, max_=10)

    for xx in [-4, 0, 4]:
        for yy in [-4, 0, 4]:
            fig.ellipse(xcenter=xx, ycenter=yy, xamplitude=1, yamplitude=1, label=("%d,%d" % (xx, yy)))

    fig.scatter([4], [4])

    print(fig.show(legend=True))
