# -*- coding: utf-8 -*-
import mechanize, cookielib, re, parse, sys, postalcodes, random, os
import settings
from utils import *

EXTRACT_CONVENTIONS = settings.EXTRACT_CONVENTIONS
while True:
    if len(sys.argv) > 1:
        POSTALCODE = sys.argv[1]
    else:
        POSTALCODE = random.choice(list(postalcodes.postal_codes_left()))

    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    warn(POSTALCODE)
    info("HOMEPAGE")
    br.open('https://www.transparence.sante.gouv.fr')

    warn(POSTALCODE)
    info("BIG FORM")
    r = br.follow_link(text="Recherche avancée")
    br.select_form(nr=0)
    br.form['form:codePostalBeneficiaire'] = POSTALCODE
    r = br.submit()

    warn(POSTALCODE)
    info("CAPTCHA")
    print br.geturl()
    html = r.read()
    match = re.search('Quelle est la (.*?)è[r|m]e lettre du mot « (.*?) » ?', html, re.S)
    n, word = match.group(1), match.group(2)
    print "asked:",n, word
    word = word.decode('utf-8')
    answer = word[int(n)-1]
    print "answer:",answer
    br.select_form(nr=0)
    br.form['j_idt187:captcha'] = answer.encode('utf-8')
    r = br.submit()

    if EXTRACT_CONVENTIONS:     
        warn(POSTALCODE)
        info("SWITCH TO CONVENTIONS")
        br.select_form(nr=0)
        r = br.submit(name='j_idt17:j_idt23')

    warn(POSTALCODE)
    info("RESULTS")
    page = 0
    tmp_out = settings.EXTRACT_DIR+"/tmp/%s.csv" % POSTALCODE
    out = open(tmp_out,'w')
    while True:
        info(POSTALCODE +" page %s" % page)
        html = r.read()
        data = list(parse.results(html))
        for line in data:
            out.write(','.join([l.encode('utf-8') for l in line])+"\n")
        br.select_form(nr=0)
        try:
            if br.form.find_control('j_idt17:j_idt93').disabled:
                break
            r = br.submit(name='j_idt17:j_idt93')
        except mechanize._form.ControlNotFoundError: #only one page of data
            break
        page += 1

    out.close()
    os.rename(tmp_out, settings.EXTRACT_DIR+"/%s.csv" % POSTALCODE)
    print POSTALCODE, "is finished"
    
    if len(sys.argv) > 1:
        break
