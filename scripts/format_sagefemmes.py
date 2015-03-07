# -*- coding: utf-8 -*-

import pandas as pd
import sys
import string
import re

input_filename = sys.argv[1]
output_filename = sys.argv[2]
df = pd.read_csv(input_filename, sep=';', encoding='utf-8')

df['DECL_DATE'] = df['DECL_DATE'].apply(str).apply(lambda date: '-'.join(reversed(string.split(date, '/'))) if date.find('/') else date)
df['DECL_CONV_DATE'] = df['DECL_CONV_DATE'].apply(str).apply(lambda date: '-'.join(reversed(string.split(date, '/'))) if date.find('/') else date)
df['DECL_AVANT_DATE'] = df['DECL_AVANT_DATE'].apply(str).apply(lambda date: '-'.join(reversed(string.split(date, '/'))) if date.find('/') else date)
df['BENEF_PS_QUALITE_NOM_PRENOM'] = df['BENEF_PS_QUALITE_NOM_PRENOM'].apply(str).apply(lambda nom: ' '.join(reversed(string.split(re.sub(' ([A-Z][A-Z ]*)', '@\g<1>', nom.replace('Sage-femme ', '').replace('Sage femme ', '')), '@'))))
def nomprenomtwice(nom):
    anom = string.split(nom, ' ')
    if anom[len(anom)/2] != anom[0]:
        return nom.upper()
    return ' '.join(anom[0:len(anom)/2]).upper()

df['BENEF_PS_QUALITE_NOM_PRENOM'] = df['BENEF_PS_QUALITE_NOM_PRENOM'].apply(lambda nom: nomprenomtwice(nom))
df['BENEF_PS_QUALIFICATION'] = 'Sage-femme'
df['BENEF_PS_CODEPOSTAL'] = df['BENEF_PS_ADR'].apply(lambda s: s.encode('ascii', errors='ignore')  if isinstance(s, unicode) else str(s) ).apply(lambda addr: re.sub( '.* ([0-9]{5})[ \.].*', '\g<1>', addr)).apply(lambda s: s if (len(s) == 5) else '')
df['DECL_AVANT_NATURE'] = df['DECL_AVANT_NATURE'].apply(lambda s: s.encode('ascii', errors='ignore')  if isinstance(s, unicode) else str(s) ).apply(lambda s: s.replace(',', ' -'))

df.to_csv(output_filename, index=False, encoding='utf-8')

