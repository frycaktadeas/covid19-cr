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

            # Make time x array of values
            if len(time_x) == number:
                time_x.append(list(cases_content[number][district][village].keys()))

                cases_y.append([])
                eohi_y.append([])

            # Make cases y array of values
            for num, cases in enumerate(cases_content[number][district][village].values()):
                cases_people = (cases[1] / population) * 100

                # Nth village
                try:
                    cases_y[number][num] += cases[1]
                    eohi_y[number][num] = (eohi_y[number][num] + cases_people) / 2

                # First village
                except IndexError:
                    cases_y[number].append(cases[1])
                    eohi_y[number].append(cases_people)


show_graph(time_x, cases_y, "Active cases", "Compare data - Czech Republic")
show_graph(time_x, eohi_y, "Establishment of herd immunity [%]",
           f"Compare data - Czech Republic")
