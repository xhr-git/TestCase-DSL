from core.include import *


class ts_test_sync(TestStepSync):
    _list = [
        ts_item('ts_hello', {'duration': 4}),
        ts_item('ts_hello', {'duration': 4}),
        ts_item('ts_hello', {'duration': 4}),
    ]

    def __init__(self, prefix, deep, paras):
        super().__init__(desc=None, prefix=prefix, deep=deep, paras=paras, _list=self._list)


if __name__ == '__main__':
    pass

