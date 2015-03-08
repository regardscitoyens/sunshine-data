#!/bin/bash

cat data/refined/dentistes.refined.csv > data/all.csv
sed 1d data/refined/infirmiers.refined.csv >> data/all.csv
sed 1d data/refined/medecins_exploitables.refined.csv >> data/all.csv
sed 1d data/refined/medecins_inexploitables.refined.csv >> data/all.csv
sed 1d data/refined/pharmaciens.refined.csv >> data/all.csv
sed 1d data/refined/sagefemmes.refined.csv >> data/all.csv
sed 1d data/refined/transparencesante_avantages.refined.csv >> data/all.csv
sed 1d data/refined/transparencesante_conventions.refined.csv >> data/all.csv
