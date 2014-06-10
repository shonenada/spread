#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
import sys


def emit_reducer():
    emit_count = {}
    for line in sys.stdin:
        line = line.strip()
        state, word, count = line.split('\t', 2)
        try:
            if state not in emit_count:
                emit_count[state] = {}
            if word not in emit_count[state]:
                emit_count[state][word] = 0
            emit_count[state][word] += int(count)
        except ValueError:
            pass

    for state, emit in emit_count.iteritems():
        for word, count in emit.iteritems():
            print '%s\t%s\t%s' % (state, word, count)


if __name__ == '__main__':
    emit_reducer()
