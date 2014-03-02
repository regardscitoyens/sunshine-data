# -*- coding: utf-8 -*-

import pandas as pd
import sys

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
    'MONTANT_AVANTAGE': 'DECL_AVANT_MONTANT',
    'DATE_AVANTAGE': 'DECL_AVANT_DATE',
    'NATURE_AVANTAGE': 'DECL_AVANT_NATURE',
}

input_filename = sys.argv[1]
output_filename = sys.argv[2]

df = pd.read_csv(input_filename, sep=';', encoding='utf-8')

df['QUALITE_NOM_PRENOM'] = df['QUALITE'] + ' ' + df['NOM'] + ' ' + df['PRENOM']
df['ORIGIN'] = 'Infirmier'

for origin, target in header_mapping.items():
    df[target] = df[origin]

df[header_mapping.values()].to_csv(output_filename, index=False, encoding='utf-8')
