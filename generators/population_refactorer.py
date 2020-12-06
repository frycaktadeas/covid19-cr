"""

Reformat Excel files from dir to one JSON
Variables to define:
  - DIR_INPUT is input dir with Excel files
  - FILENAME_OUTPUT is output file
  - FILENAME_REGIONS is file with regions and districts

"""

# Imports
import pandas
import json
import os

# Define constants
DIR_INPUT = "data/pohyb19"
FILENAME_OUTPUT = "data/final/population.json"
FILENAME_REGIONS = "data/regions.json"

# Define constants for Excel files
YEAR = "Rok"
VILLAGE_NAME = "Název obce"
COUNT = "Stav 31.12."

# Load JSON file with regions
with open(FILENAME_REGIONS, "r") as file:
    regions = json.load(file)

# Copy this JSON
output = regions.copy()

# For every Excel file in dir
for file in os.listdir(DIR_INPUT):
    # Validation, if file is really Excel file
    if file.endswith(".xlsx"):
        # Load data and select columns
        current_data = pandas.read_excel(os.path.join(DIR_INPUT, file))
        current_df = pandas.DataFrame(current_data, columns=[YEAR, VILLAGE_NAME, COUNT])

        # Define variables for current file
        current_refactored = {}
        current_final = {}

        # Refactor
        for num, village in enumerate(current_df[VILLAGE_NAME]):
            # If village is not in dictionary
            if village not in current_refactored:
                # Append information about village
                current_refactored[village] = {"year": current_df[YEAR][num], "count": current_df[COUNT][num]}

            else:
                # If this year is newer than last year
                if current_refactored[village]["year"] < current_df[YEAR][num]:
                    # If it is valid
                    if current_df[COUNT][num] != "-":
                        # Change to newer information
                        current_refactored[village]["year"] = current_df[YEAR][num]
                        current_refactored[village]["count"] = current_df[COUNT][num]

        # Delete old villages
        for key in current_refactored:
            # Copy only villages that have year >= 2015
            if current_refactored[key]["year"] >= 2015:
                current_final[key] = int(current_refactored[key]["count"])

            # else:
            #     print(key, current_refactored[key]["year"], current_refactored[key]["count"])

        # For every region in output
        for region in output:
            # Get district code from name of file
            district_code = os.path.splitext(file)[0]
            if district_code in output[region].keys():
                # Save information
                output[region][district_code] = current_final


# Save to output file
with open(FILENAME_OUTPUT, mode="w") as file:
    json.dump(output, file)

    # writer = csv.writer(file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # for key in total_final:
    #     writer.writerow([key, total_final[key]])
