from core.include import *
import time
import random
import sys


class ts_hello(TestStep):
    desc = 'Print "hello" repeatedly'

    def __init__(self, prefix, deep, paras):
        super().__init__(desc=self.desc, prefix=prefix, deep=deep, paras=paras)
        if self.duration is None:
            self.duration = 5

    def action(self):
        i = 0
        while not self.time_up():
            i = i + 1
            self.log('hello world : {}'.format(i))
            time.sleep(random.uniform(0.65, 2.35))
        self.log(f'"hello" was printed {i} times')
        return 0


if __name__ == '__main__':
    __paras = {}
    if len(sys.argv) == 2:
        __paras['duration'] = int(sys.argv[1])
    __ts = ts_hello('', 0, __paras)
    __ts.start_time = time.time()
    exit(__ts.action())

