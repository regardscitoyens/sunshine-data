# -*- coding: utf-8 -*-
import sys, os, re
import pandas as pd
import numpy as np

input_filename = sys.argv[1]
operation_field = sys.argv[2]
operation_filename = sys.argv[3]


df = pd.read_csv(input_filename, encoding='utf-8', low_memory=False)
keys = df[operation_field].unique()
operations = pd.DataFrame({'key':keys, 'value':keys})
operations.to_csv(os.path.join(operation_filename), encoding='utf-8', index=False, header=0)
