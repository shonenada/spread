#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
import sys


def trans_reducer():
    trans_count = {}
    for line in sys.stdin:
        line = line.strip()
        current, next, count = line.split('\t', 2)
        try:
            if current not in trans_count:
                trans_count[current] = {}
            if next not in trans_count[current]:
                trans_count[current][next] = 0
            trans_count[current][next] += 1
        except ValueError:
            pass

    for current, trans in trans_count.iteritems():
        for next, count in trans.iteritems():
            print '%s\t%s\t%s' % (current, next, count)


if __name__ == '__main__':
    trans_reducer()
