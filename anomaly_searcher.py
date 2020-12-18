"""

Look for some anomalies in curves against average curve
Variables to define:
  - AVERAGE_FILE is file with average curve
  - MAX_POPULATION is max population of village to be selected as anomaly
  - MIN_POPULATION is min population of village to be selected as anomaly

"""

# Imports
from library.data import Covid19, Population, Area
from library.graph import show_graph
import json

# Define constants

AVERAGE_FILE = "data/final/average.json"

MAX_POPULATION = 3000000
MIN_POPULATION = 1000

cases_content = Covid19().load().data()
population_content = Population().load().data()
area_content = Area().load().data()

# Load files
with open(AVERAGE_FILE, "r") as file:
    content = json.load(file)
    average_time_x = content["x"]
    average_cases_y = content["y"]

# For every district in number
for district in cases_content:
    # For every village in district
    for village in cases_content[district]:
        # Get village name without district in brackets
        population = population_content[district][village]

        # Define variables
        cases_y = []
        difference = []

        # Make curve for current village
        for cases in cases_content[district][village].values():
            cases_y.append(cases[1] / population * 100)

        # Make difference
        for num, i in enumerate(cases_y):
            difference.append(abs(average_cases_y[num] - i))

        # If difference in summer is high
        if sum(difference[60:][:110]) >= 25 and MAX_POPULATION > population > MIN_POPULATION:
            # Show graph
            show_graph(average_time_x, difference, "Establishment of herd immunity [%]",
                       f"{area_content[village][0]} - {population} citizens")
