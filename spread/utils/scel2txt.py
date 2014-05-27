#-*- coding: utf-8 -*-
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
        if flag is not self.TABLE_START_FLAG:
            return None

        pos = 0

        byte = data[4:]
        length = len(byte)

        while position < length:
            idx_pos = byte[pos : pos + 2]
            index = self.unpack(idx_pos)
            pos += 2
            size_pos = byte[pos : pos + 2]
            size = unpack(size_pos)
            pos += 2
            spelling = byte2str(byte[pos : pos + size])
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

        def analyse(self):
            with open(self.file_path, 'rb') as scel:
                data = scel.read()

                if data[0 : 12] is not SCEL_FLAG:
                    print("Not *.scel file")
                    return None

                table = get_table(data[TABLE_START : CHINESE_START])
                results = get_chinese(data[CHINESE_START:], table)
        
            return results


class SCELSet(object):

    def __init__(self):
        self.scels = set()

    def from_files(scel_files):
        for _file in scel_files:
            scel = SCEL(_file)
            self.scels.add(scel)

    def write_file(self, out_to, fields=None):
        if fields is None:
            fields = ('number', 'spelling', 'word')

        for scel in self.scels:
            results = scel.analyse()
            if not results:
                continue

            with open(out_to, 'w') as out_stream:
                for item in results:
                    line = []
                    for field in fields:
                        line.append(field)
                        line.append(results[field])

                out_stream.write(line)
                out_stream.write('\n')
