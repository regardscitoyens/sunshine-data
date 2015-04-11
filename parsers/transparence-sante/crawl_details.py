# -*- coding: utf-8 -*-
import os, sys

from crawler import TSCrawler
from parse import parse_listing
from utils import info

from settings import EXTRACT_DETAIL_DIR

import threading
import logging
import time
import Queue

from plan_crawl import get_all_tasks

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

HEADERS = ["rpps", "ville", "adresse", "nom", "prenom", "codepostal", "value", "nature", "intitule", "date", "id", "typologie"]


class ThreadWorker(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            dept_code, pages = self.queue.get()
            start = time.time()
            worker(dept_code, pages)
            self.queue.task_done()
            t = time.time() - start
            print "Task department=%s, page count=%s finished in: %.1f s, %.1f s/page" % (dept_code, len(pages), t, t / len(pages))


def worker(dept_code, pages):
    info("Crawl Dep=%s, page start=%s, page end=%s, page count=%s" % (dept_code, pages[0], pages[-1], len(pages)))

    dept_dir = "%s/%s" % (EXTRACT_DETAIL_DIR, dept_code)

    if not os.path.isdir(dept_dir):
        os.makedirs(dept_dir)

    ts_crawler = TSCrawler()

    info("Crawl department %s" % dept_code)

    form_response = ts_crawler.submit_form_by_dept(dept_code)

    for page in pages:
        info("Department=%s, page=%s" % (dept_code, page))

        listing_filename = "%s/%s/listing-%s-%s.html" % (EXTRACT_DETAIL_DIR, dept_code, dept_code, page)

        if os.path.isfile(listing_filename):
            continue

        if page != 0:
            form_response = ts_crawler.get_listing_page(page)

        form_html = form_response.read()
        data = list(parse_listing(form_html))

        # Crawl detail
        for idx, _ in enumerate(data):
            detail_filename = "%s/%s/avantage-%s-%s-%s.html" % (EXTRACT_DETAIL_DIR, dept_code, dept_code, page, idx)

            if os.path.isfile(detail_filename):
                continue

            with open(detail_filename, "w") as detail_file:
                detail_response = ts_crawler.get_detail(idx)

                if detail_response:
                    detail_file.write(detail_response.read())

        with open(listing_filename, 'w') as tmp_out:
            tmp_out.write(form_html)

    info("Departement=%s is finished" % dept_code)


def main():
    if len(sys.argv) > 1:
        thread_count = int(sys.argv[1])
    else:
        thread_count = 4

    queue = Queue.Queue()

    for task in get_all_tasks():
        queue.put(task)

    for i in range(thread_count):
        t = ThreadWorker(queue)
        t.setDaemon(True)
        t.start()

    queue.join()

main()