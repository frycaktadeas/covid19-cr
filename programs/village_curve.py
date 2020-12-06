"""

Shows graph of active cases depending on time for selected village
Variables to define:
  - CASES_FILE is cases refactored file
  - VILLAGE_NAME is name of village to show graph

"""

# Imports
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import json

# Define constants
CASES_FILE = "data/final/cases.json"
VILLAGE_NAME = "Český Krumlov"

# Define variables
time_x = []
cases_y = []

# Load cases file
with open(CASES_FILE, "r") as file:
    cases_content = json.load(file)

# For every region in cases file
for region in cases_content:
    # For every district in region
    for district in cases_content[region]:
        # For every village in district
        for village in cases_content[region][district]:
            # Get village name without district in brackets
            real_name_village = village.split(" (")[0]

            # If this village is selected village
            if real_name_village == VILLAGE_NAME:
                # Make time x array of values
                for date in cases_content[region][district][village].keys():
                    split_date = date.split("-")
                    time_x.append(f"{split_date[2]}/{split_date[1]}")

                # Make cases y array of values
                for cases in cases_content[region][district][village].values():
                    cases_y.append(cases)

                # Prepare graph
                fig, ax = plt.subplots()
                ax.plot(time_x, cases_y)

                # Show every 25th information
                ax.xaxis.set_major_locator(ticker.MultipleLocator(25))

                # Label axes and graph
                plt.xlabel("Date [dd/mm]")
                plt.ylabel("Active cases")
                plt.title(f"{village} - Covid19 active cases")

                # Show graph and then exit app
                plt.show()
                exit()
