#!/bin/bash

cat names.all | while read NOM ; do
curl -s -f -X POST -d "secfield=&nom="$(echo $NOM | sed 's/ /+/g')"&prenom=" http://www.ordre-infirmiers.fr/transparence-des-avantages-des-infirmiers.html | sed 's/<td/\n<td/g' | sed 's|</td>|</td>\n|g' | grep data_cell | sed 's/^[^>]*>//' | tr '\n' ' ' | sed 's| *</td> *|;|g' | tr '\r' '\n' | sed 's/^;//' | sed 's| *<br/> *| |g'
done