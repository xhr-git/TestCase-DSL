from core.include import *
import random
import time


class ts_sleep(TestStep):
    def __init__(self, prefix, deep, paras):
        self.__time = paras.get('time', 1)
        min_t = self.__min_t = paras.get('min')
        max_t = self.__max_t = paras.get('max')

        def range_valid(x):
            if x is float or x is int:
                return True
            else:
                return False

        if range_valid(min_t) and range_valid(max_t) and min_t <= max_t:
            self.__time = None
        if self.__time is None:
            desc = 'sleep [{}, {}] seconds'.format(min_t, max_t)
        else:
            desc = f'sleep {self.__time} seconds'
        super().__init__(desc=desc, prefix=prefix, deep=deep, paras=paras)

    def action(self):
        if self.__time is None:
            time.sleep(random.uniform(self.__min_t, self.__max_t))
        else:
            time.sleep(self.__time)
        return 0


if __name__ == '__main__':
    pass

