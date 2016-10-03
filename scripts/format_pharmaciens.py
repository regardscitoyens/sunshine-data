# -*- coding: utf-8 -*-

import pandas as pd
import sys

from builtins import str as text
from utils import find_zipcode, str2date

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
df['date'] = df['date'].apply(str2date)
df['BENEF_PS_CODEPOSTAL'] = df['address'].apply(find_zipcode)

for origin, target in header_mapping.items():
    df[target] = df[origin]
    df[target] = df[target].apply(text).apply(lambda s: s.replace(',', '- ').replace('"', ''))

df[list(header_mapping.values())].to_csv(output_filename, index=False, encoding='utf-8')
