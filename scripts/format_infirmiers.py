# -*- coding: utf-8 -*-

import pandas as pd
import sys
import re

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
}

input_filename = sys.argv[1]
output_filename = sys.argv[2]

df = pd.read_csv(input_filename, sep=';', encoding='utf-8')

def euro2float(montant):
    try:
        montant = re.sub(r"[^0-9\.,]", "", re.sub(r",", ".", montant.encode('utf-8')))
        fmontant = float(montant)
    except AttributeError:
        fmontant = float(montant)
    except ValueError:
        fmontant = 0.0
    return fmontant

months = {'jan':'01', 'r s':'01', 'fev': '02', 'mar': '03', 'avr':'04', 'mai':'05', 'uin':'06', 'uil':'07', 'aou':'08', 'aoû':'08', 'sep':'09','oct':'10','nov':'11','dec':'12','déc':'12'}

def humanmonth(match):
    return '20%s-%s-%02d' %  match.group(4)[-2:], months[re.sub('^jui', 'ui', match.group(3).lower())[:3]], int(match.group(2))

def str2date(date):
    try:
        date = re.sub(' ?/ ?', '/', date)
        if (re.search('(^|\D)\d{1,2}/\d{2}/\d{4}', date)):
            return re.sub('(^|.*\D)(\d{1,2})/(\d{2})/(\d{4})', '\g<4>-\g<3>-\g<2>', date)
        if (re.search('.*\d{2}\D\d{2}\D\d{4}.*', date)):
            return re.sub(r'(\d{2})\D(\d{2})\D(\d{4})', '\3-\2-\1', date)
        if (re.search('.*\d{2}\D\d{2}\D\d{2}(\D|$).*', date)):
            return re.sub('.*(\d{2})\D(\d{2})\D(\d{2}).*', '20\3-\2-\1', date)
        if (re.search('\d{1,2}\D\D+\D(20)?\d{2}', date)):
            return re.sub(r'(.*\D|^)(\d{1,2})\D(\D+)\D(\d{2}(\d{2}|$)).*', humanmonth, date)
    except TypeError:
        return ''
    return ''

df['MONTANT_AVANTAGE'] = df['MONTANT_AVANTAGE'].apply(euro2float)
df['DATE_AVANTAGE'] = df['DATE_AVANTAGE'].apply(str2date)
df['DATE_SIGNATURE_CONVENTION'] = df['DATE_SIGNATURE_CONVENTION'].apply(str2date)

df['QUALITE_NOM_PRENOM'] = df['QUALITE'] + ' ' + df['NOM'] + ' ' + df['PRENOM']
df['ORIGIN'] = 'Infirmier'

for origin, target in header_mapping.items():
    df[target] = df[origin]

print df['DECL_AVANT_MONTANT'].sum()

df[header_mapping.values()].to_csv(output_filename, index=False, encoding='utf-8')
