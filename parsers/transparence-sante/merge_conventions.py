# -*- coding: utf-8 -*-
import glob
import re,csv

count = 0
out = csv.writer(open('data/conventions.csv','wb'))
out.writerow("entreprise,type_beneficiaire,beneficiaire,date,periode,objet,code_postal_beneficaire".split(','))
for path in glob.glob('./raw_conventions/*.csv'):
    with open(path) as csv:
        for line in csv:
            line = line.replace('"','')
            data = line.split(',')
            postal_code = path.split('/')[-1].split('.')[0]

            if len(data) < 5:
                print "corrupt data",data,postal_code
                continue

            date_index = 5
            size = 6
            data = data[:date_index]+[','.join(x.strip() for x in data[date_index:] if x.strip())]
            out.writerow(data+[postal_code])
            count += 1
print(count)
