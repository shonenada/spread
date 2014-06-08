#-*- coding: utf-8 -*-
import os
import struct


class SCEL(object):
    '''A model class of scel files.
    This class implementation some of methods to parse scel file.
    Its goal is transforming the scel file to txt file.

    :param file_path: the path of scel file.
    '''

    TABLE_START = 0x1540
    CHINESE_START = 0x2628
    TABLE_START_FLAG = '\x9D\x01\x00\x00'
    SCEL_FLAG = '\x40\x15\x00\x00\x44\x43\x53\x01\x01\x00\x00\x00'
    BYTE_INVALID_CHAR = ('\t', ' ')

    def __init__(self, file_path):
        self.file_path = file_path
        self.results = []

    def unpack(self, code):
        fmt_chr = struct.unpack('H', code)
        return fmt_chr[0]

    def byte2str(self, byte):
        '''transform byte to string'''
        output = []
        length = len(byte)
        for position in xrange(0, length, 2):
            unicode_code = byte[position : position + 2]
            fmt_chr = self.unpack(unicode_code)
            char = unichr(fmt_chr)
            if char not in self.BYTE_INVALID_CHAR:
                output.append(char)
            elif char == '\t':
                output.append('\n')
        return ''.join(output)

    def get_table(self, data):
        '''Get spelling table from data'''
        spelling_table = dict()

        flag = data[0:4]
        if flag != self.TABLE_START_FLAG:
            return None

        pos = 0

        byte = data[4:]
        length = len(byte)

        while pos < length:
            idx_pos = byte[pos : pos + 2]
            index = self.unpack(idx_pos)
            pos += 2
            size_pos = byte[pos : pos + 2]
            size = self.unpack(size_pos)
            pos += 2
            spelling = self.byte2str(byte[pos : pos + size])
            spelling_table[index] = spelling
            pos += size

        return spelling_table

    def get_word_spelling(self, data, table):
        output = []
        for pos in xrange(0, len(data), 2):
            unicode_code = data[pos : pos + 2]
            index = self.unpack(unicode_code)
            output.append(table[index])
    
        return ''.join(output)

    def get_chinese(self, data, table):
        pos = 0
        results = []
        length = len(data)

        while pos < length:
            same = self.unpack(data[pos : pos + 2])
            pos += 2
            table_len = self.unpack(data[pos : pos + 2])
            pos += 2

            spelling = self.get_word_spelling(data[pos : pos+table_len], table)

            pos += table_len

            for i in xrange(same):
                chinese_len = self.unpack(data[pos : pos + 2])
                pos += 2

                word = self.byte2str(data[pos : pos + chinese_len])
                pos += chinese_len

                ext_len = self.unpack(data[pos : pos + 2])
                pos += 2

                number = self.unpack(data[pos : pos + 2])
                pos += ext_len

                results.append(
                    {'number': number,
                     'spelling': spelling,
                     'word': word})
        return results

    def analyse(self):
        with open(self.file_path, 'rb') as scel:
            data = scel.read()

        if data[0 : 12] != self.SCEL_FLAG:
            print("Not *.scel file")
            return None

        table = self.get_table(data[self.TABLE_START : self.CHINESE_START])
        results = self.get_chinese(data[self.CHINESE_START:], table)
        self.results = results
        return results

    def write_file(self, out_path, filename=None, fields=None):
        if filename is None:
            filename = '%s.%s' % (self.file_path.rsplit('/', 1).pop(), 'txt')

        if fields is None:
            fields = ('number', 'spelling', 'word')

        line = []

        for item in self.results:
            for field in fields:
                line.append(unicode(item[field]).encode('utf-8'))
        output = '\n'.join(line)

        out_path = os.path.join(out_path, filename)
        with open(out_path, 'w') as out:
            out.write(output)


class SCELSet(object):

    def __init__(self):
        self.scels = set()

    def from_files(self, scel_files):
        for _file in scel_files:
            if not _file.endswith('scel'):
                continue

            scel = SCEL(_file)
            self.scels.add(scel)

    def from_path(self, path):
        for root, dirs, files in os.walk(path):
            self.from_files(['%s/%s' % (path, f) for f in files])

    def write_file(self, out_to, fields=None):
        for scel in self.scels:
            scel.analyse()
            scel.write_file(out_to, fields=fields)
