# -*- coding: utf-8 -*-

import pandas as pd
import sys
import string
import re

header_mapping = {
    'ORIGIN': 'ORIGIN',
    'LABO': 'LABO',
    'NOM_PRENOM': 'BENEF_PS_QUALITE_NOM_PRENOM',
    'ADDRESS': 'BENEF_PS_ADR',
    'QUALITE': 'BENEF_PS_QUALIFICATION',
    'MONTANT': 'DECL_AVANT_MONTANT',
    'DATE': 'DECL_AVANT_DATE',
    'AVANTAGE': 'DECL_AVANT_NATURE',
    'BENEF_PS_CODEPOSTAL': 'BENEF_PS_CODEPOSTAL'
}
input_filename = sys.argv[1]
output_filename = sys.argv[2]
df = pd.read_csv(input_filename, sep=';', encoding='utf-8')

df['NOM_PRENOM'] = df['NOM'] + ' ' + df['PRENOM']
df['ADDRESS'] = df['VILLE'] + ' ' + df['CP'].apply(lambda cp: int(cp) if not pd.np.isnan(cp) else pd.np.nan).apply(str)
df['ORIGIN'] = 'Dentiste'
df['DATE'] = df['DATE'].apply(str).apply(lambda date: '-'.join(reversed(string.split(date, '/'))) if date.find('/') else date )
df['BENEF_PS_CODEPOSTAL'] = df['ADDRESS'].apply(lambda s: s.encode('ascii', errors='ignore')  if isinstance(s, unicode) else str(s) ).apply(lambda addr: re.sub( '(.* |^)([0-9]{4,5})[ \.].*', '\g<2>', addr).zfill(5)).apply(lambda s: s if (re.match('^[0-9]{5}$', s)) else '')

for origin, target in header_mapping.items():
    df[target] = df[origin]

df[header_mapping.values()].to_csv(output_filename, index=False, encoding='utf-8')

