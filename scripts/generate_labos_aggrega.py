#!/usr/bin/env python

from csv import reader

with open("data/public/labos.departements.csv") as f:
    data = list(reader(f))

output = {}
keys = data.pop(0)
keys.remove("LABO")
keys.remove("DEPARTEMENT")
for row in data:
    if not row[0]:
        continue
    if row[0] not in output:
        output[row[0]] = dict({k: 0 for k in keys})
    for i, k in enumerate(keys):
        output[row[0]][k] += float(row[2+i]) if row[2+i] else 0

print "LABO,"+",".join(keys)
for labo in output:
    print labo+","+",".join([str(output[labo][k]) for k in keys])
