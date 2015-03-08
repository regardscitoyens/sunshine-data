#!/bin/bash
cd data/formatted

echo "ORIGIN,LABO,BENEF_PS_QUALITE_NOM_PRENOM,BENEF_PS_ADR,BENEF_PS_QUALIFICATION,BENEF_PS_RPPS,DECL_CONV_DATE,DECL_CONV_OBJET,DECL_CONV_PROGRAMME,DECL_AVANT_MONTANT,DECL_AVANT_DATE,DECL_AVANT_NATURE,BENEF_ETUD_ETA,BENEF_PS_CODEPOSTAL" > ../all.csv
#data/refined/dentistes.refined.csv
#ORIGIN:,BENEF_PS_QUALIFICATION:2,BENEF_PS_QUALITE_NOM_PRENOM:3,BENEF_PS_CODEPOSTAL:4,DECL_AVANT_MONTANT:5,BENEF_PS_ADR:6,DECL_AVANT_DATE:7,DECL_AVANT_NATURE:8,LABO:9
sed 1d dentistes*.csv | awk -F ',' '{print $1","$9","$3","$6","$2",,,,,"$5","$7","$8",,"$4}' >> ../all.csv
#data/refined/infirmiers.refined.csv
#ORIGIN:1,DECL_AVANT_MONTANT:2,BENEF_PS_RPPS:3,LABO:4,DECL_CONV_DATE:5,BENEF_PS_QUALIFICATION:6,BENEF_PS_SPECIALITE:7,DECL_CONV_PROGRAMME:8,DECL_CONV_OBJET:9,BENEF_PS_QUALITE_NOM_PRENOM:10,DECL_AVANT_DATE:11,BENEF_PS_ADR:12,BENEF_PS_CODEPOSTAL:13,DECL_AVANT_NATURE:14
sed 1d infirmiers*.csv | awk -F ',' '{print $1","$4","$10","$12","$6","$3","$5","$9","$8","$2","$11","$14",,"$13}' >> ../all.csv
#data/refined/pharmaciens.refined.csv
#ORIGIN:1,BENEF_PS_RPPS:2,BENEF_PS_QUALIFICATION:3,BENEF_PS_CODEPOSTAL:4,LABO:5,BENEF_PS_ADR:6,DECL_AVANT_DATE:7,BENEF_PS_QUALITE_NOM_PRENOM:8,DECL_AVANT_NATURE:9,DECL_AVANT_MONTANT:10
sed 1d pharmaciens*.csv | awk -F ',' '{print $1","$5","$8","$6","$3","$2",,,,"$10","$7","$9",,"$4}' >> ../all.csv
#data/refined/sagefemmes.refined.csv
#ORIGIN:1,LABO:2,BENEF_PS_QUALITE_NOM_PRENOM:3,BENEF_PS_ADR:4,BENEF_PS_QUALIFICATION:5,BENEF_PS_RPPS:6,DECL_AVANT_MONTANT:7,DECL_DATE:8,DECL_NATURE:9,DECL_CONV_DATE:10,DECL_CONV_NATURE:11,DECL_AVANT_DATE:12,DECL_AVANT_NATURE:13,BENEF_PS_CODEPOSTAL:14
sed 1d sagefemmes*.csv | awk -F ',' '{print $1","$2","$3","$4","$5","$6","$10","$11",,"$7","$12","$13",,"$14}' >> ../all.csv
#data/refined/medecins_exploitables.refined.csv
sed 1d medecins_exploitables*.csv >>  ../all.csv
#data/refined/medecins_inexploitables.refined.csv
sed 1d medecins_inexploitables*.csv >>  ../all.csv
#data/refined/transparencesante_avantages.refined.csv
sed 1d transparencesante_avantages*.csv >>  ../all.csv
#data/refined/transparencesante_conventions.refined.csv
sed 1d transparencesante_conventions*.csv >>  ../all.csv
