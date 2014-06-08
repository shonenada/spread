#-*- coding: utf-8 -*-
import os
import re
import json

from spread.core.app import Spread
from spread.utils.scel_crawler import RangePage
from spread.utils.scel2txt import SCELSet
from spread.utils.word2bems import BEMSHelper


class Command(object):

    command = None
    args_table = None

    def set_args(self, args):
        self.args = args

    def valid(self):
        return (len(self.args) == len(self.args_table))

    def do(self):
        if not self.valid():
            print 'Error arguments for %s' % self.command
            print 'Args Tabls: ', self.args_table
            return None

        self._do()

    def _do(self):
        pass


class TestCommand(Command):

    command = 'test'
    args_table = ()

    def _do(self):
        print "Testing"
        print self.args


class CrawlerCommand(Command):

    command = 'crawler'
    args_table = ('save_to', 'lower', 'upper', 'limit')

    def _do(self):
        # parse args
        save_to, lower, upper, limit = self.args

        lower = int(lower)
        upper = int(upper)
        limit = int(limit)

        rp = RangePage(save_to=save_to, lower=lower,
                       upper=upper, limit=limit)

        rp.fetch_all()


class Scel2TxtCommand(Command):

    command = 'scel2txt'
    args_table = ('path', 'out_to')

    def _do(self):

        path, out_to = self.args

        scel_set = SCELSet()
        scel_set.from_path(path)

        scel_set.write_file(out_to, fields=('word',))


class BEMSCommand(Command):

    command = 'bems'
    args_table = ('txt_folder', 'out_path')

    def _do(self):
        
        txt_folder, out_path = self.args

        bems = BEMSHelper(txt_folder)

        bems.analyse()
        bems.write_prob_file(out_path)


class BEMSCountCommand(Command):

    command = 'count'
    args_table = ('txt_folder', 'out_path')

    def _do(self):

        txt_folder, out_path = self.args

        for root, dirs, files in os.walk(txt_folder):
            for _f in files:
                if not _f.endswith('txt'):
                    continue
                path = os.path.join(root, _f)
                filename = _f.rsplit('.')[0]
                bems = BEMSHelper()
                bems.analyse_file(path)
                bems.write_count_file(out_path, filename=filename)


class SpreadCommand(Command):

    command = 'spread'
    args_table = ('path', 'start', 'trans', 'emit')

    def _do(self):

        path, start, trans, emit = self.args

        spread = Spread()

        spread.load_start_prob(start)
        spread.load_trans_prob(trans)
        spread.load_emit_prob(emit)

        result = list()

        with open(path, 'r') as input_file:
            for line in input_file.readlines():
                result.append(spread.split_sentence(line))

        for seg in result:
            print '/ '.join([x.encode('utf-8') for x in seg])


class SpreadShortCutCommand(Command):

    command = 'sr'
    args_table = ('path', 'prob_folder')

    def _do(self):

        path, prob_folder = self.args

        proxy = SpreadCommand()
        proxy.set_args((
            path,
            os.path.join(prob_folder, 'start_prob.json'),
            os.path.join(prob_folder, 'trans_prob.json'),
            os.path.join(prob_folder, 'emit_prob.json')
        ))

        proxy.do()


class SpreadServerCommand(Command):

    command = 'spread-server'
    args_table = ('infile', 'prob_path', 'output')

    def _do(self):
        infile, prob_path, output = self.args

        spread = Spread()

        start_path = os.path.join(prob_path, 'start_prob.json')
        trans_path = os.path.join(prob_path, 'trans_prob.json')
        emit_path = os.path.join(prob_path, 'emit_prob.json')

        spread.load_start_prob(start_path)
        spread.load_trans_prob(trans_path)
        spread.load_emit_prob(emit_path)

        result = list()

        with open(infile, 'r') as input_file:
            for line in input_file.readlines():
                for each in spread.split_sentence(line):
                    result.append(each)

        if not os.path.exists(output):
            os.mkdir(output)

        with open(os.path.join(output, 'dict.json'), 'w') as out_file:
            out_file.write(json.dumps(result, indent=2))
