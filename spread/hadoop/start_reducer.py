#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
import sys


def start_reducer():
    start_count = {}
    for line in sys.stdin:
        line = line.strip()
        state, count = line.split('\t', 1)
        try:
            count = int(count)
            if not state in start_count:
                start_count[state] = 0
            start_count[state] += count
        except ValueError:
            pass

    for word, count in start_count.iteritems():
        print '%s\t%s' % (word, count)


if __name__ == '__main__':
    start_reducer()
