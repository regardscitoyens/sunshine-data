# coding: utf-8
import scrapy
import re
import sys
from ts_spider import TSSpider
from scrapy.http import Request
from scrapy import log

class AvantageItem(scrapy.Item):
    type = scrapy.Field() 
    range = scrapy.Field() 
    labo = scrapy.Field()
    type_beneficiaire = scrapy.Field()
    beneficiaire = scrapy.Field()
    date = scrapy.Field()
    objet = scrapy.Field()
    montant = scrapy.Field()


class TSAvantagesSpider(TSSpider):
    name = "ts_avantages"

    def entrepriseAvantagesTable(self, response):
        tableexecvar = response.url.split("execution=")[-1]
        if response.css('table'):
            for sel in response.css('table').css('tr'):
                data = []
                for td in sel.css('td').extract():
                    a = re.sub('<[^<]+?>', '', re.sub('.*\n[ \t]*', '', td))
                    if (a):
                        data.append(a)
                if (len(data)):
                    i = AvantageItem()
                    i['type'] = 'avantage'
                    i['range'] = self.semestre
                    i['labo'] = data[0]
                    i['type_beneficiaire'] = data[1]
                    i['beneficiaire'] = data[2]
                    i['date'] = data[3]
                    i['objet'] = data[4]
                    i['montant'] = data[5]
                    yield i
            log.msg('page : '+response.css('li.btn-page input[disabled=disabled]::attr(value)').extract()[0], level=log.DEBUG)
            if (len(response.css('input.btn-next::attr(disabled)').extract()) == 0 and len(response.css('.btn-page input').extract()) > 1):
                nexturl = 'https://www.transparence.sante.gouv.fr/flow/rechercheEntreprises?execution='+tableexecvar+'&j_idt17=j_idt17&j_idt17%3Aj_idt88=Suivant&javax.faces.ViewState='+tableexecvar
                yield Request(url=nexturl, callback=self.entrepriseAvantagesTable, dont_filter=True)
            else:
                log.msg('End of Detail', level=log.DEBUG)
                return
        else:
            log.msg('No Detail', level=log.DEBUG)
            
