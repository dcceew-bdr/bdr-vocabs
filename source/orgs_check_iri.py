import csv
import httpx


iris = []
with open("orgs.csv") as f:
    for line in sorted(csv.reader(f, delimiter=",", quotechar='"'), key=lambda x: x[3]):
        if line[1] not in iris:
            iris.append(line[1])

for iri in iris:
    if not iri.startswith("http"):
        continue

    r = httpx.get(iri, follow_redirects=True)

    html = r.text

    if "Page not found" in html:
        print(iri)
