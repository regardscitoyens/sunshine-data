# -*- coding: utf-8 -*-

import pandas as pd

all_df = None

for filename in ["dentistes.refined.csv",
                 "infirmiers.refined.csv",
                 "medecins_exploitables.refined.csv",
                 "medecins_inexploitables.refined.csv",
                 "pharmaciens.refined.csv",
                 "transparencesante_avantages.refined.csv",
                 "sagefemmes.refined.csv",
                 "transparencesante_conventions.refined.csv"]:

    df = pd.read_csv("data/refined/%s" % filename, dtype=object, encoding='utf-8', usecols=["DECL_TYPE", "ORIGIN", "LABO", "BENEF_PS_QUALITE_NOM_PRENOM", "DECL_CONV_DATE", "DECL_AVANT_DATE", "DECL_AVANT_MONTANT"])
    if all_df is None:
        all_df = df
    else:
        all_df = all_df.append(df)

print("Number of duplicated rows : " % all_df.duplicated().sum())