echo "ORIGIN,LABO,BENEF_PS_QUALITE_NOM_PRENOM,BENEF_PS_ADR,BENEF_PS_QUALIFICATION,BENEF_PS_RPPS,DECL_CONV_DATE,DECL_CONV_OBJET,DECL_CONV_PROGRAMME,DECL_AVANT_MONTANT,DECL_AVANT_DATE,DECL_AVANT_NATURE,BENEF_ETUD_ETA,BENEF_PS_CODEPOSTAL" > data/formatted/transparencesante_conventions.formatted.csv
#entreprise:1,type_beneficiaire:2,beneficiaire:3,date:4,periode:5,objet:6,code_postal_beneficaire:7
cat data/raw/transparencesante_conventions.csv | awk -F ',' '{print $2","$1","$3","$7","$2",,"$4","$6","$5",,,,"$7}' | sed 's/  */ /g' | sed 's/, /,/g' | sed 's/ ,/,/g' >> data/formatted/transparencesante_conventions.formatted.csv


