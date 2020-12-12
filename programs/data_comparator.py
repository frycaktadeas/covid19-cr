from multiprocessing import Process, Queue
# Imports
import json
import csv

# Define constants
FILENAME_INPUT_CURRENT = "../data/covid19/obec.csv"
FILENAME_INPUT_OLD = "../data/covid19/obec_old.csv"

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
    return data.split(";")[column]


old = []
current = []

# Load input old file
with open(FILENAME_INPUT_OLD, "r") as file_old:
    # Read *.csv file
    reader_old = csv.reader(file_old)
    for line in list(reader_old)[1:]:
        old.append(line[0])

# Load input file
with open(FILENAME_INPUT_CURRENT, "r") as file_current:
    # Read *.csv file
    reader_current = csv.reader(file_current)
    for line in list(reader_current)[1:]:
        current.append(line[0])


def work(my_old, my_current, thread_number):
    # For every line (without header line)
    for line_old in my_old:
        # Get some information from each line
        date_old = get_column(line_old, 1)
        district_code_old = get_column(line_old, 4)
        village_old = get_column(line_old, 11)
        cases_old = get_column(line_old, 13)

        for line_current in my_current:
            date_current = get_column(line_current, 1)
            district_code_current = get_column(line_current, 4)
            village_current = get_column(line_current, 11)
            cases_current = get_column(line_current, 13)
            if district_code_old == district_code_current:
                if village_old == village_current:
                    if date_old == date_current:
                        if cases_old == cases_current:
                            break
                        else:
                            if abs(int(cases_current)-int(cases_old)) >= 10:
                                print(f"{village_old} old:\t\t{date_old} - {cases_old}")
                                print(f"{village_current} current:\t{date_current} - {cases_current}")
                                print("---")
    print(f"Thread {thread_number} exited")


cores = 8

one_range = round(len(old) / cores)
last_range = 0
applied = 0

for i in range(cores):
    applied += one_range
    if i+1 == cores:
        p = Process(target=work, args=(old[last_range:(last_range + one_range)],
                                       current[last_range:(last_range + one_range)], i))
    else:
        p = Process(target=work, args=(old[last_range:], current[last_range:], i))
    p.start()
