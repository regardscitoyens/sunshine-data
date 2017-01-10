#!/bin/bash

awk -F ',' '{print $24";"$8}' data/all.unames.csv  | grep -v '^;' | sort -u | sed 's/;.*/;/'  | uniq -c | sed 's/^ *//' | sed 's/ /;/'  > /tmp/finess_ps_avec_liens.csv
sort -t ';' -k 2,2 /tmp/finess_ps_avec_liens.csv > /tmp/finess_ps_avec_liens.sorted.csv
awk -F ';' '{print $19}' data/rpps.csv | sed 's/"//g' | sort | uniq -c | sed 's/^ *//' | sed 's/ /;/'  > /tmp/finess_rpps.csv
sort -t ';' -k 2,2 /tmp/finess_rpps.csv > /tmp/finess_rpps.sorted.csv
join -t ';' -1 2 -2 2 /tmp/finess_ps_avec_liens.sorted.csv /tmp/finess_rpps.sorted.csv > /tmp/comparaison_finess.csv
echo "FINESS;Nombre de praticiens ayant au moins un lien avec un labo entre 2012 et 2016;Nombre de praticiens dans cet établissement;% de praticiens ayant des liens avec les labos" > data/comparaison_liens_finess.csv
awk -F ';' '{print $1";"$2";"$4";"$2/$4}' /tmp/comparaison_finess.csv | sort -t ';' -k 3,4 -n -r >> data/comparaison_liens_finess.csv
rm /tmp/finess_ps_avec_liens.csv /tmp/finess_ps_avec_liens.sorted.csv /tmp/finess_rpps.csv /tmp/finess_rpps.sorted.csv /tmp/comparaison_finess.csv
