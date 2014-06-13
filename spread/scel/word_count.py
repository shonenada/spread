#-*- coding: utf-8
import re
import sys


def unicodify(word):
    if not type(word) is unicode:
        try:
            word = word.decode('utf-8')
        except:
            word = word.decode('gbk', 'ignore')
    return word


class WordCount(object):

    chinese = re.compile(ur'[\u4E00-\u9FA5]')

    def __init__(self):
        self.text = None
        self.dicts = dict()

    def read_file(self, file_path):
        with open(file_path, 'r') as _file:
            self.text = _file.read()
        self.text = unicodify(self.text)
        self.splits = self.chinese.findall(self.text)

    def count_each_chinese(self):
        for x in self.splits:
            if not x in self.dicts.keys():
                self.dicts[x] = 1
            else:
                self.dicts[x] += 1

    def count(self, word):
        word = unicodify(word)
        total_length = len(self.text)
        replaced = self.text.replace(word, '')
        sub_length = len(replaced)
        return (total_length - sub_length) / len(word)

    def report(self):
        for key, value in self.dicts.iteritems():
            print key, value


if __name__ == '__main__':
    wc = WordCount()
    wc.read_file(sys.argv[1])
    # wc.count_each_chinese()
    print wc.count('中文')
    wc.report()
