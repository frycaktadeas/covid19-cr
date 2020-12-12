import matplotlib.pyplot as plt
import numpy as np
import json

DATE = "2020-11-06"
x, y, z = [], [], []

with open("data/final/location.json", "r") as f:
    location = json.load(f)

with open("data/final/cases.json", "r") as f:
    cases_content = json.load(f)

cases = {}

# For every region in cases file
for region in cases_content:
    cases[region] = {}
    # For every district in region
    for district in cases_content[region]:
        cases[region][district] = {}
        # For every village in district
        for village in cases_content[region][district]:
            # Get village name without district in brackets
            real_name_village = village.split(" (")[0]
            for date in cases_content[region][district][village]:
                if date == DATE:
                    cases[region][district][village] = cases_content[region][district][village][date][1]

for num, i in enumerate(location.values()):
    x.append(i[0])
    y.append(i[1])
    village_name = list(location.keys())[num]

    # For every region in cases file
    for region in cases:
        # For every district in region
        for district in cases[region]:
            # For every village in district
            for village in cases[region][district]:
                # Get village name without district in brackets
                real_name_village = village.split(" (")[0]
                if village_name == real_name_village:
                    z.append(cases[region][district][village])
                    break
            else:
                continue
            break
        else:
            continue
        break
    else:
        z.append(0)
fig = plt.figure()
ax1 = fig.add_subplot(111, projection='3d')
print(len(x))
print(len(y))
print(len(z))
ax1.bar3d(x, y, z, 0.001, 0.001, 0.001)

ax1.set_xlabel('x axis')
ax1.set_ylabel('y axis')
ax1.set_zlabel('z axis')

plt.show()
