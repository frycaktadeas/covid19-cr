# Imports
import json
import csv

# Define constants
import pandas

FILENAME_INPUT = "../data/coordinates/Obce_centroid.xls"
FILENAME_OUTPUT = "../data/final/location.json"

DISTRICT = "NAZ_OBEC"
CENTROID_X = "INSIDE_X"
CENTROID_Y = "INSIDE_Y"

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


current_data = pandas.read_excel(FILENAME_INPUT)
current_df = pandas.DataFrame(current_data, columns=[DISTRICT, CENTROID_X, CENTROID_Y])

for num, district in enumerate(current_df[DISTRICT]):
    dictionary[district] = [current_df[CENTROID_X][num],
                            current_df[CENTROID_Y][num]]

print(dictionary)
# Save to output file
with open(FILENAME_OUTPUT, "w") as file:
    json.dump(dictionary, file)

