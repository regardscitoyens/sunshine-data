# coding: utf-8
import scrapy
from scrapy.http import Request
from scrapy import log
import json
import sys

class TSList(scrapy.Spider):
    name = "ts_list"
    allowed_domains = ["transparence.sante.gouv.fr"]
    start_urls = [
        "https://www.transparence.sante.gouv.fr/flow/rechercheEntreprises"
        ]

    def parse(self, response):
        return self.foreachLetters('https://www.transparence.sante.gouv.fr/ajax/nomsEntreprises?nomEntreprise=')

    def foreachLetters(self, url):
        log.msg("Debut: "+url, level=log.DEBUG)
        for ascii in xrange(ord('a'), ord('z')+1):
            yield Request(
                url=url+chr(ascii), callback=self.entreprises, dont_filter=True
                )

    def entreprises(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        nb = 0
        for nom in jsonresponse['nomsEntreprises']:
            if (nom['categorieRecherche'] == 'COMMENCE_PAR'):
                nb = nb + 1
                sys.stdout.write('LABO;'+nom['libelle']+';'+str(nb)+"\n")
        if (nb > 19):
            log.msg('MORE !!', level=log.DEBUG)
            return self.foreachLetters(response.url)
        log.msg('Fin: '+str(nb)+" "+response.url, level=log.DEBUG)
        return 
