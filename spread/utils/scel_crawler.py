#-*- coding: utf-8 -*-
import re
import Queue
import threading
import urllib

import requests


class SingePage(object):

    URL_PATTERN = 'http://pinyin.sogou.com/dict/list.php?c=%s&page=%s'
    DT_PATTERN = '<dt><a href="cell\.php\?id=(?P<id>\d+)">(?P<name>[\s\S]+?)</a>[\s\S]*?</dt>\s+?<dd>[\s\S]+?<a href="(?P<url>http://download\.pinyin\.sogou\.com/.+?)" class="dlbtn3">\S+?</a>[\s\S]+?</dd>'
    HREF_PATTERN = re.compile(DT_PATTERN)

    def __init__(self, category):
        self.category = category

    def fetch(self, html):
        results = self.HREF_PATTERN.findall(html)
        return results

    def fetch_page(self, page):
        url = self.URL_PATTERN % (self.category, page)
        html = self.__fetch_html(url)
        if html is None:
            return None

        links = self.fetch(html)
        if len(links) <= 0:
            return False
        return links

    def fetch_pages(self, page=None):
        if page is None:
            page = 1
        download_links = []
        while(True):
            links = self.fetch_page(page)
            if not links:
                break
            download_links.extend(links)
            page += 1

        return download_links

    def __fetch_html(self, url):
        res = requests.get(url)
        if res.status_code is 200:
            return res.content
        else:
            return None


class RangePage(object):

    def __init__(self, save_to, lower=1, upper=500, limit=3):
        self.lower = lower
        self.upper = upper
        self.save_to = save_to
        self.limit = limit
        self.downloaders = list()
        self.queue = Queue.Queue()

    def fetch_all(self):
        for i in xrange(self.lower, self.upper):
            single_page = SingePage(category=i)

            results = single_page.fetch_pages()

            for res in results:
                _id, name, url = res
                name = name.decode('gb2312', 'ignore')
                self.queue.put((_id, name, url, self.save_to))

        for tid in xrange(self.limit):
            thread = Downloader(self.queue)
            self.downloaders.append(thread)
            thread.start()

        for dwer in self.downloaders:
            dwer.join()

        self.queue.join()


class Downloader(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            if self.queue.empty():
                break

            task = self.queue.get()
            _id, name, url, path = task
            target = '%s/%s.scel' % (path, name)
            urllib.urlretrieve(url, target)
            self.queue.task_done()
