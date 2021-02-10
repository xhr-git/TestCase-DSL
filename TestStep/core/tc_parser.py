from tc_tokenizer import tc_tokenizer_file
import re
import sys

kwauto = 'auto'
kwimport = 'import'

tp_concurrent = '__Concurrent__'
tp_sequence = '__Sequence__'
tp_import = '__Import__'
tp_normal = NotImplemented


class TcObj:
    def __init__(self, tokens: list = None):
        self.type: str = None
        self.paras: dict = {}
        self.objs: list = []
        self.tokens: list = tokens
        first = self.__get()
        if first == kwauto:
            self.__parser_auto()
        elif first == kwimport:
            self.__parser_import()
        else:
            self.__parser_obj()
        if self.type is None:
            print('self.type is None !!!')
            exit(1)

    @staticmethod
    def __str_to_val(s: str, n):
        if s is not None and s.isdigit():
            digit = int(s)
        else:
            try:
                digit = float(s)
            except:
                digit = None
        if s is None:
            return True
        elif n == 1:
            if s == 'true' or s == 'True':
                return True
            elif s == 'false' or s == 'False':
                return False
            elif digit is not None:
                return digit
            else:
                return s
        elif digit is not None:
            return digit
        else:
            print('syntax error: [{}] is not a value!!!!'.format(s))
            exit(5)

    @staticmethod
    def __str_refine(s: str):
        prefix = '[str]'
        n = len(prefix)
        if len(s) >= n:
            if s[0:n] == prefix:
                return s[n:]
        return s

    @staticmethod
    def __is_word(s: str):
        t = re.search(r'\b[A-Za-z_]+\w*\b', s)
        if t is None:
            return False
        return t.span() == (0, len(s))

    def __parser_auto(self):
        self.__del()
        self.__parser_paras()
        self.__parser_list()

    def __parser_import(self):
        if self.__get() != kwimport:
            print('syntax error: It\'s not import !!!!')
            exit(7)
        self.__del()
        self.type = tp_import
        self.paras[tp_import] = self.__str_refine(self.__get())
        self.__del()

    def __parser_list(self):
        flag = self.__get()
        self.__del()
        if flag == '{':
            self.type = tp_sequence
            flag = '}'
        elif flag == '(':
            self.type = tp_concurrent
            flag = ')'
        else:
            print('syntax error: after \'auto\' need () or {}!!!!')
            exit(7)
        while len(self.tokens) > 0:
            if self.__get() == flag:
                flag = None
                self.__del()
                break
            self.objs.append(TcObj(self.tokens))
        if flag is not None:
            print('syntax error: Maybe the parentheses are not paired!!!!')
            exit(7)

    def __parser_obj(self):
        if len(self.tokens) <= 0:
            return
        name = self.__get()
        self.__del()
        tp = [tp_import, tp_sequence, tp_concurrent]
        for t in tp:
            if name == tp:
                print('syntax error: TestStep must not be \'{}\'!!!!'.format(t))
                exit(7)
        if not self.__is_word(name):
            print('syntax error: TestStep must be a whole word, but now is <{}>!!!!'.format(name))
            exit(8)
        self.type = name
        self.__parser_paras()

    def __parser_paras(self):
        if self.__get() != '[':
            return
        self.__del()
        if self.__get() == ']':
            self.__del()
            return
        key = None
        val = None
        n = 0
        while len(self.tokens) > 0:
            first = self.__get()
            self.__del()
            if key is None:
                if not self.__is_word(first):
                    print('syntax error: para [{}] is not a word!!!!'.format(first))
                    exit(7)
                else:
                    key = first
                    continue
            else:
                if first == '=':
                    val = str()
                    n = 0
                elif first == ',' or first == ']':
                    if key is None:
                        print('syntax error: [{}] is syntax error!!!!'.format(key))
                        exit(5)
                    self.paras[key] = self.__str_to_val(val, n)
                    val = None
                    key = None
                    if first == ']':
                        return
                    else:
                        continue
                else:
                    if val is None:
                        print('syntax error: [{}] The equal sign may be missing !!!!'.format(key))
                        exit(5)
                    else:
                        val = val + self.__str_refine(first)
                        n = n + 1

    def __get(self):
        if len(self.tokens) <= 0:
            print('syntax error: There is no more context !!')
            exit(6)
        return self.tokens[0]

    def __del(self):
        del self.tokens[0]

    def show(self, prefix=''):
        print('{}{}: {}'.format(prefix, self.type, self.paras))
        if self.type == tp_sequence or self.type == tp_concurrent:
            for o in self.objs:
                o: TcObj
                o.show(prefix + '    ')


def tc_parser(tokens: list):
    # tokens = list.copy(tokens)
    return TcObj(tokens)


def tc_parser_file(file: str, show: bool = False):
    tco = tc_parser(tc_tokenizer_file(file))
    if show:
        print('=' * 50)
        print()
        tco.show()
        print()
        print('=' * 50)
    return tco


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: {} <file_name>'.format(__file__))
        exit(1)
    tc_parser_file(sys.argv[1], True)
