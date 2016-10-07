#!/bin/bash

echo "ORIGIN,LABO,BENEF_PS_QUALITE_NOM_PRENOM,BENEF_PS_ADR,BENEF_PS_QUALIFICATION,BENEF_PS_RPPS,DECL_AVANT_MONTANT,DECL_AVANT_DATE,DECL_AVANT_NATURE,BENEF_ETUD_ETA,BENEF_PS_CODEPOSTAL" > data/formatted/declaration_avantages.formatted.csv
#1=entreprise_identifiant;2=denomination_sociale;3=ligne_identifiant;4=ligne_rectification;5=benef_categorie_code;6=categorie;7=benef_nom;8=benef_prenom;9=benef_qualite_code;10=qualite;11=benef_adresse1;12=benef_adresse2;13=benef_adresse3;14=benef_adresse4;15=benef_codepostal;16=benef_ville;17=benef_pays_code;18=pays;19=benef_titre_code;20=benef_titre_libelle;21=benef_specialite_code;22=benef_speicalite_libelle;23=benef_qualification;24=benef_identifiant_type_code;25=identifiant_type;26=benef_identifiant_valeur;27=benef_etablissement;28=benef_etablissement_codepostal;29=benef_etablissement_ville;30=benef_denomination_sociale;31=benef_objet_social;32=ligne_type;33=conv_date_signature;34=conv_objet;35=conv_date_debut;36=conv_date_fin;37=conv_manifestation_date;38=conv_manifestation_nom;39=conv_manifestation_lieu;40=conv_manifestation_organisateur
#1=entreprise_identifiant;2=denomination_sociale;3=ligne_identifiant;4=ligne_rectification;5=benef_categorie_code;6=categorie;7=benef_nom;8=benef_prenom;9=benef_qualite_code;10=qualite;11=benef_adresse1;12=benef_adresse2;13=benef_adresse3;14=benef_adresse4;15=benef_codepostal;16=benef_ville;17=benef_pays_code;18=pays;19=benef_titre_code;20=benef_titre_libelle;21=benef_specialite_code;22=benef_speicalite_libelle;23=benef_qualification;24=benef_identifiant_type_code;25=identifiant_type;26=benef_identifiant_valeur;27=benef_etablissement;28benef_etablissement_codepostal;29=benef_etablissement_ville;30=benef_denomination_sociale;31=benef_objet_social;32=ligne_type;33=avant_date_signature;34=avant_montant_ttc;35=avant_nature;36=avant_convention_lie;37=avant_conv_semestre

tail -n +2 data/raw/declaration_avantages.test.csv | sed 's/"//g' | sed 's/,/ /g' | awk -F ';' '{
LABO=$2
NOM=$8" "$7" "$28" "$30;
ADRESSE=$27" "$28" "$29" "$11" "$12" "$13" "$14" "$15" "$16" "$18;
QUALIF=$6" "$10" "$22" "$31
RPPS=$26
MONTANT=$34
DATE=$33
NATURE=$38" "$35" "$36
ETA=$27" "$28" "$29
CODEPOSTAL=$15
if ( $25 == "AUTRE") RPPS=""
print "EXPORT-ETALAB,"LABO","NOM",\""ADRESSE"\","QUALIF","RPPS","MONTANT","DATE",\""NATURE"\",\""ETA"\","CODEPOSTAL
}' | sed 's/, */,/g' | sed 's/," */,"/g' | sed 's/ *",/",/g'  | sed 's/ *,/,/g'  | sed 's/  */ /g' >> data/formatted/declaration_avantages.formatted.csv
