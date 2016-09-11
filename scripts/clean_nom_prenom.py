# -*- coding: utf-8 -*-

import re
import pandas as pd
from unidecode import unidecode

from utils import Fingerprinter

clean_re = re.compile("^((DR(.)?)|TITRE|STOMATOLOGUE|-MR|MR|0|A|MEDECIN|DOCTEUR|DENTISTE|IDE|MADAME|MONSIEUR|DOCTEUR|PROFESSEUR|INFIRMIER|DRS)\s")


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


def get_fingerprint_ngram(string):
    if not pd.isnull(string):
        return Fingerprinter(string).get_ngram_fingerprint(n=2)
    return string


def clean_name(name):
    if pd.isnull(name):
        return name
    return clean_re.sub('', nomprenomtwice(unidecode(name).strip().upper()))

df = pd.read_csv("data/all.csv", dtype=object, encoding='utf-8', usecols=["BENEF_PS_QUALITE_NOM_PRENOM"])

df["BENEF_PS_QUALITE_NOM_PRENOM"] = df.BENEF_PS_QUALITE_NOM_PRENOM.apply(clean_name)
df["fingerprint"] = df.BENEF_PS_QUALITE_NOM_PRENOM.apply(get_fingerprint)

unifier = {}

for _, rows in df.groupby(["fingerprint"]):
    names = sorted(rows.BENEF_PS_QUALITE_NOM_PRENOM.unique(), lambda x,y: cmp(len(x), len(y)))
    if len(names) > 1:
        reference = names[0]
        for name in names[1:]:
            if len(reference) > 0:
                unifier[reference] = name

df.drop("fingerprint", axis=1, inplace=True)
df["fingerprint_ngram"] = df.BENEF_PS_QUALITE_NOM_PRENOM.apply(nomprenomtwice).apply(get_fingerprint_ngram)
gp = df.groupby(["fingerprint_ngram"])

for _, rows in gp:
    names = sorted(rows.BENEF_PS_QUALITE_NOM_PRENOM.unique(), lambda x,y: cmp(len(x), len(y)))
    if len(names) > 1:
        reference = names[0]
        for name in names[1:]:
            if len(name[0]) > 0:
                unifier[reference] = name

df.drop("fingerprint_ngram", axis=1, inplace=True)

with open('unifier.csv', 'w') as f:
    f.write("\n".join([",".join(item) for item in unifier.iteritems()]))

del unifier
del gp

df_all = pd.read_csv("data/all.csv", dtype=object, encoding='utf-8', na_filter=False)
df_all["BENEF_PS_QUALITE_NOM_PRENOM"] = df["BENEF_PS_QUALITE_NOM_PRENOM"]
df_all.to_csv("data/all.clean.names.csv", index=False, encoding="utf-8")
