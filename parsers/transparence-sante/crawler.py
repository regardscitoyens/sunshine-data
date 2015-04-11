# -*- coding: utf-8 -*-

import cookielib
import re
import time
import random
import mechanize

from utils import info


class TSCrawler(object):
    """Transparence sante crawler"""
    def __init__(self, proxy_host=None):
        self.browser = mechanize.Browser()
        if proxy_host is not None:
            self.browser.set_proxies({"http": proxy_host})
        self.cookie = cookielib.LWPCookieJar()
        self.browser.set_cookiejar(self.cookie)
        self.browser.set_handle_equiv(True)
        self.browser.set_handle_redirect(True)
        self.browser.set_handle_referer(True)
        self.browser.set_handle_robots(False)
        self.browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        self.browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    def submit_form_by_dept(self, department_code):
        self.browser.open('https://www.transparence.sante.gouv.fr')
        self.browser.follow_link(text="Recherche avancée")
        self.browser.select_form(nr=0)
        self.browser.form['form:departementBeneficiaire'] = [department_code]

        html = self.browser.submit().read()

        # Captcha
        match = re.search('Quelle est la (.*?)è[r|m]e lettre du mot « (.*?) » ?', html, re.S)
        n, word = match.group(1), match.group(2)

        word = word.decode('utf-8')
        answer = word[int(n)-1]

        self.browser.select_form(nr=0)
        self.browser.form['j_idt187:captcha'] = answer.encode('utf-8')
        return self.browser.submit()

    def get_detail(self, id):
        self.browser.select_form(nr=0)
        if self.browser.form.find_control('j_idt17:dataTable:%s:j_idt80' % id):
            response = self.browser.submit(name='j_idt17:dataTable:%s:j_idt80' % id)
            # go back to previous page
            self.browser.select_form(nr=0)
            self.browser.submit(name='j_idt17:j_idt24')
            time.sleep(random.random() * 2)
            return response

    def get_listing_page(self, i):
        try:
            self.browser.select_form(nr=0)
            self.browser.form.set_all_readonly(False)
            self.browser.form['j_idt17:j_idt90:%s:j_idt91' % 5] = str(  i)
            self.browser.form['j_idt17'] = 'j_idt17'
            self.browser.form['javax.faces.ViewState'] = 'e2s2'
            return self.browser.submit()

        except mechanize._form.ControlNotFoundError:
            info("mechanize error, should be last page")
            pass
