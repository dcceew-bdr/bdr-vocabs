import csv



iris = []
with open("orgs.desc.csv") as f:
    for line in csv.reader(f, delimiter=",", quotechar='"'):
        print(f'<{line[0]}> skos:definition """{line[1]}"""@en .')