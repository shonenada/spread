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
