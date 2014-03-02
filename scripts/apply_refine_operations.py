# -*- coding: utf-8 -*-
import sys
import pandas as pd
import json

input_filename = sys.argv[1]
refine_filename = sys.argv[2]
output_filename = sys.argv[3]

df = pd.read_csv(input_filename, encoding='utf-8')
operations = json.load(open(refine_filename))

def apply_refine_operation(operation):
    # At this time, handle only "core/mass-edit"
    if operation['op'] == 'core/mass-edit':
        column = operation['columnName']
        for edit in operation['edits']:
            def transform(value):
                if value in edit['from']:
                    return edit['to']
            df[column] = df[column].apply(transform)

    elif operation['op'] == 'core/text-transform':
        column = operation['columnName']
        if 'jython' in operation['expression']:
            # XXX: I know this fucking bad...
            myfunction_str = 'def my_operation(value):%s'%operation['expression'].split('jython:')[1]
            exec myfunction_str in globals(), locals()
            df[column] = df[column].apply(my_operation)
        else:
            print operation
            raise "handle only jython function"
    else:
        print operation
        raise 'operation not yet handled'

for operation in operations:
    apply_refine_operation(operation)

df.to_csv(output_filename, encoding='utf-8', index=False)


