# -*- coding: utf-8 -*-

from __future__ import division

import re
import glob
import os
from settings import EXTRACT_DIR
from crawler import TSCrawler
from parse import parse_listing_count_and_count_per_page


def get_departments():
    with open("external_sources/departements.csv") as file:
        codes = []
        lines = file.readlines()
        for line in lines[1:]:
            region , dep, cheflieu, tncc, ncc, nccenr = line.strip().split(',')
            codes.append(dep)
        return codes


def get_dept_remaining_tasks(dept_code):
    first_listing_page_filename = "%s/%s/listing-%s-0.html" % (EXTRACT_DIR, dept_code, dept_code)

    if not os.path.isfile(first_listing_page_filename):
        crawler = TSCrawler()
        response = crawler.submit_form_by_dept(dept_code)
        dept_dir = "%s/%s/" % (EXTRACT_DIR, dept_code)
        if not os.path.isdir(dept_dir):
            os.makedirs(dept_dir)
        with open(first_listing_page_filename, 'w') as output:
            output.write(response.read())

    first_listing_page = open(first_listing_page_filename, 'r')

    count, count_per_page = parse_listing_count_and_count_per_page(first_listing_page)

    if count_per_page == 0:
        pages_to_crawl = []
    else:
        pages_to_crawl = range(0, int(count / count_per_page) + 1)

    print "Dep=%s , total pages to crawl=%s" % (dept_code, len(pages_to_crawl))

    already_crawled_listings = glob.glob("%s/%s/listing-%s-*.html" % (EXTRACT_DIR, dept_code, dept_code))

    if pages_to_crawl:
        for name in already_crawled_listings:
            page = int(re.search("listing-\d{1,3}[A,B]?-(\d{1,5}).html", name).groups()[0])
            try:
                pages_to_crawl.remove(page)
            except ValueError:
                print name

    print "Dep=%s , remaining pages to crawl=%s" % (dept_code, len(pages_to_crawl))

    return pages_to_crawl


def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


def get_all_tasks():
    all_tasks = []
    for dept_code in get_departments():
        dept_pages = get_dept_remaining_tasks(dept_code)

        if dept_pages:
            for chunk in chunks(dept_pages, 50):
                all_tasks.append((dept_code, chunk))

    return all_tasks