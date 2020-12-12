"""

Shows graph of active cases depending on time for selected village
Variables to define:
  - VILLAGE_NAME is name of village to show graph
  - CASES_FILE is cases refactored file
  - POPULATION_FILE is refactored population file

"""

# Imports
import matplotlib.pyplot as plt
import datetime
import json

# Define constants
CASES_FILE = "data/final/cases.json"
CASES_FILE_OLD = "data/final/cases_old.json"
POPULATION_FILE = "data/final/population.json"

# Define variables
time_x = []
cases_y = []
cases_y_old = []

cases_total = []
cases_total_old = []

cases_all = 0
cases_all_old = 0

# Load cases file
with open(CASES_FILE, "r") as file:
    cases_content = json.load(file)

with open(CASES_FILE_OLD, "r") as file:
    cases_content_old = json.load(file)

with open(POPULATION_FILE, "r") as file:
    population_content = json.load(file)


# Functions
def show_graph(y, y2, label, name):
    # Prepare graph
    current_x = time_x[:264]
    current_y = y[:264]
    current_y2 = y2[:264]

    plt.plot(current_x, current_y, color="b", label="Data from 06/12/2020")
    plt.plot(current_x, current_y2, color="r", label="Data from 19/11/2020")

    # Label axis and graph
    plt.xlabel("Date [YYYY-mm]")
    plt.ylabel(label)
    plt.title(name)
    plt.legend()

    plt.gcf().autofmt_xdate()
    # Show graph and then exit app
    plt.show()


# For every region in cases file
for region in cases_content:
    # For every district in region
    for district in cases_content[region]:
        # For every village in district
        for village in cases_content[region][district]:
            # Get village name without district in brackets
            real_name_village = village.split(" (")[0]
            population = population_content[region][district][real_name_village]

            # X axis
            if not time_x:
                # Make time x axis
                for date in cases_content[region][district][village].keys():
                    date_final = datetime.datetime.strptime(date, "%Y-%m-%d")
                    time_x.append(date_final)

            # Y axis
            for num, cases in enumerate(list(cases_content[region][district][village].values())[:264]):
                cases_all += cases[0]
                # Second, third, ... village
                try:
                    cases_total[num] += cases[1]
                    cases_y[num] = (cases_y[num] + cases[1] / population * 100) / 2

                # First village
                except IndexError:
                    cases_total.append(cases[1])
                    cases_y.append(cases[1] / population * 100)

            # Y axis
            for num, cases in enumerate(cases_content_old[region][district][village].values()):
                cases_all_old += cases[0]

                # Second, third, ... village
                try:
                    cases_total_old[num] += cases[1]
                    cases_y_old[num] = (cases_y_old[num] + cases[1] / population * 100) / 2

                # First village
                except IndexError:
                    cases_total_old.append(cases[1])
                    cases_y_old.append(cases[1] / population * 100)

show_graph(cases_y, cases_y_old, "Establishment of herd immunity [%]", "Czech Republic - average curve")
show_graph(cases_total, cases_total_old, "Active cases", "Czech Republic - total curve")

print("All", cases_all_old-cases_all)
