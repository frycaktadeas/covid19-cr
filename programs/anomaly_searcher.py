"""

Look for some anomalies in curves against average curve
Variables to define:
  - CASES_FILE is cases file
  - POPULATION_FILE is population file
  - AVERAGE_FILE is file with average curve
  - MAX_POPULATION is max population of village to be selected as anomaly
  - MIN_POPULATION is min population of village to be selected as anomaly

"""

# Imports
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import json

# Define constants
CASES_FILE = "../data/final/cases.json"
POPULATION_FILE = "../data/final/population.json"
AVERAGE_FILE = "../data/final/average.json"

MAX_POPULATION = 3000000
MIN_POPULATION = 1000

# Load files
with open(CASES_FILE, "r") as file:
    cases_content = json.load(file)

with open(POPULATION_FILE, "r") as file:
    population_content = json.load(file)

with open(AVERAGE_FILE, "r") as file:
    content = json.load(file)
    average_time_x = content["x"]
    average_cases_y = content["y"]

# For every region in cases file
for region in cases_content:
    # For every district in region
    for district in cases_content[region]:
        # For every village in district
        for village in cases_content[region][district]:
            # Get village name without district in brackets
            real_name_village = village.split(" (")[0]
            population = population_content[region][district][real_name_village]

            # Define variables
            cases_y = []
            difference = []

            # Make curve for current village
            for cases in cases_content[region][district][village].values():
                cases_y.append(cases / population * 100)

            # Make difference
            for num, i in enumerate(cases_y):
                difference.append(abs(average_cases_y[num] - i))

            # If difference in summer is high
            if sum(difference[60:][:110]) >= 25 and MAX_POPULATION > population > MIN_POPULATION:
                # Prepare graph
                fig, ax = plt.subplots()
                ax.plot(average_time_x, difference)

                # Show every 28th label
                ax.xaxis.set_major_locator(ticker.MultipleLocator(28))

                # Label axis and graph
                plt.xlabel("Date [dd/mm]")
                plt.ylabel("Establishment of herd immunity [%]")
                plt.title(f"{real_name_village} - {population} citizens")

                # Show graph
                plt.show()
