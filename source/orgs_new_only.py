import csv
import httpx


known_orgs = []
with open("orgs.csv") as f:
    for line in csv.reader(f, delimiter=",", quotechar='"'):
        if line[0].startswith("https://"):
            known_orgs.append(line[0])

new_orgs = []
with open("orgs_2025_08.csv") as f:
    for line in csv.reader(f, delimiter=",", quotechar='"'):
        if line[0].startswith("https://"):
            if line[0] not in known_orgs:
                new_orgs.append(line[0])

for o in new_orgs:
    print(o)