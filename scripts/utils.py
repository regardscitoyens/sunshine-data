# -*- coding: utf-8 -*-

import re


def find_zipcode(s):
    s = re.sub('.* ([0-9]{5})[ \.].*', '\g<1>', unicode(s))
    return s if len(s) == 5 else ''


def euro2float(montant):
    try:
        montant = re.sub(r"[^0-9\.,]", "", re.sub(r",", ".", montant.encode('utf-8')))
        fmontant = float(montant)
    except AttributeError:
        fmontant = float(montant)
    except ValueError:
        fmontant = 0.0
    return fmontant

months = {'jan':'01', 'r s':'01', 'fev': '02', 'mar': '03', 'avr':'04', 'mai':'05', 'uin':'06', 'uil':'07', 'aou':'08', 'aoû':'08', 'sep':'09','oct':'10','nov':'11','dec':'12','déc':'12'}


def humanmonth(match):
    return '20%s-%s-%02d' %  match.group(4)[-2:], months[re.sub('^jui', 'ui', match.group(3).lower())[:3]], int(match.group(2))


def str2date(date):
    try:
        date = re.sub(' ?/ ?', '/', date)
        if (re.search('(^|\D)\d{1,2}/\d{2}/\d{4}', date)):
            return re.sub('(^|.*\D)(\d{1,2})/(\d{2})/(\d{4})', '\g<4>-\g<3>-\g<2>', date)
        if (re.search('\d{2}\D\d{2}\D\d{4}', date)):
            return re.sub(r'(\d{2})\D(\d{2})\D(\d{4})', '\g<3>-\g<2>-\g<1>', date)
        if (re.search('\d{4}\D\d{2}\D\d{2}', date)):
            return re.sub(r'(\d{4})\D(\d{2})\D(\d{2})', '\g<1>-\g<2>-\g<3>', date)
        if (re.search('.*\d{2}\D\d{2}\D\d{2}(\D.*|$)', date)):
            return re.sub('.*(\d{2})\D(\d{2})\D(\d{2}).*', '20\g<3>-\g<2>-\g<1>', date)
        if (re.search('\d{1,2}\D\D+\D(20)?\d{2}', date)):
            return re.sub(r'(.*\D|^)(\d{1,2})\D(\D+)\D(\d{2}(\d{2}|$)).*', humanmonth, date)
    except TypeError:
        return ''
    return ''
