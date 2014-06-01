#-*-coding: utf-8 -*-
import re
import json

from spread.core.viterbi import viterbi
from spread.utils.character import Character


class Spread(object):

    states = ('B', 'M', 'E', 'S',)

    def __init__(self, *args, **kwargs):
        self.sentence = kwargs.pop('sentence', None)
        self.start_prob = kwargs.pop('start_prob', None)
        self.trans_prob = kwargs.pop('trans_prob', None)
        self.emit_prob = kwargs.pop('emit_prob', None)

    def split_sentence(self, sentence):
        sentence = Character.unicodify(sentence)

        chinese = re.compile(ur'([\u4E00-\u9FA5]+)')
        english = re.compile(ur'[^a-zA-Z0-9+#\n]')

        blocks = chinese.split(sentence)

        for block in blocks:
            if chinese.match(block):
                for word in self.cut(block):
                    yield word
            else:
                char = english.split(block)
                for c in char:
                    if c != '':
                        yield c

    def cut(self, sentence):
        prob, path = viterbi(
            sentence, self.states,
            self.start_prob, self.trans_prob, self.emit_prob)
        begin, next = 0, 0
        for i, char in enumerate(sentence):
            pos = path[i]
            if pos == 'B':
                begin = i
            elif pos == 'E':
                yield sentence[begin : i+1]
                next = i + 1
            elif pos == 'S':
                yield char
                next = i + 1

        if next < len(sentence):
            yield sentence[next:]

    def load_prob(self, path):
        if path.endswith('py'):
            with open(path, 'rb') as model:
                data = eval(model.read())
        elif path.endswith('json'):
            with open(path, 'rb') as model:
                data = json.load(model)
        elif path.endswith('txt'):
            with open(path, 'rb') as model:
                data = set()
                for line in iter(model.readline, ''):
                    data.add(line.strip().decode('utf-8'))
        else:
            return None

        return data

    def load_start_prob(self, path):
        self.start_prob = self.load_prob(path)

    def load_trans_prob(self, path):
        self.trans_prob = self.load_prob(path)

    def load_emit_prob(self, path):
        self.emit_prob = self.load_prob(path)
