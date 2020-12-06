"""

Generates regions with district codes to JSON fine
Variables to define:
  - FILENAME_INPUT is input file
  - FILENAME_OUTPUT is output file

"""

# Imports
import json
import csv

# Define constants
FILENAME_INPUT = "data/covid19/obec.csv"
FILENAME_OUTPUT = "data/regions.json"

# Define variables
dictionary = {}


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
        region = get_column(line, 3)
        district_code = get_column(line, 4)
        district_name = get_column(line, 5)

        # Sort codes to regions
        if region not in dictionary:
            dictionary[region] = {}

        dictionary[region][district_code] = district_name

# Save to output file
with open(FILENAME_OUTPUT, "w") as file:
    json.dump(dictionary, file)

