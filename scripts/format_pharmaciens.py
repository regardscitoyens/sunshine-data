# -*- coding: utf-8 -*-

import pandas as pd
import sys
import re

header_mapping = {
    'origin': 'ORIGIN',
    'company_name': 'LABO',
    'lastname_firstname': 'BENEF_PS_QUALITE_NOM_PRENOM',
    'address': 'BENEF_PS_ADR',
    'job': 'BENEF_PS_QUALIFICATION',
    'rpps': 'BENEF_PS_RPPS',
    'value': 'DECL_AVANT_MONTANT',
    'date': 'DECL_AVANT_DATE',
    'kind': 'DECL_AVANT_NATURE',
    'BENEF_PS_CODEPOSTAL': 'BENEF_PS_CODEPOSTAL'
}

input_filename = sys.argv[1]
output_filename = sys.argv[2]

df = pd.read_csv(input_filename, encoding='utf-8')

df['lastname_firstname'] = df['name'] + ' ' + df['firstname']
df['origin'] = 'Pharmacien'
df['BENEF_PS_CODEPOSTAL'] = df['address'].apply(lambda s: s.encode('ascii', errors='ignore')  if isinstance(s, unicode) else str(s) ).apply(lambda addr: re.sub( '(^|.* )([0-9]{4,5})[ \.].*', '\g<2>', addr).zfill(5)).apply(lambda s: s if (re.match('^[0-9]{5}$', s)) else '')

for origin, target in header_mapping.items():
    df[target] = df[origin]

df[header_mapping.values()].to_csv(output_filename, index=False, encoding='utf-8')
