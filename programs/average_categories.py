"""

Make average curves for categories
Variables to define:
  - CASES_FILE is cases file
  - POPULATION_FILE is population file
  - AVERAGE_FILE is file with average curve
  - MAX_POPULATION is max population of village to be selected as anomaly
  - MIN_POPULATION is min population of village to be selected as anomaly

"""

# Imports
import math

import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import json

# Define constants
CASES_FILE = "../data/final/cases.json"
POPULATION_FILE = "../data/final/population.json"

CATEGORIES = [1, 3_000, 50_000, 1_300_000, math.inf]
CATEGORIES_LABELS = ["villages", "towns", "cities", "Prague"]

# Define variables
dictionary = {}

# Load files
with open(CASES_FILE, "r") as file:
    cases_content = json.load(file)

with open(POPULATION_FILE, "r") as file:
    population_content = json.load(file)

# For every region in cases file
for region in cases_content:
    # For every district in region
    for district in cases_content[region]:
        # For every village in district
        for village in cases_content[region][district]:
            # Get village name without district in brackets
            real_name_village = village.split(" (")[0]
            population = population_content[region][district][real_name_village]

            for num, i in enumerate(CATEGORIES[:-1]):
                if i < population < CATEGORIES[num+1]:
                    if CATEGORIES_LABELS[num] not in dictionary:
                        dictionary[CATEGORIES_LABELS[num]] = {
                            "x": [],
                            "y": [],
                            "count": 0
                        }

                    x = dictionary[CATEGORIES_LABELS[num]]["x"]
                    y = dictionary[CATEGORIES_LABELS[num]]["y"]
                    dictionary[CATEGORIES_LABELS[num]]["count"] += 1

                    current_cases = cases_content[region][district][village]

                    # X axis
                    if not x:
                        # Make time x axis
                        for date in current_cases.keys():
                            # time_x.append(date)
                            split_date = date.split("-")
                            x.append(f"{split_date[2]}/{split_date[1]}")

                    # Y axis
                    for num2, cases in enumerate(current_cases.values()):
                        # Second, third, ... village
                        # try:
                        if len(y) == len(current_cases.values()):
                            y[num2] = (y[num2] + cases / population * 100) / 2

                        else:
                            y.append(cases) # / population * 100)
                        # First village
                        # except IndexError:


                    break

for num, label in enumerate(dictionary.keys()):
    # Prepare graph
    fig, ax = plt.subplots()
    ax.plot(dictionary[label]["x"], dictionary[label]["y"])

    # Show every 28th label
    ax.xaxis.set_major_locator(ticker.MultipleLocator(28))

    # Label axis and graph
    plt.xlabel("Date [dd/mm]")
    plt.ylabel("Establishment of herd immunity [%]")
    plt.title(f"{dictionary[label]['count']} {label} - between {CATEGORIES[num]} and {CATEGORIES[num+1]} people")

    # Show graph
    plt.show()
