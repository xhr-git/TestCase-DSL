from core.include import *
import time
import sys


class ts_ping(TestStep):
    desc = 'ping a PC'

    def __init__(self, prefix, deep, paras):
        super().__init__(desc=self.desc, prefix=prefix, deep=deep, paras=paras)
        if self.duration is None:
            self.duration = 5

    def action(self):
        i = 0
        while not self.time_up():
            i = i + 1
            self.log('ping seq = {}'.format(i))
            time.sleep(1)
        self.log(f'Pinged a total of {i} times')
        return 0


if __name__ == '__main__':
    __paras = {}
    if len(sys.argv) == 2:
        __paras['duration'] = int(sys.argv[1])
    __ts = ts_ping('', 0, __paras)
    __ts.start_time = time.time()
    exit(__ts.action())

