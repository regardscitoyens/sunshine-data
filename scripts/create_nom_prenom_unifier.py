# -*- coding: utf-8 -*-

import pandas as pd
from unidecode import unidecode

df = pd.DataFrame()

from utils import Fingerprinter


def nomprenomtwice(nom):
    if not pd.isnull(nom):
        anom = nom.split(' ')
        if anom[len(anom)/2] != anom[0]:
            return nom.upper()
        return ' '.join(anom[0:len(anom)/2]).upper()
    return nom


def get_fingerprint(string):
    if not pd.isnull(string):
        return Fingerprinter(string).get_fingerprint()
    return string

for filename in ["dentistes.refined.csv",
                 "infirmiers.refined.csv",
                 "medecins_exploitables.refined.csv",
                 "medecins_inexploitables.refined.csv",
                 "pharmaciens.refined.csv",
                 "sagefemmes.refined.csv"]:

    newdf = pd.read_csv("data/refined/%s" % filename, dtype=object, encoding='utf-8', usecols=["BENEF_PS_QUALITE_NOM_PRENOM"])
    if df is None:
        df = newdf

    else:
        df = df.append(newdf)

df["fingerprint"] = df.BENEF_PS_QUALITE_NOM_PRENOM.apply(nomprenomtwice).apply(get_fingerprint)

gp = df.groupby(["fingerprint"])

unifier = []

for group_name, rows in gp:
    names = sorted(rows.BENEF_PS_QUALITE_NOM_PRENOM.unique(), lambda x,y: cmp(len(x), len(y)))
    if len(names) > 1:
        reference = names[0]
        for name in names[1:]:
            fixed_name = nomprenomtwice(unidecode(reference).strip().upper())
            if len(fixed_name) > 0:
                unifier.append(",".join([name.encode('utf-8'), fixed_name]))

print "\n".join(unifier)