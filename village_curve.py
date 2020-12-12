"""

Shows graph of active cases depending on time for selected village
Variables to define:
  - VILLAGE_NAME is name of village to show graph
  - CASES_FILE is cases refactored file
  - POPULATION_FILE is refactored population file

"""

# Imports
from data.data import Population, Covid19, Area
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import json

# Define constants
VILLAGE_NAME = "Žermanice".lower()


# Define variables
time_x = []
cases_y = []
eohi_y = []

cases_content = Covid19().load().data()
population_content = Population().load().data()
area_content = Area().load().data()


# Functions
def show_graph(y, label):
    # Prepare graph
    fig, ax = plt.subplots()
    ax.plot(time_x, y)

    # Show every 28th label
    ax.xaxis.set_major_locator(ticker.MultipleLocator(28))

    # Label axis and graph
    plt.xlabel("Date [dd/mm]")
    plt.ylabel(label)
    plt.title(f"{village_name} - {population} citizens")

    # Show graph and then exit app
    plt.show()


# For every village in district
for village_code in cases_content:
    population = population_content[village_code]
    village_name = area_content[village_code][0]
    village_name_pure = village_name.split(" (")[0]

    # If this village is selected village
    if village_name.lower() == VILLAGE_NAME or village_name_pure.lower() == VILLAGE_NAME:
        # Make time x array of values
        for date in cases_content[village_code].keys():
            split_date = date.split("-")
            time_x.append(f"{split_date[2]}/{split_date[1]}")

        # Make cases y array of values
        for cases in cases_content[village_code].values():
            cases_y.append(cases[1])
            eohi_y.append(cases[1] / population * 100)

        show_graph(cases_y, "Active cases")
        show_graph(eohi_y, "Establishment of herd immunity [%]")
        exit()
