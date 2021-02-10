from core.include import *


class ts_fail(TestStep):
    def __init__(self, prefix, deep, paras):
        super().__init__(desc='Let the test fail', prefix=prefix, deep=deep, paras=paras)

    def action(self):
        return 88

