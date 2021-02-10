import re
import sys

pattern_double = [
    {
        'begin': r'/\*',    # /* */
        'end': r'\*/',
        'hold': False
    }, {
        'begin': r'\"',     # " "
        'end': r'(?<!\\)\"',
        'hold': True
    }
]

pattern_discard = [
    r'//.*(\n|\r)+',				# //
    r'\s+',					# blank
    r'\r',
    r'\n',
]

pattern_hold = [
    r'(=|\[|\]|\(|\)|\{|\}|,|\.)',
    r'\b\w+\b',
]


def check_double(line: str, arr: list):
    for p in pattern_double:
        begin = re.search(p['begin'], line)
        if begin is not None and begin.span()[0] == 0:
            end = re.search(p['end'], line[begin.span()[1]:])
            if end is not None:
                if p['hold'] is True:
                    temp = line[begin.span()[1]:begin.span()[1]+end.span()[0]]
                    temp = temp.replace('\n', '').replace('\r', '').replace('\\\"', '\"')
                    temp = '[str]' + temp
                    arr.append(temp)
                return 'continue', line[begin.span()[1]+end.span()[1]:]
            else:
                return 'break', line
    return 'next', line


def check_discard(line: str, arr: list):
    for p in pattern_discard:
        match = re.search(p, line)
        if match is not None and match.span()[0] == 0:
            return 'continue', line[match.span()[1]:]
    return 'next', line


def check_hold(line: str, arr: list):
    for p in pattern_hold:
        match = re.search(p, line)
        if match is not None and match.span()[0] == 0:
            # print('[{}] {} : {} '.format(p, match.span(), match.group()))
            arr.append(match.group())
            return 'continue', line[match.span()[1]:]
    return 'next', line


check_token = [
    check_double,
    check_discard,
    check_hold,
]


def check_all(line: str, arr: list):
    ret = 'next'
    for check in check_token:
        ret, line = check(line, arr)
        if ret == 'next':
            continue
        elif ret == 'break' or ret == 'continue':
            return ret, line
        else:
            print('check_all fatal error: {}'.format(line))
    if ret == 'next':
        print('unknown pattern: [ {} ]'.format(line.replace('\r', '').replace('\n', '')))
        exit(1)


def tc_tokenizer(lines: list, show: bool = False):
    tokens = []
    line = str()
    for string in lines:
        line = line + ' ' + string
        while len(line) > 0:
            ret, line = check_all(line, tokens)
            if ret == 'break':
                break
            else:
                continue
    if line != '':
        print('\nERROR !!!!!!')
        exit(2)
    if show:
        print('=' * 50)
        i = 0
        for t in tokens:
            print('[{}] <{}>'.format(i, t))
            i = i + 1
        print('=' * 50)
    return tokens


def tc_tokenizer_file(file: str, show: bool = False):
    lines = open(file, 'r').readlines()
    return tc_tokenizer(lines, show)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: {} <file_name>'.format(__file__))
        exit(1)
    tc_tokenizer_file(sys.argv[1], True)

