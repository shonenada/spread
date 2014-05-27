#-*- coding: utf-8 -*-
import re


class Character(object):

    RE_SKIP_PATTERN = re.compile(r'(\d+\.\d+|[a-zA-Z0-9]+)')
    CONNECTIORS = ('+', '#', '&', '.', '_', '-')

    def is_chinese_char(self, char):
        if 0x4E00 <= char <= 0x9FA5:
            return True
        return False

    def is_english_char(self, char):
        if (0x0041 <= char <= 0x005A) or (0x0061 <= char <= 0x007A):
            return True
        return False

    def is_digit(self, char):
        if 0x0030 <= char <= 0x0039:
            return True
        return False

    def is_connector(self, char):
        return char in (self.connectors)

    def find(self, char):
        if ((self.is_chinese_char(char)) or
            (self.is_english_char(char)) or
            (self.is_digit(char))):
            return True
        return False

    @staticmethod
    def regularize(char):
        if char == 12288:
            return 32
        if 65280 < char < 65375:
            return char - 65248
        if ord('A') <= char <= ord('Z'):
            return char += 32
        return char

    @staticmethod
    def unicodify(word):
        if not type(word) is unicode:
            try:
                word = word.decode('utf-8')
            except:
                word = word.decode('gbk', 'ignore')

        word = word.replace('\n', '')
        return word
