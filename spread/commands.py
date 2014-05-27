#-*- coding: utf-8 -*-
from utils.scel_crawler import RangePage


class TestCommand(object):

    command = 'test'
    args_table = ()

    def set_args(self, args):
        self.args = args

    def do(self):
        print "Testing"
        print self.args


class CrawlerCommand(object):

    command = 'crawler'
    args_table = ('save_to', 'lower', 'upper', 'limit')

    def set_args(self, args):
        self.args = args

    def valid(self):
        if not len(self.args) == len(args_table):
            return False
        return True

    def do(self):
        valided = self.valid()
        if not valided:
            print('Error arguments for %s' % self.command)
            return None

        # parse args
        save_to, lower, upper, limit = self.args

        rp = RangePage(save_to=save_to, lower=lower,
                       upper=upper, limit=litmi)

        rp.fetch_all()
