from base_TestStep import TestStep
import importlib
import os
import sys

g_modules: list = None


def __find_all_modules():
    global g_modules
    print('=' * 50)
    g_modules = []
    path = os.path.abspath(__file__)
    path = os.path.dirname(os.path.dirname(path))
    sys.path.append(path)
    for f in os.listdir(path):
        m = os.path.isfile(os.path.join(path, f))
        if not m:
            continue
        if f[-3:] != '.py':
            continue
        if f == '__init__.py':
            continue
        c = f[:-3]
        try:
            m = importlib.import_module(c)
            m = m.__getattribute__(c)
            t = m
            while t.__base__ is not None:
                if t.__base__.__name__ is TestStep.__name__:
                    g_modules.append(m)
                    break
                t = t.__base__
            else:
                print('WARNING!! [{}] is not inherited from {}'.format(c, TestStep))
        except Exception as e:
            print('WARNING!! Can\'t import module: {}'.format(e))
    i = 0
    for m in g_modules:
        i = i + 1
        print('[{}] import :{}'.format(i, m))
    print('=' * 50)


def get_module(name: str):
    global g_modules
    if g_modules is None:
        __find_all_modules()
    for mod in g_modules:
        if mod.__name__ == name:
            return mod
    print('can\'t find module <{}>'.format(name))
    exit(1)


if __name__ == '__main__':
    pass
