# -*- coding: utf-8 -*-
import sys
import pandas as pd
import numpy as np
import json

input_filename = sys.argv[1]
operation_filename = sys.argv[2]
operation_field = sys.argv[3]
output_filename = sys.argv[4]

df = pd.read_csv(input_filename, encoding='utf-8')
operations = pd.read_csv(open(operation_filename), encoding='utf-8', index_col=0, squeeze=True )
df[operation_field] = df[operation_field].fillna('UNKNOWN')
keys = np.unique(np.append(df[operation_field].unique(), operations.index.values))

operations = operations.reindex(keys).fillna(value='UNKNOWN')
operations.to_csv(operation_filename+".new", encoding='utf-8')
df[operation_field] = df[operation_field].apply(lambda labo: operations[labo])

df.to_csv(output_filename, encoding='utf-8', index=False)


