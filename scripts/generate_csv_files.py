# -*- coding: utf-8 -*-

import pandas as pd

df = pd.read_csv("data/all.anonymes.csv", dtype=object, encoding='utf-8')

df['DECL_AVANT_MONTANT'] = df.DECL_AVANT_MONTANT.astype('float32')

# by LABO
labos = df.groupby(['LABO', 'BENEF_PS_DEPARTEMENT', 'DECL_TYPE']).agg({'DECL_AVANT_MONTANT': {'DECL_AVANT_SOMME': 'sum', 'DECL_AVANT_NOMBRE': 'count'}})
labos.columns = labos.columns.droplevel(0)
labos.to_csv('public/labos.csv', encoding='utf-8')

# by ORIGIN
origins = df.groupby(['ORIGIN', 'BENEF_PS_DEPARTEMENT', 'DECL_TYPE']).agg({'DECL_AVANT_MONTANT': {'DECL_AVANT_SOMME': 'sum', 'DECL_AVANT_NOMBRE': 'count'}})
origins.columns = origins.columns.droplevel(0)
origins.to_csv('public/origins.csv', encoding='utf-8')

# by DECL_AVANT_NATURE
natures = df.groupby(['DECL_AVANT_NATURE', 'BENEF_PS_DEPARTEMENT', 'DECL_TYPE']).agg({'DECL_AVANT_MONTANT': {'DECL_AVANT_SOMME': 'sum', 'DECL_AVANT_NOMBRE': 'count'}})
natures.columns = natures.columns.droplevel(0)
natures.to_csv('public/natures.csv', encoding='utf-8')