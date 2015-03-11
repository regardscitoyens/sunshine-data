# -*- coding: utf-8 -*-

import pandas as pd

DIRECTORY_FILEPATH = 'data/unifier/RPPS_DIRECTORY.csv'

directory = pd.read_csv(DIRECTORY_FILEPATH, dtype=object, encoding='utf-8')

for filename in ["dentistes.refined.csv",
                 "infirmiers.refined.csv",
                 "medecins_exploitables.refined.csv",
                 "medecins_inexploitables.refined.csv",
                 "pharmaciens.refined.csv",
                 "transparencesante_avantages.refined.csv",
                 "sagefemmes.refined.csv",
                 "transparencesante_conventions.refined.csv"]:

    df = pd.read_csv("data/refined/%s" % filename, dtype=object, encoding='utf-8', usecols=["BENEF_PS_QUALITE_NOM_PRENOM", "BENEF_PS_RPPS"])
    df = df.dropna()
    df.BENEF_PS_QUALITE_NOM_PRENOM = df.BENEF_PS_QUALITE_NOM_PRENOM.str.strip()
    df_by_name = df.groupby("BENEF_PS_QUALITE_NOM_PRENOM").first()
    df_by_name.reset_index(level=0, inplace=True)

    directory = directory.append(df_by_name).groupby("BENEF_PS_QUALITE_NOM_PRENOM").first()
    directory.reset_index(level=0, inplace=True)

directory.to_csv(DIRECTORY_FILEPATH, encoding='utf-8', index=False)
