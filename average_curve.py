"""

Shows average curve in graph of Czech republic
Save this average curve to JSON
Variables to define:
  - CASES_FILE is cases refactored file
  - VILLAGE_NAME is name of village to show graph

"""

# Imports
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import json

# General constants
CASES_FILE = "data/final/cases.json"
POPULATION_FILE = "data/final/population.json"
OUTPUT_FILE = "data/final/average.json"

# Load files
with open(CASES_FILE, "r") as file:
    cases_content = json.load(file)

with open(POPULATION_FILE, "r") as file:
    population_content = json.load(file)

# Define variables
time_x = []
cases_y = []

# For every region in cases file
for region in cases_content:
    # For every district in region
    for district in cases_content[region]:
        # For every village in district
        for village in cases_content[region][district]:
            # Get village name without district in brackets
            real_name_village = village.split(" (")[0]
            population = population_content[region][district][real_name_village]

            # Validation
            if real_name_village in population_content[region][district]:
                # X axis
                if not time_x:
                    # Make time x axis
                    for date in cases_content[region][district][village].keys():
                        # time_x.append(date)
                        split_date = date.split("-")
                        time_x.append(f"{split_date[2]}/{split_date[1]}")

                # Y axis
                for num, cases in enumerate(cases_content[region][district][village].values()):
                    # Second, third, ... village
                    try:
                        cases_y[num] = (cases_y[num] + cases[1] / population * 100) / 2

                    # First village
                    except IndexError:
                        cases_y.append(cases[1] / population * 100)

            else:
                print(f"'{village}' not found in region '{region}' in district '{district}'")

with open(OUTPUT_FILE, "w") as file:
    json.dump({"x": time_x, "y": cases_y}, file)

# Prepare graph
fig, ax = plt.subplots()
ax.plot(time_x, cases_y)

# Show every 28th label
ax.xaxis.set_major_locator(ticker.MultipleLocator(28))

# Label axis and graph
plt.xlabel("Date [dd/mm]")
plt.ylabel("Establishment of herd immunity [%]")
plt.title("CR - Covid19 establishment of herd immunity")

# Show graph
plt.show()
