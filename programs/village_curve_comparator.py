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
VILLAGE_NAME = "Karviná"

CASES_FILE = "../data/final/cases.json"
CASES_FILE_OLD = "../data/final/cases_old.json"
POPULATION_FILE = "../data/final/population.json"

# Define variables
time_x = []
cases_y = []
cases_y2 = []
eohi_y = []
eohi_y2 = []

# Load cases file
with open(CASES_FILE, "r") as file:
    cases_content = json.load(file)

with open(CASES_FILE_OLD, "r") as file:
    cases_content_old = json.load(file)

with open(POPULATION_FILE, "r") as file:
    population_content = json.load(file)


# Functions
# Functions
def show_graph(y, y2, label):
    # Prepare graph
    current_x = time_x[:264]
    current_y = y[:264]
    current_y2 = y2[:264]

    plt.plot(current_x, current_y, color="b", label="Data from 06/12/2020")
    plt.plot(current_x, current_y2, color="r", label="Data from 19/11/2020")

    # Label axis and graph
    plt.xlabel("Date [YYYY-mm]")
    plt.ylabel(label)
    plt.title(f"{village} - {population} citizens")

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

            # If this village is selected village
            if village.lower() == VILLAGE_NAME.lower() or real_name_village.lower() == VILLAGE_NAME.lower():
                # Make time x array of values
                for date in cases_content[region][district][village].keys():
                    date_final = datetime.datetime.strptime(date, "%Y-%m-%d")
                    time_x.append(date_final)

                # Make cases y array of values
                for cases in cases_content[region][district][village].values():
                    cases_y.append(cases[1])
                    eohi_y.append(cases[1] / population * 100)

                for cases in cases_content_old[region][district][village].values():
                    cases_y2.append(cases[1])
                    eohi_y2.append(cases[1] / population * 100)

                show_graph(cases_y, cases_y2, "Active cases")
                show_graph(eohi_y, eohi_y2, "Establishment of herd immunity [%]")
                exit()
