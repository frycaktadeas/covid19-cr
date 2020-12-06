"""

Reformat ini file to JSON
Variables to define:
  - FILENAME_INPUT is input file
  - FILENAME_OUTPUT is output file

"""

# Imports
import json
import csv

# Define constants
FILENAME_INPUT = "../data/covid19/obec.csv"
FILENAME_OUTPUT = "../data/final/cases.json"

# Define variables
refactored = {}


# Functions
def get_column(data, column):
    """
    Get from column data
    :param data: data
    :param column: column number
    :return: data from column
    """
    return data[0].split(";")[column]


# Load input file
with open(FILENAME_INPUT, "r") as file:
    # Read *.csv file
    reader = csv.reader(file)

    # For every line (without header line)
    for line in list(reader)[1:]:
        # Get some information from each line
        date = get_column(line, 1)
        region = get_column(line, 3)
        district_code = get_column(line, 4)
        district_name = get_column(line, 5)
        village = get_column(line, 11)

        # If village name is valid
        if village != "N/A":
            # Create region in dictionary, if it hasn't been created yet
            if region not in refactored:
                refactored[region] = {}

            # Same for district
            if district_code not in refactored[region]:
                refactored[region][district_code] = {}

            # Same for village name
            if village not in refactored[region][district_code]:
                refactored[region][district_code][village] = {}

            # Save information to current village and to current date
            refactored[region][district_code][village][date] = int(get_column(line, 13))

# Save to output file
with open(FILENAME_OUTPUT, "w") as file:
    json.dump(refactored, file)
