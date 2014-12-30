# coding: utf-8
import scrapy
import re
import sys
from scrapy.http import Request
from scrapy import log

class TSSpider(scrapy.Spider):
    handle_httpstatus_list = [404]

    def __init__(self, entreprise='SANOFI AVENTIS FRANCE', semestre='2012S1', *args, **kwargs):
        super(TSSpider, self).__init__(*args, **kwargs)
        self.entreprise = entreprise
        self.semestre = semestre

    allowed_domains = ["transparence.sante.gouv.fr"]
    start_urls = [
        "https://www.transparence.sante.gouv.fr/flow/rechercheEntreprises"
        ]

    def parse(self, response):
        if (re.search('erreur|redirection', response.url)):
            log.msg('url contains erreur: '+response.url, level=log.ERROR)
            exit(1)
        execvar = response.url.split("execution=")[-1]
        yield Request(
            url='https://www.transparence.sante.gouv.fr/flow/rechercheEntreprises?execution='+execvar+'&form=form&form:denominationSociale-autocomplete='+self.entreprise+'&form:j_idt57=Rechercher&javax.faces.ViewState='+execvar+'&form:dateDebut='+self.semestre+'&form:dateFin='+self.semestre,
            callback=self.capchta, dont_filter=True
            )
        return;

    def capchta(self, response):
        if (re.search('erreur|redirection', response.url)):
            log.msg('url contains erreur: '+response.url, level=log.ERROR)
            exit(1)
        execvar = response.url.split("execution=")[-1]
        splitted = response.css('label::text').extract()[0].split(' ');
        index = int(splitted[3][0])
        mot = splitted[8]
        log.msg('captcha breaker: '+str(index)+' '+mot+' => '+mot[index-1], level=log.DEBUG)
        yield Request(
            url='https://www.transparence.sante.gouv.fr/flow/rechercheEntreprises?execution='+execvar+'&j_idt62=j_idt62&j_idt62%3Acaptcha='+mot[index-1]+'&j_idt62%3Aj_idt70=Valider&javax.faces.ViewState='+execvar,
            callback=self.entrepriseSelector, dont_filter=True
            )
    def entrepriseSelector(self, response):
        if (re.search('erreur|redirection', response.url)):
            log.msg('url contains erreur: '+response.url, level=log.ERROR)
            exit(1)
        execvar = response.url.split("execution=")[-1]
        yield Request(
            url='https://www.transparence.sante.gouv.fr/flow/rechercheEntreprises?execution='+execvar+'&j_idt74=j_idt74&j_idt74%3AdataTable%3A0%3Aj_idt82=on&j_idt74%3Aj_idt107=Valider&javax.faces.ViewState='+execvar,
            callback=self.entrepriseAvantagesTable, dont_filter=True
            )
