# -*- coding: utf-8 -*-
import sys, os, re
import pandas as pd
import numpy as np

input_filename = sys.argv[1]
operation_dirname = sys.argv[2]
output_filename = sys.argv[3]

columns = ['ORIGIN','LABO','BENEF_PS_QUALITE_NOM_PRENOM','BENEF_PS_ADR','BENEF_PS_QUALIFICATION','BENEF_PS_RPPS','DECL_CONV_DATE','DECL_CONV_OBJET','DECL_CONV_PROGRAMME','DECL_AVANT_MONTANT','DECL_AVANT_DATE','DECL_AVANT_NATURE','BENEF_ETUD_ETA']

df = pd.read_csv(input_filename, encoding='utf-8', low_memory=False)
for dirname, dirnames, filenames in os.walk(operation_dirname):
    # print path to all filenames.
    for filename in filenames:
        operation_filename = os.path.join(dirname, filename)
        if not re.search('csv$', operation_filename):
            continue
        operation_field = re.sub('.*/([^\.]*)\.csv', '\\1', operation_filename)
        operations = pd.read_csv(open(operation_filename), encoding='utf-8', index_col=0, squeeze=True, header=None)
        df[operation_field] = df[operation_field].fillna(u'Non renseigné')
        keys = np.unique(np.append(df[operation_field].unique(), operations.index.values))
        
        operations = operations.reindex(keys).fillna(value='UNKNOWN')
#        operations[operations.values == 'UNKNOWN'] = operations[operations.values == 'UNKNOWN'].index
        operations.to_csv(operation_filename+".new", encoding='utf-8')
        
        df[operation_field] = df[operation_field].apply(lambda labo: operations[labo])
        
        for col in columns:
            df[col] = df.get(col, '')
df.loc[df['DECL_AVANT_MONTANT'] > 1,'DECL_CONV_OBJET'] = ''
df.loc[df['DECL_AVANT_MONTANT'] > 1,'DECL_CONV_PROGRAMME'] = ''
df.to_csv(output_filename, encoding='utf-8', index=False, cols=columns)
