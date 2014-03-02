#!/bin/bash

VIEWER="tail -n +2"

echo "ORIGINE;LABO;BENEF_QUALITE_NOM_PRENOM;BENEF_QUALIFICATION;BENEF_SPECIALITE;BENEF_ADR;BENEF_CP;BENEF_RPPS;DECL_CONV_DATE;DECL_CONV_OBJET;DECL_CONV_PROGRAMME;DECL_AVANT_MONTANT;DECL_AVANT_DATE;DECL_AVANT_NATURE"

##origin 1,convention_kind 2,name 3,benefit_value 4,title 5,establishment 6,benefit_kind 7,convention_date 8,benefit_date 9,rpps 10,expertise 11,company_name 12,qualification 13,address 14,quality 15
#cat data/sunshine.doctors.latest.csv  | $VIEWER | sed 's/\r//' | sed 's/[\*;]//g' | awk -F ',' 'BEGIN{OFS=";"} {print "MEDECINS1",$12,$3,$15,$11,$14,"",$10,$8,$2,"",$4,$9,$7}' | sed 's/; */;/g' | sed 's/ *;/;/g' | sed 's/  */ /g'

##kind 1,name 2,firstname 3,grade 4,company 5,company_id 6,value 7,rpps 8,job 9,company_name 10,address 11,date 12
#cat data/sunshine.pharmaciens.csv | $VIEWER | sed 's/\r//' | sed 's/[\*;]//g' | awk -F ',' 'BEGIN{OFS=";"} {print "PHARMACIENS",$10,$2" "$3,$4,$9,$11,"","","","","",$7,$12,$1}' | sed 's/; */;/g' | sed 's/ *;/;/g' | sed 's/  */ /g'

##QUALITE 1;NOM 2;PRENOM 3;CP 4;VILLE 5;DATE 6;MONTANT 7;AVANTAGE 8;ANNEE 9;LABO 10;OBJER CONVENTION 11
cat data/raw/dentistes.csv | $VIEWER | sed 's/\r//' | sed 's/[\*]//g' | awk -F ';' 'BEGIN{OFS=";"} {print "DENTISTES",$10,$1" "$2" "$3,"","",$4" "$5,$4,"","","","",$7,$6,$8}'  | sed 's/; */;/g' | sed 's/ *;/;/g' | sed 's/  */ /g'

##NOM 1;PRENOM 2;QUALITE 3;ADRESSE 4;TITRE 5;SPECIALITE 6;QUALIFICATION 7;NUMERO_ORDINAL 8;DATE_SIGNATURE_CONVENTION 9;OBJET 10;PROGRAMME 11;MONTANT_AVANTAGE 12;DATE_AVANTAGE 13;NATURE_AVANTAGE 14;LABO 15
cat data/raw/infirmiers.csv | $VIEWER | sed 's/\r//' | sed 's/[\*]//g' | awk -F ';' 'BEGIN{OFS=";"} {print "INFIRMIERS",$15,$3" "$1" "$2,$7,$6,$4,"",$8,$9,$10,$11,$12,$13,$14}' | sed 's/; */;/g' | sed 's/ *;/;/g' | sed 's/  */ /g'

#ORIGIN 1;LABO 2;BENEF_PS_QUALITE_NOM_PRENOM 3;BENEF_PS_ADR 4;BENEF_PS_QUALIFICATION 5;BENEF_PS_RPPS 6;DECL_AVANT_MONTANT 7;DECL_DATE 8;DECL_NATURE 9;DECL_CONV_DATE 10;DECL_CONV_NATURE 11;DECL_AVANT_DATE 12;DECL_AVANT_NATURE 13
cat data/raw/sagefemme.csv | $VIEWER | sed 's/\r//' | sed 's/[\*]//g' | awk -F ';' 'BEGIN{OFS=";"} {print "SAGEFEMMES",$2,$3,$5,"",$4,"",$6,$10,$11,"",$7,$12,$13}'

#LABO 1;PS_NOM 2;PS_PRENOM 3;PS_ 4;PS_ADR1 5;PS_ADR2 6;PS_ADR_NUM 7;PS_ADR_COMP 8;PS_VOIE 9;PS_ADR4 10;PS_CP 11;PS_VILLE 12;PS_PAYS 13;PS_QUALIF 14;PS_RPPS 15;CONV_DATE 16;CONV_OBJET 17;CONV_PROGRAMME 18;AVANT_MONTANT 19;AVANT_DATE 20;AVANT_NATURE 21
cat data/raw/internes_inexploitables.csv | $VIEWER | sed 's/\r//' | sed 's/[\*;]//g' | awk -F '\t' 'BEGIN{OFS=";"} {print "ETUDIANTSMEDECINS",$1,$2" "$3,$14,$4,$5" "$6" "$7" "$8" "$9" "$10" "$11" "$12" "$13,$11,$15,$16,$17,$18,$19,$20,$21}' | sed 's/; */;/g' | sed 's/ *;/;/g' | sed 's/  */ /g'

cat data/raw/medecins_inexploitables.csv | $VIEWER | sed 's/\r//' | sed 's/[\*;]//g' | awk -F '\t' 'BEGIN{OFS=";"} {print "MEDECINS",$1,$2" "$3,$14,$4,$5" "$6" "$7" "$8" "$9" "$10" "$11" "$12" "$13,$11,$15,$16,$17,$18,$19,$20,$21}' | sed 's/; */;/g' | sed 's/ *;/;/g' | sed 's/  */ /g'
