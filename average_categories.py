"""

Make average curves for categories
Variables to define:
  - CATEGORIES - define categories with number of citizens
  - CATEGORIES_LABELS - define labels of categories

"""

# Imports
from library.data import Covid19, Population, Area
import math

# Define constants
from library.graph import show_graph

CATEGORIES = [1, 3_000, 50_000, 1_300_000, math.inf]
CATEGORIES_LABELS = ["villages", "towns", "cities", "Prague"]

# Define variables
dictionary = {}

cases_content = Covid19().load().data()
population_content = Population().load().data()
area_content = Area().load().data()

# For every district in number
for district in cases_content:
    # For every village in district
    for village in cases_content[district]:
        # Get village name without district in brackets
        population = population_content[district][village]

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
                dictionary[CATEGORIES_LABELS[num]]["x"] = list(cases_content[district][village].keys())
                y = dictionary[CATEGORIES_LABELS[num]]["y"]
                dictionary[CATEGORIES_LABELS[num]]["count"] += 1

                current_cases = cases_content[district][village]

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
    before_text = str(dictionary[label]["count"]) + " "
    if dictionary[label]["count"] == 1:
        before_text = ""

    after_text = f"between {CATEGORIES[num]} and {CATEGORIES[num+1]} citizens"
    if CATEGORIES[num+1] == math.inf:
        after_text = f"more than {CATEGORIES[num]} citizens"

    # Show graph
    show_graph(dictionary[label]["x"], dictionary[label]["y"],
               "Establishment of herd immunity [%]", f"{before_text}{label} - {after_text}")
