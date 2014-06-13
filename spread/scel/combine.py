#-*-coding: utf-8
import os
import sys


class Scel(object):

    def __init__(self):
        self.dicts = set()

    def add_file(self, file_path):
        with open(file_path, 'r') as _file:
            for line in _file.readlines():
                self.dicts.add(line)

    def add_path(self, path):
        for root, dirs, files in os.walk(path):
            for _file in files:
                self.add_file('%s/%s' % (root, _file))
                print 'write %s' % _file

    def write_file(self, _file):
        with open(_file, 'a') as f:
            for d in self.dicts:
                f.write(d)
                print 'write %s' % d


if __name__ == '__main__':
    scel = Scel()
    scel.add_path(sys.argv[1])
    scel.write_file(sys.argv[2])
