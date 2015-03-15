#!/bin/bash

echo 'BENEFICIAIRE,DEPARTEMENT,NB TOTAL CONVENTIONS + AVANTAGES,NB CONVENTIONS,NB AVANTAGES,MONTANT AVANTAGES' > data/public/beneficiaires.top.csv
sort -k 8,8 -t ',' -n -r data/public/beneficiaires.csv  | grep -v ',,' | head -n 5000 | awk -F ',' '{print $2" "$1" ("$3"),"$4","$5","$6","$7","$8}' | sed 's/ \(.....\)[^ ]* (/ \1 (/' >> data/public/beneficiaires.top.csv
