import matplotlib.pyplot as plt
import datetime
import numpy

COLORS = ["b", "r", "g"]


def show_graph(x, y, label, name):
    # Prepare graph
    for num, (mx, my) in enumerate(zip(x, y)):
        if type(mx) == list:
            plt.plot(list(prepare_x(mx)), my, color=COLORS[num], label=f"Data from {mx[len(mx) - 1]}")
        else:
            plt.plot(list(prepare_x(x)), y, color=COLORS[num], label=f"Data from {x[len(x)-1]}")
            break
    # plt.plot(current_x, current_y2, color="r", label="Data from 19/11/2020")

    # Label axis and graph
    plt.xlabel("Date [YYYY-mm]")
    plt.ylabel(label)
    plt.title(name)
    plt.legend()

    plt.gcf().autofmt_xdate()
    # Show graph and then exit app
    plt.show()


def prepare_x(array):
    for date in array:
        yield datetime.datetime.strptime(date, "%Y-%m-%d")
