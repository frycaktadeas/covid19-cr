"""

Shows graph of active cases depending on time for selected village
Variables to define:
  - VILLAGE_NAME is name of village to show graph
  - CASES_FILE is cases refactored file
  - POPULATION_FILE is refactored population file

"""

# Imports
from library.data import Population, Covid19, Area, Coordinates
from library.graph import show_graph

# Define constants
VILLAGE_NAME = "Praha".lower()

# Define variables
time_x = []
cases_y = []
eohi_y = []

cases_content = Covid19().load().data()
population_content = Population().load().data()
area_content = Area().load().data()


# For every village in district
for district in cases_content:
    for village in cases_content[district]:
        population = population_content[district][village]
        village_name = area_content[village][0]
        village_name_pure = village_name.split(" (")[0]

        # If this village is selected village
        if village_name.lower() == VILLAGE_NAME or village_name_pure.lower() == VILLAGE_NAME:
            # Make time x array of values
            time_x = list(cases_content[district][village].keys())

            # Make cases y array of values
            for cases in cases_content[district][village].values():
                cases_y.append(cases[1])
                eohi_y.append(cases[1] / population * 100)

            show_graph(time_x, cases_y, "Cases [count]", f"Active cases - {VILLAGE_NAME.capitalize()}")
            show_graph(time_x, eohi_y, "Establishment of herd immunity [%]", f"EoHI - {VILLAGE_NAME.capitalize()}")
            exit()
