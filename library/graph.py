import matplotlib.pyplot as plt
import datetime


def show_graph(x, y, label, name):
    # Prepare graph
    plt.plot(list(prepare_x(x)), y, color="b", label="Data from 06/12/2020")
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
