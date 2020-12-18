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
from library.data import Covid19, Population, Area
from library.graph import show_graph

VILLAGE_NAME = "Praha".lower()

# Define variables
pre = {}

time_x = []
cases_y = []
eohi_y = []

cases_content = Covid19().load().data(compare=True)
population_content = Population().load().data()
area_content = Area().load().data()

# For every number in cases file
for number in range(len(cases_content)):
    # For every district in number
    for district in cases_content[number]:
        # For every village in district
        for village in cases_content[number][district]:
            # Get village name without district in brackets
            population = population_content[district][village]

            village_name = area_content[village][0]
            village_name_pure = village_name.split(" (")[0]

            # If this village is selected village
            if village_name.lower() == VILLAGE_NAME or village_name_pure.lower() == VILLAGE_NAME:
                # Make time x array of values
                time_x.append(list(cases_content[number][district][village].keys()))
                cases_y.append([])
                eohi_y.append([])

                # Make cases y array of values
                for cases in cases_content[number][district][village].values():
                    cases_y[number].append(cases[1])
                    eohi_y[number].append(cases[1] / population * 100)

                break

        else:
            continue
        break

show_graph(time_x, cases_y, "Active cases", f"Compare data - {VILLAGE_NAME.capitalize()}")
show_graph(time_x, eohi_y, "Establishment of herd immunity [%]",
           f"Compare data - {VILLAGE_NAME.capitalize()}")
