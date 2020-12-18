"""

Shows average curve in graph of Czech republic
Save this average curve to JSON

"""

# Imports
from library.data import Covid19, Population
from library.graph import show_graph
import json

# General constants
OUTPUT_FILE = "data/final/average.json"
cases_content = Covid19().load().data()
population_content = Population().load().data()

# Define variables
time_x = []
cases_y = []

# For every district in number
for district in cases_content:
    # For every village in district
    for village in cases_content[district]:
        population = population_content[district][village]

        # X axis
        time_x = list(cases_content[district][village].keys())

        # Y axis
        for num, cases in enumerate(cases_content[district][village].values()):
            cases_people = (cases[1] / population) * 100

            # Nth village
            try:
                cases_y[num] = (cases_y[num] + cases_people) / 2

            # First village
            except IndexError:
                cases_y.append(cases_people)


with open(OUTPUT_FILE, "w") as file:
    json.dump({"x": time_x, "y": cases_y}, file)

show_graph(time_x, cases_y, "Establishment of herd immunity [%]", "CR - Average curve")
