#-*- coding: utf-8 -*-
import os
import sys
import struct


TABLE_START = 0x1540
CHINESE_START = 0x2628
TABLE_START_FLAG = '\x9D\x01\x00\x00'
SCEL_FLAG = '\x40\x15\x00\x00\x44\x43\x53\x01\x01\x00\x00\x00'


def unpack(code):
    fmt_chr = struct.unpack('H', code)
    return fmt_chr[0]


def byte2str(byte):
    """将原始字节码转换成字符串"""
    output = []
    length = len(byte)
    for pos in xrange(0, len(byte), 2):
        unicode_code = byte[pos : pos + 2]
        # transform uni to unsigned short.
        fmt_chr = unpack(unicode_code)
        # transform fmt_chr to unicode by its Unicode code.
        char = unichr(fmt_chr)
        if char not in ('\t', ' '):
            output.append(char)
        elif char == '\t':
            output.append('\n')
    return ''.join(output)


def get_table(data):
    pinyin_table = {}

    flag = data[0:4]
    if flag != TABLE_START_FLAG:
        return None

    pos = 0
    byte = data[4:]
    length = len(byte)
    while pos < length:
        idx_pos = byte[pos : pos + 2]
        index = unpack(idx_pos)
        pos += 2
        size_pos = byte[pos : pos + 2]
        size = unpack(size_pos)
        pos += 2
        pinyin = byte2str(byte[pos : pos + size])
        pinyin_table[index] = pinyin
        pos += size

    return pinyin_table


def get_word_pinyin(data, table):
    output = []
    for pos in xrange(0, len(data), 2):
        uni = data[pos : pos + 2]
        index = unpack(uni)
        output.append(table[index])
    return ''.join(output)


def get_chinese(data, table):
    pos = 0
    results = []
    length = len(data)
    while pos < length:
        same = unpack(data[pos : pos + 2])
        pos += 2
        pinyin_table_len = unpack(data[pos : pos + 2])        
        pos += 2

        pinyin = get_word_pinyin(data[pos : pos + pinyin_table_len], table)
        pos += pinyin_table_len

        for i in xrange(same):
            chinese_len = unpack(data[pos : pos + 2])
            pos += 2

            word = byte2str(data[pos : pos + chinese_len])
            pos += chinese_len

            ext_len = unpack(data[pos : pos + 2])
            pos += 2

            count = unpack(data[pos : pos + 2])
            results.append((count, pinyin, word))
            pos += ext_len

    return results


def analyse(filename):
    with open(filename, 'rb') as scel:
        data = scel.read()

        if data[0:12] != SCEL_FLAG:
            print("%s not *.scel" % filename)
            return None

        table = get_table(data[TABLE_START : CHINESE_START])
        results = get_chinese(data[CHINESE_START:], table)
    return results


def main(path, output):
    for root, dirs, files in os.walk(path):
        for _file in files:
            if _file.endswith('scel'):
                fp = '%s/%s' % (path, _file)
                results = analyse(fp)
                if not results:
                    continue
                try:
                    with open('%s/%s%s' % (output, _file, '.txt'), 'w') as out_stream:
                        print 'open %s' % _file
                        for _, _, word in results:
                            out_stream.write(unicode(word).encode('utf-8'))
                            out_stream.write('\n')
                except Exception:
                    continue


'''
def main(scel_files):
    for f in scel_files:
        results = analyse(f)
        with open('%s%s' % (f, '.txt'), 'w') as out_stream:
            for item in results:
                line = "%s %s %s" % item
                out_stream.write(unicode(line).encode('utf-8'))
                out_stream.write('\n')
'''


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        sys.exit(0)
    main(args[1], args[2])
