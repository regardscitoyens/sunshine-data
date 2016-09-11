# -*- encoding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re

def retrieveData(unNom):
	params = {'nom': unNom, 'prenom': ''}
	cookies = dict(bir_cookie_stat_permanent='1', SN5154d980b0aa2='02936942e77e061f68be9d206a089caa')
	r = requests.post("http://www.ordre-infirmiers.fr/transparence-des-avantages-des-infirmiers.html", data=params, cookies=cookies)
	html_doc = r.text

	soup = BeautifulSoup(html_doc)

	container = soup.find("tbody" , "data_container")
	if not container:
		return

	rows = container.findAll(attrs={'class' : re.compile("data_even|data_odd")})
		#for (nom, prenom, qualite, adresse, titre, specialite, qualification, numero_ordinal, date_signature_convention, objet, programme, montant, date, nature, entreprise) in row.findAll(attrs={'class' : 'data_cell' }):
	for row in rows:
		#    cells = row.find_all(attrs={'class' : 'data_cell' })
		cells = row.find_all("td")
		nom = cells[0].get_text()
		prenom = cells[1].get_text()
		qualite = cells[2].get_text()
		adresse = cells[3].get_text()
		titre = cells[4].get_text()
		specialite = cells[5].get_text()
		qualification = cells[6].get_text()
		numero_ordinal = cells[7].get_text()
		date_signature_convention = cells[8].get_text()
		objet = cells[9].get_text()
		programme = cells[10].get_text()
		montant = cells[11].get_text()
		date = cells[12].get_text()
		nature = cells[13].get_text()
		entreprise = cells[14].get_text()
		sep = "\t"
		print nom,sep, prenom,sep, qualite,sep, adresse,sep, titre,sep, specialite,sep, qualification, sep,numero_ordinal, sep,date_signature_convention, sep,objet,sep, programme,sep, montant,sep, date,sep, nature,sep, entreprise,



f = open("listeNomInfirmier.csv")
for unNom in f:
		retrieveData(unNom.strip())



