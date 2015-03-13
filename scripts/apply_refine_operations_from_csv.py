# -*- coding: utf-8 -*-
import sys, os, re
import pandas as pd
import numpy as np

input_filename = sys.argv[1]
operation_dirname = sys.argv[2]
output_filename = sys.argv[3]

columns = ['DECL_TYPE', 'ORIGIN','LABO','BENEF_PS_QUALITE_NOM_PRENOM','BENEF_PS_CODEPOSTAL','BENEF_PS_ADR','BENEF_PS_QUALIFICATION','BENEF_PS_RPPS','DECL_CONV_DATE','DECL_CONV_OBJET','DECL_CONV_PROGRAMME','DECL_AVANT_MONTANT','DECL_AVANT_DATE','DECL_AVANT_NATURE','BENEF_ETUD_ETA']

df = pd.read_csv(input_filename, dtype=object, encoding='utf-8')

df['DECL_AVANT_MONTANT'] = df.DECL_AVANT_MONTANT.astype('float32')

for col in columns:
    df[col] = df.get(col, '')

for dirname, dirnames, filenames in os.walk(operation_dirname):
    for filename in filenames:
        operation_filename = os.path.join(dirname, filename)

        if not re.search('csv$', operation_filename):
            continue

        print "operation filename", operation_filename

        operation_field = re.sub('.*/([^\.]*)\.csv', '\\1', operation_filename)
        operations = pd.read_csv(open(operation_filename), encoding='utf-8', index_col=0, squeeze=True, header=None)
        df[operation_field] = df[operation_field].fillna('')
        keys = np.unique(np.append(df[operation_field].unique(), operations.index.values))

        operations = operations.groupby(level=0).first().reindex(keys).fillna('')

        df[operation_field] = df[operation_field].apply(lambda labo: operations[labo])
        
df['DECL_TYPE'] = ''

if input_filename == 'data/formatted/transparencesante_avantages.formatted.csv':
    df['DECL_TYPE'] = 'AVANTAGE'
elif input_filename == 'data/formatted/transparencesante_conventions.formatted.csv':
    df['DECL_TYPE'] = 'CONVENTION'
else:
    MIN_HONORAIRE_FOR_CONVENTION = 1000

    df.loc[(df['DECL_CONV_OBJET'] == "COLLABORATION SCIENTFIQUE") & (df['DECL_AVANT_MONTANT'] > MIN_HONORAIRE_FOR_CONVENTION), 'DECL_TYPE'] = 'CONVENTION'
    df.loc[(df['DECL_CONV_OBJET'] == "ORATEUR/FORMATEUR") & (df['DECL_AVANT_MONTANT'] > MIN_HONORAIRE_FOR_CONVENTION), 'DECL_TYPE'] = 'CONVENTION'
    df.loc[(df['DECL_AVANT_NATURE'] == "TRANSPORT"), 'DECL_TYPE'] = 'AVANTAGE'

    df.loc[(df['DECL_TYPE'] != 'CONVENTION') & (df['DECL_AVANT_MONTANT'] < 5000) & (df['DECL_AVANT_MONTANT'] >= 1), 'DECL_TYPE'] = 'AVANTAGE'
    df.loc[(df['DECL_AVANT_DATE'].isnull()) & (df['DECL_TYPE'] != "AVANTAGE"), 'DECL_TYPE'] = 'CONVENTION'
    df.loc[(df['DECL_TYPE'] != 'AVANTAGE') & (df['DECL_AVANT_DATE'].isnull()) & (df['DECL_AVANT_MONTANT'].isnull()) & (df['DECL_CONV_OBJET'].notnull()), 'DECL_TYPE'] = 'CONVENTION'

    df.loc[(df['DECL_AVANT_NATURE'] == "HONORAIRES") & (df['DECL_AVANT_MONTANT'] > MIN_HONORAIRE_FOR_CONVENTION), 'DECL_TYPE'] = 'CONVENTION'
    df.loc[(df['DECL_TYPE'].isnull()), 'DECL_TYPE'] = 'AVANTAGE'

    df.loc[(df['DECL_CONV_OBJET'] == "CONTRAT DE CESSION"), 'DECL_TYPE'] = 'CONVENTION'
    df.loc[(df['DECL_CONV_OBJET'] == "CONTRAT DE CONSULTANT"), 'DECL_TYPE'] = 'CONVENTION'
    df.loc[(df['DECL_CONV_OBJET'] == "ÉTUDE DE MARCHÉ") & (df['DECL_AVANT_MONTANT'] > MIN_HONORAIRE_FOR_CONVENTION), 'DECL_TYPE'] = 'CONVENTION'
    
df.loc[(df['DECL_TYPE'] == "AVANTAGE"), 'DECL_CONV_OBJET'] = ''
df.loc[(df['DECL_TYPE'] == "AVANTAGE"), 'DECL_CONV_PROGRAMME'] = ''
df.loc[(df['DECL_TYPE'] == "AVANTAGE"), 'DECL_CONV_DATE'] = ''

selection = df.loc[(df['DECL_TYPE'] == "CONVENTION") & (df['DECL_AVANT_NATURE']) & (df['DECL_CONV_OBJET'].isnull()), 'DECL_CONV_OBJET']
if selection.shape[0] > 0:
    df.loc[(df['DECL_TYPE'] == "CONVENTION") & (df['DECL_AVANT_NATURE']) & (df['DECL_CONV_OBJET'].isnull()), 'DECL_CONV_OBJET'] = df['DECL_AVANT_NATURE']

df.loc[(df['DECL_TYPE'] == "CONVENTION"), 'DECL_AVANT_NATURE'] = ''
df.loc[(df['DECL_TYPE'] == "CONVENTION"), 'DECL_AVANT_DATE'] = ''

df.to_csv(output_filename, encoding='utf-8', index=False, cols=columns)
