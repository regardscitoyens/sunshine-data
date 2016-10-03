# -*- coding: utf-8 -*-

import pandas as pd
import sys
from utils import find_zipcode, euro2float, str2date
from builtins import str as text

header_mapping = {
    'ORIGIN': 'ORIGIN',
    'LABO': 'LABO',
    'QUALITE_NOM_PRENOM': 'BENEF_PS_QUALITE_NOM_PRENOM',
    'ADRESSE': 'BENEF_PS_ADR',
    'QUALIFICATION': 'BENEF_PS_QUALIFICATION',
    'MONTANT_AVANTAGE': 'DECL_AVANT_MONTANT',
    'DATE_AVANTAGE': 'DECL_AVANT_DATE',
    'NATURE_AVANTAGE': 'DECL_AVANT_NATURE',
    'SPECIALITE': 'BENEF_PS_SPECIALITE',
    'NUMERO_ORDINAL': 'BENEF_PS_RPPS',
    'DATE_SIGNATURE_CONVENTION': 'DECL_CONV_DATE',
    'OBJET': 'DECL_CONV_OBJET',
    'PROGRAMME': 'DECL_CONV_PROGRAMME',
    'BENEF_PS_CODEPOSTAL': 'BENEF_PS_CODEPOSTAL'
}

input_filename = sys.argv[1]
output_filename = sys.argv[2]

df = pd.read_csv(input_filename, sep=';', encoding='utf-8')

df['MONTANT_AVANTAGE'] = df['MONTANT_AVANTAGE'].apply(euro2float)
df['DATE_AVANTAGE'] = df['DATE_AVANTAGE'].apply(str2date)
df['DATE_SIGNATURE_CONVENTION'] = df['DATE_SIGNATURE_CONVENTION'].apply(str2date)
df['QUALITE_NOM_PRENOM'] = df['QUALITE'] + ' ' + df['NOM'] + ' ' + df['PRENOM']
df['ORIGIN'] = 'Infirmier'
df['BENEF_PS_CODEPOSTAL'] = df['ADRESSE'].apply(find_zipcode)

for origin, target in header_mapping.items():
    df[target] = df[origin]
    df[target] = df[target].apply(text).apply(lambda s: s.replace(',', '- ').replace('"', ''))

df[list(header_mapping.values())].to_csv(output_filename, index=False, encoding='utf-8')
