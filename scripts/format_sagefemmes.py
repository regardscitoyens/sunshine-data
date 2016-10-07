# -*- coding: utf-8 -*-

import pandas as pd
import sys
import re

from utils import find_zipcode

input_filename = sys.argv[1]
output_filename = sys.argv[2]
df = pd.read_csv(input_filename, sep=';', encoding='utf-8')

df['DECL_DATE'] = df['DECL_DATE'].apply(str).apply(lambda date: '-'.join(reversed(date.split('/'))) if date.find('/') else date)
df['DECL_CONV_DATE'] = df['DECL_CONV_DATE'].apply(str).apply(lambda date: '-'.join(reversed(date.split('/'))) if date.find('/') else date)
df['DECL_AVANT_DATE'] = df['DECL_AVANT_DATE'].apply(str).apply(lambda date: '-'.join(reversed(date.split('/'))) if date.find('/') else date)
df['BENEF_PS_QUALITE_NOM_PRENOM'] = df['BENEF_PS_QUALITE_NOM_PRENOM'].apply(str).apply(lambda nom: ' '.join(reversed(re.sub(' ([A-Z][A-Z ]*)', '@\g<1>', nom.replace('Sage-femme ', '').replace('Sage femme ', '')).split('@'))))


def nomprenomtwice(nom):
    anom = nom.split(' ')
    if anom[int(len(anom)/2)] != anom[0]:
        return nom.upper()
    return ' '.join(anom[0:int(len(anom)/2)]).upper()

df['BENEF_PS_QUALITE_NOM_PRENOM'] = df['BENEF_PS_QUALITE_NOM_PRENOM'].apply(lambda nom: nomprenomtwice(nom))
df['BENEF_PS_QUALIFICATION'] = 'Sage-femme'
df['BENEF_PS_CODEPOSTAL'] = df['BENEF_PS_ADR'].apply(find_zipcode)
df['DECL_AVANT_NATURE'] = df['DECL_AVANT_NATURE'].str.replace(',', '-').replace('"', '')

df.to_csv(output_filename, index=False, encoding='utf-8')

