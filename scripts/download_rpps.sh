#!/bin/bash

url=$(curl -s -c /tmp/$$.jar --tlsv1.1 -k -L  https://annuaire.sante.fr/web/site-pro/extractions-publiques | sed 's|zip"><img src="/rass-pro-theme/images/bt_telecharger_espace_perso.png.*|zip|' | sed 's/.*href="//' | grep zip)
curl -s -b /tmp/$$.jar --tlsv1.1 -k -L $url > /tmp/sunshine.zip
unzip  /tmp/sunshine.zip -d /tmp/
mv /tmp/ExtractionMonoTable_CAT18_ToutePopulation_201610040928.csv data/rpps.csv
rm /tmp/sunshine.zip /tmp/$$.jar
