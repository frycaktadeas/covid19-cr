"""

Make average curves for categories
Variables to define:
  - CASES_FILE is cases file
  - POPULATION_FILE is population file
  - AVERAGE_FILE is file with average curve
  - CATEGORIES - define categories with number of citizens
  - CATEGORIES - define labels of categories

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

            # Find the correct category
            for num, i in enumerate(CATEGORIES[:-1]):
                if i < population < CATEGORIES[num+1]:
                    # If it is not initialised
                    if CATEGORIES_LABELS[num] not in dictionary:
                        dictionary[CATEGORIES_LABELS[num]] = {
                            "x": [],
                            "y": [],
                            "count": 0
                        }

                    # Get values
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
                        if len(y) == len(current_cases.values()):
                            y[num2] = (y[num2] + ((cases[1] / population) * 100)) / 2

                        # First village
                        else:
                            y.append((cases[1] / population) * 100)

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

    before_text = str(dictionary[label]["count"]) + " "
    if dictionary[label]["count"] == 1:
        before_text = ""

    after_text = f"between {CATEGORIES[num]} and {CATEGORIES[num+1]} citizens"
    if CATEGORIES[num+1] == math.inf:
        after_text = f"more than {CATEGORIES[num]} citizens"

    plt.title(f"{before_text}{label} - {after_text}")

    # Show graph
    plt.show()
