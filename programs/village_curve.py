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
POPULATION_FILE = "../data/final/population.json"

# Define variables
time_x = []
cases_y = []
eohi_y = []

# Load cases file
with open(CASES_FILE, "r") as file:
    cases_content = json.load(file)

with open(POPULATION_FILE, "r") as file:
    population_content = json.load(file)


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
                    eohi_y.append(cases / population* 100)

                show_graph(cases_y, "Active cases")
                show_graph(eohi_y, "Establishment of herd immunity [%]")
                exit()
