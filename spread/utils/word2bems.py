#-*- coding: utf-8 -*-
import re
import os
import json

from .character import Character


class BEMS(object):

    CHINESE_PATTERN = re.compile(ur'[\u4E00-\u9FA5]')

    def __init__(self, words):
        words = Character.regularize(words)
        self.words = Character.unicodify(words)

    def transform(self):
        chinese_words = self.CHINESE_PATTERN.findall(self.words)
        if not chinese_words:
            return list()

        if len(chinese_words) == 1:
            return [{'word': chinese_words[0], 'state': 'S'}]

        output = list()
        output.append({'word': chinese_words[0], 'state': 'B'})

        for word in chinese_words[1:-1]:
            output.append({'word': word, 'state': 'M'})

        output.append({'word': chinese_words[len(chinese_words) - 1],
                       'state': 'E'})

        return output


class BEMSHelper(object):

    def __init__(self, filename):
        self.reset(filename)

    def reset(self, filename):
        self.filename = filename
        self.emit_list = dict()
        self.start_count = {'B': 0.0, 'S': 0.0}
        self.bems_count = {'B': 0.0, 'M': 0.0, 'E': 0.0, 'S': 0.0}
        self.transform_count = {
            'B': {'M': 0.0, 'E': 0.0,},
            'E': {'B': 0.0, 'S': 0.0,},
            'M': {'E': 0.0, 'M': 0.0,},
            'S': {'B': 0.0, 'S': 0.0,}
        }
        self.start_probability = {'B': 0.0, 'S': 0.0}
        self.bems_probability = {'B': 0.0, 'M': 0.0, 'E': 0.0, 'S': 0.0}
        self.transform_probability = {
            'B': {'M': 0.0, 'E': 0.0,},
            'E': {'B': 0.0, 'S': 0.0,},
            'M': {'E': 0.0, 'M': 0.0,},
            'S': {'B': 0.0, 'S': 0.0,}
        }
        self.emit_probability = {'B': {}, 'M': {}, 'E': {}, 'S': {}}

    def update_emit(self, bems):
        word, state = bems['word'], bems['state']
        if word not in self.emit_list.keys():
            self.word_item = {'B': 0.0, 'M': 0.0, 'E': 0.0, 'S': 0.0}
            self.emit_list.setdefault(word, self.word_item)
        self.emit_list[word][state] += 1

    def calculate_emit_probability(self):
        counts = {'B': 0.0, 'M': 0.0, 'E': 0.0, 'S': 0.0}
        for wordsbems in self.emit_list.values():
            for state, count in wordsbems.iteritems():
                counts[state] += count

        for word, wordsbems in self.emit_list.iteritems():
            for state in wordsbems:
                if counts[state] == 0:
                    self.emit_probability[state][word] = 0
                    continue
                prob = float(wordsbems[state] / counts[state])
                self.emit_probability[state][word] = prob

    def analyse_file(self):
        with open(self.filename, 'r') as _file:
            last = None
            for line in iter(_file.readline, ''):
                bems = BEMS(line)
                output = bems.transform()
                
                # start count.
                if len(output) == 1 and output[0]['state'] == 'S':
                    self.start_count['S'] += 1
                elif len(output) > 1 and output[0]['state'] == 'B':
                    self.start_count['B'] += 1

                for each in output:
                    # emit count.
                    self.update_emit(each)
                    
                    # total count.
                    self.bems_count[each['state']] += 1

                    # transform count
                    if last:
                        self.transform_count[last][each['state']] += 1
                    last = each['state']

    def analyse_probability(self):

        # start probability
        start_total = sum(self.start_count.values())
        for key in self.start_probability:
            self.start_probability[key] = self.start_count[key] / start_total

        # total probability
        bems_total = sum(self.bems_count.values())
        for key in self.bems_probability:
            self.bems_probability[key] = self.bems_count[key] / bems_total

        # transform probability
        for k, v in self.transform_count.iteritems():
            transform_total = sum(v.values())
            for key, value in v.iteritems():
                self.transform_probability[k][key] = value / transform_total

        # emit probability
        self.calculate_emit_probability()

    def write_file(self, folder_path):
        if not os.path.exists(folder_path):
            os.mkdir (folder_path)

        with open('%s/start_prob.txt' % folder_path, 'w') as out:
            out.write(json.dumps(self.start_probability, indent=2))

        with open('%s/transform_prob.txt' % folder_path, 'w') as out:
            out.write(json.dumps(self.transform_probability, indent=2))

        with open('%s/emit_prob.txt' % folder_path, 'w') as out:
            out.write(json.dumps(self.emit_probability, indent=2))
