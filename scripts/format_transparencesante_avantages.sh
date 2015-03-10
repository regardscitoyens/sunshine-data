echo "ORIGIN,LABO,BENEF_PS_QUALITE_NOM_PRENOM,BENEF_PS_ADR,BENEF_PS_QUALIFICATION,BENEF_PS_RPPS,DECL_CONV_DATE,DECL_CONV_OBJET,DECL_CONV_PROGRAMME,DECL_AVANT_MONTANT,DECL_AVANT_DATE,DECL_AVANT_NATURE,BENEF_ETUD_ETA,BENEF_PS_CODEPOSTAL" > data/tmp/transparencesante_avantages.formatted.csv
#entreprise,type_beneficiaire,beneficiaire,date,nature,montant,code_postal_beneficaire
cat data/raw/transparencesante_avantages.csv | sed 's/\r//' | sed 1d | iconv -f utf8 -t utf8//IGNORE | perl -e 'while(<STDIN>){chomp; while(s/"([^"]*),([^"]*)"/"\1 -\2"/g){}; @a = split /,/; @s = split /\//, $a[3] ; $a[3] = $s[2]."-".$s[1]."-".$s[0]; print join ",", @a; print "\n"; }' | awk -F ',' '{print $2","$1","$3","$7","$2",,,,,"$6","$4","$5",,"$7}' | sed 's/  */ /g' | sed 's/, /,/g' | sed 's/ ,/,/g' >> data/tmp/transparencesante_avantages.formatted.csv
sed -i 's/Medecin/Médecin/g' data/tmp/transparencesante_avantages.formatted.csv
sed -i 's/,30002530750,/,,/' data/tmp/transparencesante_avantages.formatted.csv
sed -i 's/,12404201412,/,,/' data/tmp/transparencesante_avantages.formatted.csv
sed -i 's/,MéA,/,Médecin,/' data/tmp/transparencesante_avantages.formatted.csv

if false; then
sed -i 1244931d data/tmp/transparencesante_avantages.formatted.csv
sed -i 1244930d data/tmp/transparencesante_avantages.formatted.csv
sed -i 1229175d data/tmp/transparencesante_avantages.formatted.csv
sed -i 1175885d data/tmp/transparencesante_avantages.formatted.csv
sed -i 1166379d data/tmp/transparencesante_avantages.formatted.csv
sed -i 1164878d data/tmp/transparencesante_avantages.formatted.csv
sed -i 1124104d data/tmp/transparencesante_avantages.formatted.csv
sed -i 1123388d data/tmp/transparencesante_avantages.formatted.csv
sed -i 1096793d data/tmp/transparencesante_avantages.formatted.csv
sed -i 1088304d data/tmp/transparencesante_avantages.formatted.csv
sed -i 1042911d data/tmp/transparencesante_avantages.formatted.csv
sed -i 1011486d data/tmp/transparencesante_avantages.formatted.csv
sed -i 1011485d data/tmp/transparencesante_avantages.formatted.csv
sed -i 931803d data/tmp/transparencesante_avantages.formatted.csv
sed -i 840758d data/tmp/transparencesante_avantages.formatted.csv
sed -i 792715d data/tmp/transparencesante_avantages.formatted.csv
sed -i 686503d data/tmp/transparencesante_avantages.formatted.csv
sed -i 686310d data/tmp/transparencesante_avantages.formatted.csv
sed -i 586418d data/tmp/transparencesante_avantages.formatted.csv
sed -i 582673d data/tmp/transparencesante_avantages.formatted.csv
sed -i 571969d data/tmp/transparencesante_avantages.formatted.csv
sed -i 517008d data/tmp/transparencesante_avantages.formatted.csv
sed -i 313855d data/tmp/transparencesante_avantages.formatted.csv
sed -i 313854d data/tmp/transparencesante_avantages.formatted.csv
sed -i 148597d data/tmp/transparencesante_avantages.formatted.csv
sed -i 141886d data/tmp/transparencesante_avantages.formatted.csv
sed -i 140971d data/tmp/transparencesante_avantages.formatted.csv
sed -i 140663d data/tmp/transparencesante_avantages.formatted.csv
sed -i 126197d data/tmp/transparencesante_avantages.formatted.csv
sed -i 107754d data/tmp/transparencesante_avantages.formatted.csv
sed -i 95347d data/tmp/transparencesante_avantages.formatted.csv
sed -i 23407d data/tmp/transparencesante_avantages.formatted.csv
fi
mv data/tmp/transparencesante_avantages.formatted.csv data/formatted/transparencesante_avantages.formatted.csv
rm data/tmp/transparencesante_avantages.formatted.csv
