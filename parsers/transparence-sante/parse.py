# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup


def parse_listing(html):
    soup = BeautifulSoup(html)
    rows = soup.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if cols:
            yield [ele.text.strip().split('\n')[0] for ele in cols]


def parse_listing_count_and_count_per_page(html):
    soup = BeautifulSoup(html)
    try:
        legend = soup.find('legend')
        if legend:
            count = int(legend.text.split(' ')[0].replace(',', ''))
            count_per_page = 0
            rows = soup.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if cols:
                    count_per_page += 1
            return count, count_per_page
        else:
            return 0, 0
    except Exception, e:
        print "Error", e
        raise


def parse_details(html):
    soup = BeautifulSoup(html)

    rpps = soup.find('input', {"id": "j_idt17:numeroIdentifiant"})
    ville = soup.find('input', {"id": "j_idt17:villeBeneficiaire"})
    adresse = soup.find('input', {"id": "j_idt17:adresseProfessionnelle"})
    nom = soup.find('input', {"id": "j_idt17:nom"})
    prenom = soup.find('input', {"id": "j_idt17:prenom"})
    codepostal = soup.find('input', {"id": "j_idt17:codePostalBeneficiaire"})
    value = soup.find('input', {"id": "j_idt17:montantDeclaration"})
    nature = soup.find('input', {"id": "j_idt17:natureDeclaration"})
    intitule = soup.find('input', {"id": "j_idt17:intituleReferenceDeclaration"})
    date = soup.find('input', {"id": "j_idt17:dateDeclaration"})
    id = soup.find('input', {"id": "j_idt17:identifiantDeclaration"})
    typologie = soup.find('input', {"id": "j_idt17:typologieDeclaration"})

    return {
        "rpps": rpps["value"] if rpps else '',
        "ville": ville["value"] if ville else '',
        "adresse": adresse["value"] if adresse else '',
        "nom": nom["value"] if nom else '',
        "prenom": prenom["value"] if prenom else '',
        "codepostal": codepostal["value"] if codepostal else '',
        "value": value["value"] if value else '',
        "nature": nature["value"] if nature else '',
        "intitule": intitule["value"] if intitule else '',
        "date": date["value"] if date else '',
        "id": id["value"] if id else '',
        "typologie": typologie["value"] if typologie else '',
        }
