from core.include import *
import os
import platform

if platform.system() == 'Windows':
    os.system('chcp 65001')


class ts_shell(TestStep):
    def __init__(self, prefix, deep, paras):
        self.__cmd = paras.get('cmd')
        assert self.__cmd is not None and self.__cmd.__class__ is str
        desc = 'shell "{}"'.format(self.__cmd)
        super().__init__(desc=desc, prefix=prefix, deep=deep, paras=paras)

    def action(self):
        return os.system(self.__cmd)


if __name__ == '__main__':
    pass

