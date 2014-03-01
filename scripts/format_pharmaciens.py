# -*- coding: utf-8 -*-

import pandas as pd
import sys

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
}

input_filename = sys.argv[1]
output_filename = sys.argv[2]

df = pd.read_csv(input_filename, encoding='utf-8')

df['lastname_firstname'] = df['name'] + ' ' + df['firstname']
df['origin'] = 'Pharmacien'

for origin, target in header_mapping.items():
    df[target] = df[origin]

df[header_mapping.values()].to_csv(output_filename, index=False, encoding='utf-8')
