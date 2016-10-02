# -*- coding: utf-8 -*-

import csv
import sys

from sunshine import (
    AVANTAGES_HEADERS,
    build_qualification,
    build_address,
    build_rpps,
    clean_text,
    build_eta,
    build_name
)


def build_nature(row):
    nature = " ".join((row["avant_nature"], row["avant_convention_lie"]))
    return clean_text(nature)



def process_csv(filepath):
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')

        print(",".join(AVANTAGES_HEADERS))

        for row in reader:
            cleaned_row = dict((k, clean_text(v)) for k, v in row.items())
            print(",".join(("ETALAB", cleaned_row["denomination_sociale"], build_name(cleaned_row),
                            build_address(cleaned_row), build_qualification(cleaned_row),
                            build_rpps(cleaned_row), cleaned_row["avant_montant_ttc"],
                            cleaned_row["avant_date_signature"], build_nature(cleaned_row),
                            build_eta(cleaned_row), cleaned_row["benef_codepostal"])))


if __name__ == "__main__":
    """
    Format of csv input file :

    1=entreprise_identifiant;2=denomination_sociale;3=ligne_identifiant;4=ligne_rectification;
    5=benef_categorie_code;6=categorie;7=benef_nom;8=benef_prenom;9=benef_qualite_code;10=qualite;
    11=benef_adresse1;12=benef_adresse2;13=benef_adresse3;14=benef_adresse4;15=benef_codepostal;
    16=benef_ville;17=benef_pays_code;18=pays;19=benef_titre_code;20=benef_titre_libelle;
    21=benef_specialite_code;22=benef_speicalite_libelle;23=benef_qualification;
    24=benef_identifiant_type_code;25=identifiant_type;26=benef_identifiant_valeur;
    27=benef_etablissement;28benef_etablissement_codepostal;29=benef_etablissement_ville;
    30=benef_denomination_sociale;31=benef_objet_social;32=ligne_type;33=avant_date_signature;
    34=avant_montant_ttc;35=avant_nature;36=avant_convention_lie;37=avant_conv_semestre
    """

    process_csv(sys.argv[1])
