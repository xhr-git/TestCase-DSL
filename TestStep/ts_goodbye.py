from core.include import *


class ts_goodbye(TestStep):
    desc = 'Print once "goodbye"'

    def __init__(self, prefix, deep, paras):
        super().__init__(desc=self.desc, prefix=prefix, deep=deep, paras=paras)

    def action(self):
        self.log(f'goodbye ! id={id(self)}')
        return 0


if __name__ == '__main__':
    pass

