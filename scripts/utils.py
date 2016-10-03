# -*- coding: utf-8 -*-

from builtins import str as text


def find_zipcode(s):
    s = re.sub('.* ([0-9]{4,5})[ \.].*', '\g<1>', text(s))
    return s if len(s) == 5 else ''


def euro2float(montant):
    if type(montant) != str:
        return ""

    try:
        montant = re.sub(r"[^0-9\.,]", "", re.sub(r",", ".", montant))
        fmontant = float(montant)
    except AttributeError:
        fmontant = float(montant)
    except ValueError:
        fmontant = 0.0
    return fmontant

months = {'jan':'01', 'r s':'01', 'fev': '02', 'mar': '03', 'avr':'04', 'mai':'05', 'uin':'06', 'uil':'07', 'aou':'08', 'aoû':'08', 'sep':'09','oct':'10','nov':'11','dec':'12','déc':'12'}


def humanmonth(match):
    return '20%s-%s-%02d' % match.group(4)[-2:], months[re.sub('^jui', 'ui', match.group(3).lower())[:3]], int(match.group(2))


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
        pass


import re, string
from unidecode import unidecode

PUNCTUATION = re.compile('[%s]' % re.escape(string.punctuation))


class Fingerprinter(object):
    '''
    Python implementation of Google Refine fingerprinting algorithm described here:
    https://github.com/OpenRefine/OpenRefine/wiki/Clustering-In-Depth

    Requires the unidecode module: https://github.com/iki/unidecode
    '''
    def __init__(self, string):
        self.string = self._preprocess(string)

    def _preprocess(self, string):
        '''
        Strip leading and trailing whitespace, lowercase the string, remove all punctuation,
        in that order.
        '''
        return PUNCTUATION.sub('', string.strip().lower())

    def _latinize(self, string):
        '''
        Replaces unicode characters with closest Latin equivalent. For example,
        Alejandro González Iñárritu becomes Alejando Gonzalez Inarritu.
        '''
        return unidecode(string)

    def _unique_preserving_order(self, seq):
        '''
        Returns unique tokens in a list, preserving order. Fastest version found in this
        exercise: http://www.peterbe.com/plog/uniqifiers-benchmark
        '''
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]

    def get_fingerprint(self):
        '''
        Gets conventional fingerpint.
        '''
        return self._latinize(' '.join(
            self._unique_preserving_order(
                sorted(self.string.split())
            )
        ))

    def get_ngram_fingerprint(self, n=1):
        '''
        Gets ngram fingerpint based on n-length shingles of the string.
        Default is 1.
        '''
        return self._latinize(''.join(
            self._unique_preserving_order(
                sorted([self.string[i:i + n] for i in range(len(self.string) - n + 1)])
            )
        ))


if __name__ == '__main__':
    f = Fingerprinter('Tom Cruise')
    print(f.get_fingerprint())
    print(f.get_ngram_fingerprint(n=1))

    f = Fingerprinter('Cruise, Tom')
    print(f.get_fingerprint())
    print(f.get_ngram_fingerprint(n=1))

    f = Fingerprinter('Paris')
    print(f.get_fingerprint())
    print(f.get_ngram_fingerprint(n=2))