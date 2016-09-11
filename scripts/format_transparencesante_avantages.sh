echo "ORIGIN,LABO,BENEF_PS_QUALITE_NOM_PRENOM,BENEF_PS_ADR,BENEF_PS_QUALIFICATION,BENEF_PS_RPPS,DECL_CONV_DATE,DECL_CONV_OBJET,DECL_CONV_PROGRAMME,DECL_AVANT_MONTANT,DECL_AVANT_DATE,DECL_AVANT_NATURE,BENEF_ETUD_ETA,BENEF_PS_CODEPOSTAL" > data/tmp/transparencesante_avantages.formatted.csv
#entreprise,type_beneficiaire,beneficiaire,date,nature,montant,code_postal_beneficaire
cat data/raw/transparencesante_avantages.csv | sed 's/\r//' | sed 1d | iconv -f utf8 -t utf8//IGNORE | perl -e 'while(<STDIN>){chomp; while(s/"([^"]*),([^"]*)"/"\1 -\2"/g){}; @a = split /,/; @s = split /\//, $a[3] ; $a[3] = $s[2]."-".$s[1]."-".$s[0]; print join ",", @a; print "\n"; }' | awk -F ',' '{print $2","$1","$3","$7","$2",,,,,"$6","$4","$5",,"$7}' | sed 's/  */ /g' | sed 's/, /,/g' | sed 's/ ,/,/g' >> data/tmp/transparencesante_avantages.formatted.csv
sed -i 's/Medecin/Médecin/g' data/tmp/transparencesante_avantages.formatted.csv
sed -i 's/,30002530750,/,,/' data/tmp/transparencesante_avantages.formatted.csv
sed -i 's/,12404201412,/,,/' data/tmp/transparencesante_avantages.formatted.csv
sed -i 's/,MéA,/,Médecin,/' data/tmp/transparencesante_avantages.formatted.csv

mv data/tmp/transparencesante_avantages.formatted.csv data/formatted/transparencesante_avantages.formatted.csv

