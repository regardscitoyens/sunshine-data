echo "ORIGIN,LABO,BENEF_PS_QUALITE_NOM_PRENOM,BENEF_PS_ADR,BENEF_PS_QUALIFICATION,BENEF_PS_RPPS,DECL_CONV_DATE,DECL_CONV_OBJET,DECL_CONV_PROGRAMME,DECL_AVANT_MONTANT,DECL_AVANT_DATE,DECL_AVANT_NATURE,BENEF_ETUD_ETA,BENEF_PS_CODEPOSTAL," > data/formatted/transparencesante_avantages.formatted.csv
#entreprise,type_beneficiaire,beneficiaire,date,nature,montant,code_postal_beneficaire
cat data/raw/transparencesante_avantages.csv | sed 's/\r//' | sed 1d | awk -F ',' '{print $2","$1","$3","$7","$2",,,,,"$6","$4","$5","$7}' | sed 's/  */ /g' | sed 's/, /,/g' | sed 's/ ,/,/g' >> data/formatted/transparencesante_avantages.formatted.csv


