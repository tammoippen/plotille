from datetime import datetime, timezone
from random import randint
from time import sleep

import plotille as plt


def new_tick():
    return datetime.now(tz=timezone.utc), randint(0, 100)


def main():
    X = []
    Y = []
    now = datetime.now(tz=timezone.utc)

    while True:
        x, y = new_tick()
        X.append(x)
        Y.append(y)
        fig = plt.Figure()
        fig.width = 40
        fig.height = 20
        fig.plot(X, Y)
        fig.origin = False
        fig.set_x_limits(min_=now)
        fig.set_y_limits(min_=0, max_=100)
        sleep(1)
        print(fig.show())


if __name__ == "__main__":
    main()
