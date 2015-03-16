from bs4 import BeautifulSoup
from pprint import pprint as pp

def results(html):
    soup = BeautifulSoup(html)
    rows = soup.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if cols:
            yield [ele.text.strip().split('\n')[0] for ele in cols]

if __name__ == '__main__':
    for r in results(open('results.html')):
        print(r)