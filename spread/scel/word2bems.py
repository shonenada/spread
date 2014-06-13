#-*- coding: utf-8
import re
import sys


def unicodify(word):
    if not type(word) is unicode:
        try:
            word = word.decode('utf-8')
        except:
            word = word.decode('gbk', 'ignore')
    return word



def word2bems(word):
    chinese = re.compile(ur'[\u4E00-\u9FA5]')
    word = unicodify(word)
    result = chinese.findall(word)
    if len(result) == 1:
        return [(word, 'S')]
    output = list()
    output.append((result[0], 'B'))
    output.append((result[len(result) - 1], 'E'))
    for x in result[1:-1]:
        output.append((x, 'M'))

    return output


if __name__ == '__main__':
    count = {'B': 0, 'E': 0, 'M': 0, 'S': 0}
    tran_count = {
        'B': {'M': 0, 'E': 0,},
        'E': {'B': 0, 'S': 0,},
        'M': {'E': 0, 'M': 0,},
        'S': {'B': 0, 'S': 0,}
    }
    last = None
    with open(sys.argv[1]) as f:
        line = f.readline()
        while line:
            output = word2bems(line)
            for x in output:
                count[x[1]] += 1
                if last:
                    tran_count[last][x[1]] += 1
                last = x[1]
            line = f.readline()
    print count
    print tran_count


# for x in  word2bems('中华人民共和国'):
    # print x[0], x[1]

# for x in word2bems('和'):
    # print x[0], x[1]
