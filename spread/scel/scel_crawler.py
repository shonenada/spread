#-*- coding: utf-8 -*-
import re
import sys
import Queue
import urllib
import threading

import requests


def fetch_html(url):
    res = requests.get(url)
    if res.status_code == 200:
        return res.content
    else:
        return None


class SinglePage(object):

    url_pattern = "http://pinyin.sogou.com/dict/list.php?c=%s&page=%s"
    href_pattern = re.compile(r'<dt><a href="cell\.php\?id=(?P<id>\d+)">(?P<name>[\s\S]+?)</a>[\s\S]*?</dt>\s+?<dd>[\s\S]+?<a href="(?P<url>http://download\.pinyin\.sogou\.com/.+?)" class="dlbtn3">\S+?</a>[\s\S]+?</dd>')

    def __init__(self, category):
        print "SinglePage: %s" % category
        self.category = category

    def fetch(self, html):
        results = self.href_pattern.findall(html)
        return results

    def fetch_page(self, page):
        url = self.url_pattern % (self.category, page)
        html = fetch_html(url)
        if html is None:
            return None

        links = self.fetch(html)
        if len(links) <= 0:
            return False
        return links

    def fetch_pages(self):
        page = 1
        download_links = []
        while(True):
            print "Page %s" % page
            links = self.fetch_page(page)
            if not links:
                break
            download_links.extend(links)
            page += 1

        return download_links


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
            print 'from %s to %s' % (url, target)
            urllib.urlretrieve(url, target)
            self.queue.task_done()


class RangePage(object):

    def __init__(self, save_to, lower=1, upper=500, limit=3):
        self.lower = lower
        self.upper = upper
        self.save_to = save_to
        self.limit = limit
        self.dwers = list()
        self.queue = Queue.Queue()

    def fetch_all(self):
        for i in xrange(self.lower, self.upper):
            single_page = SinglePage(i)
            results = single_page.fetch_pages()

            for res in results:
                _id, name, url = res
                name = name.decode('gb2312', 'ignore').encode('utf-8')
                self.queue.put((_id, name, url, self.save_to))

        for i in xrange(self.limit):
            th = Downloader(self.queue)
            self.dwers.append(th)
            th.start()

        for dwer in self.dwers:
            dwer.join()
        self.queue.join()


def test():
    zhirankexue = SinglePage(1)
    results = zhirankexue.fetch_page(1)
    print len(results)
    for r in results:
        id, name, url = r
        print name.decode('gb2312').encode('utf-8')


def main(argv):
    save_to = argv[1]
    lower = int(argv[2])
    upper = int(argv[3])
    limit = int(argv[4])

    rp = RangePage(save_to=save_to, lower=lower, upper=upper, limit=limit)
    rp.fetch_all()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test()
        sys.exit(0)

    main(sys.argv)
