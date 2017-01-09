#!/bin/bash

head -n 1 data/refined/dentistes.refined.csv > data/all.csv
sed -i 's/$/,SOURCE/' data/all.csv
sed 1d data/refined/dentistes.refined.csv | sed 's/$/,ORDRE_DENTISTES/' >> data/all.csv
sed 1d data/refined/infirmiers.refined.csv | sed 's/$/,ORDRE_INFIRMIERS/' >> data/all.csv
sed 1d data/refined/medecins_exploitables.refined.csv | sed 's/$/,ORDRE_MEDECINS_SITE/' >> data/all.csv
sed 1d data/refined/medecins_inexploitables.refined.csv | sed 's/$/,ORDRE_MEDECINS_FICHIERS/' >> data/all.csv
sed 1d data/refined/pharmaciens.refined.csv | sed 's/$/,ORDRE_PHARMACIENS/' >> data/all.csv
sed 1d data/refined/sagefemmes.refined.csv | sed 's/$/,ORDRE_SAGEFEMMES/' >> data/all.csv
sed 1d data/refined/declaration_avantages.refined.csv | sed 's/$/,ETALAB/' >> data/all.csv
sed 1d data/refined/declaration_conventions.refined.csv | sed 's/$/,ETALAB/' >> data/all.csv
sed -f data/unifier/global.sed -i data/all.csv
