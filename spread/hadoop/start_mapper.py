#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
import sys


states = ('B', 'M', 'E', 'S')


def regularize(char):
    if char == 12288:
        return 32
    if 65280 < char < 65375:
        return char - 65248
    if ord('A') <= char <= ord('Z'):
        char += 32
        return char
    return char


def unicodify(word):
    if not type(word) is unicode:
        try:
            word = word.decode('utf-8')
        except:
            word = word.decode('gbk', 'ignore')

    word = word.replace('\n', '')
    return word


def start_mapper():
    for line in sys.stdin:
        line = line.strip()
        words = line.split()
        for word in words:
            uword = unicodify(word)
            if len(uword) == 1:
                print "%s\t%s" % ('S', 1)
            elif len(uword) > 1:
                print "%s\t%s" % ('B', 1)


if __name__ == '__main__':
    start_mapper()
