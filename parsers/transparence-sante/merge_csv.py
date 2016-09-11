# -*- coding: utf-8 -*-
import glob
import re,csv

count = 0
out = csv.writer(open('data/avantages.csv','wb'))
out.writerow("entreprise,type_beneficiaire,beneficiaire,date,nature,montant,code_postal_beneficaire".split(','))
for path in glob.glob('./raw/*.csv'):
    with open(path) as csv:
        for line in csv:
            line = line.replace('"','')
            data = line.split(',')
            postal_code = path.split('/')[-1].split('.')[0]

            if len(data) < 5:
                print "corrupt data",data,postal_code
                continue

            if data[1].startswith(" "):
                data = [data[0] + data[1]]+data[2:]

            nature_index = 4
            montant_index = None
            for i, el in enumerate(data):
                if i > nature_index and '\xe2\x82\xac' in el:
                    montant_index = i
                    break

            if not montant_index:
                montant_index = len(data)-3
            data = data[:nature_index]+[','.join(data[nature_index:montant_index])]+[''.join(data[montant_index:])]
 

            if not data[nature_index]:
                print 'na nature',data,line
                continue
            
            if data[2] == "Médecin":
                print "oops, Médecin is my name",data,line

            if len(data) != 6:
                print 'invadlid data',data
                import pdb;pdb.set_trace()
            try:
                data[5] = re.sub("[^0-9]", "", data[5])
                int(data[5])
            except:
                print 'invalide montant', data[5],data
                import pdb;pdb.set_trace()

            out.writerow(data+[postal_code])
            count += 1
print(count)
