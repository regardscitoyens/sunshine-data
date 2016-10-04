# -*- coding: utf-8 -*-

import re

AVANTAGES_HEADERS = ("ORIGIN", "LABO", "BENEF_PS_QUALITE_NOM_PRENOM", "BENEF_PS_ADR", "BENEF_PS_QUALIFICATION",
                     "BENEF_PS_RPPS", "DECL_AVANT_MONTANT", "DECL_AVANT_DATE", "DECL_AVANT_NATURE", "BENEF_ETUD_ETA",
                     "BENEF_PS_CODEPOSTAL")

CONVENTION_HEADERS = ("ORIGIN", "LABO", "BENEF_PS_QUALITE_NOM_PRENOM", "BENEF_PS_ADR", "BENEF_PS_QUALIFICATION",
                      "BENEF_PS_RPPS", "DECL_CONV_DATE", "DECL_CONV_OBJET", "DECL_CONV_PROGRAMME", "BENEF_ETUD_ETA",
                      "BENEF_PS_CODEPOSTAL")


def clean_text(value):
    if type(value) != str:
        return ""

    return re.sub("\s+", " ", re.sub("\"", " ", re.sub("(\n|\r|,)", " ", value)).strip())


def build_name(row):
    name = " ".join((row["benef_prenom"], row["benef_nom"], row["benef_denomination_sociale"]))
    return clean_text(name)


def build_address(row):
    address = " ".join((
        row["benef_etablissement"], row["benef_etablissement_codepostal"], row["benef_etablissement_ville"],
        row["benef_adresse1"], row["benef_adresse2"], row["benef_adresse3"], row["benef_adresse4"],
        row["benef_codepostal"], row["benef_ville"], row["pays"]))

    return clean_text(address)


def build_qualification(row):
    qualif = " ".join((row["categorie"], row["qualite"], row["benef_speicalite_libelle"],
                       row["benef_objet_social"]))

    return clean_text(qualif)


def build_rpps(row):
    return "" if row["identifiant_type"] == "AUTRE" else row["benef_identifiant_valeur"]


def build_eta(row):
    eta = " ".join((row["benef_etablissement"], row["benef_etablissement_codepostal"],
                    row["benef_etablissement_ville"]))
    return clean_text(eta)


ORIGIN_MAPPING = {
    "Médecin": "Medecin",
    "Chirurgien-dentiste": "Dentiste"
}


def build_origin(row):
    if row["benef_categorie_code"] == "[ETU]":
        return "Etudiant"

    elif row["benef_categorie_code"] == "[PRS]":
        return ORIGIN_MAPPING.get(row["qualite"], row["qualite"])

    else:
        return row["categorie"]
