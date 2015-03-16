#!/bin/bash

#DECL_TYPE:1,ORIGIN:2,LABO:3,BENEF_PS_QUALITE_NOM_PRENOM:4,BENEF_PS_CODEPOSTAL:5,BENEF_PS_ADR:6,BENEF_PS_QUALIFICATION:7,BENEF_PS_RPPS:8,DECL_CONV_DATE:9,DECL_CONV_OBJET:10,DECL_CONV_PROGRAMME:11,DECL_AVANT_MONTANT:12,DECL_AVANT_DATE:13,DECL_AVANT_NATURE:14,BENEF_ETUD_ETA:15,SOURCE:16,BENEF_PS_ID:17,BENEF_PS_DEPARTEMENT:18
awk -F ',' '{print $1","$2","$3","$7","$17","$18","$13","$14","$12","$9","$10","$16}' data/all.unames.csv > tmp/all.anonymes.csv
head -n 1 tmp/all.anonymes.csv > data/all.anonymes.csv
sed 1d tmp/all.anonymes.csv | sort -u >> data/all.anonymes.csv
rm -f data/public/sunshine.anonymes.csv
ln data/all.anonymes.csv data/public/sunshine.anonymes.csv
