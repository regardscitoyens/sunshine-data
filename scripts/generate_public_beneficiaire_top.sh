#!/bin/bash

echo 'BENEFICIAIRE,DEPARTEMENT,NB TOTAL CONVENTIONS + AVANTAGES,NB CONVENTIONS,NB AVANTAGES,MONTANT AVANTAGES' > data/public/beneficiaires.top.csv
sed 1d data/public/beneficiaires.csv | sort -k 8,8 -t ',' -n -r | grep -v ',Asso d' | grep -v ',Fondation,' | grep -v 'personne morale,' | grep -v ',Etablissement de ' | head -n 5000 | awk -F ',' '{print $2" "$1" ("$3"),"$4","$5","$6","$7","$8}' | sed 's/ \(.....\)[^ ]* (/ \1 (/' | sed 's/(Chirurgie[^)]*)/(Chirurgie)/' >> data/public/beneficiaires.top.csv
