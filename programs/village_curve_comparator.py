"""

Shows graph of active cases depending on time for selected village
Variables to define:
  - VILLAGE_NAME is name of village to show graph
  - CASES_FILE is cases refactored file
  - POPULATION_FILE is refactored population file

"""

# Imports
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import json

# Define constants
VILLAGE_NAME = "Žermanice"

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
def show_graph(y, y2, label):
    # Prepare graph
    current_x = time_x[:264]
    current_y = y[:264]
    current_y2 = y2[:264]
    current_min = min(current_y + current_y2)
    current_max = max(current_y + current_y2)

    fig, ax = plt.subplots()
    ax.plot(current_x, current_y)
    ax2 = ax.twinx()
    ax2.plot(current_x, current_y2, color="r")

    ax.set_ylim(current_min, current_max)
    ax2.set_ylim(current_min, current_max)

    # Show every 28th label
    ax.xaxis.set_major_locator(ticker.MultipleLocator(28))

    # Label axis and graph
    plt.xlabel("Date [dd/mm]")
    plt.ylabel(label)
    plt.title(f"{village} - {population} citizens")

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
                    split_date = date.split("-")
                    time_x.append(f"{split_date[2]}/{split_date[1]}")

                # Make cases y array of values
                for cases in cases_content[region][district][village].values():
                    cases_y.append(cases)
                    eohi_y.append(cases / population * 100)

                for cases in cases_content_old[region][district][village].values():
                    cases_y2.append(cases)
                    eohi_y2.append(cases / population * 100)

                show_graph(cases_y, cases_y2, "Active cases")
                show_graph(eohi_y, eohi_y2, "Establishment of herd immunity [%]")
                exit()
