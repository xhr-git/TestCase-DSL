from TestStep.core.tc_to_TestStep import get_test_step
import sys


def __main(file: str, show_desc: bool = False):
    ret = 0
    t = get_test_step(file, show_desc)
    print()
    print('-' * 50)
    print()
    if show_desc:
        t.show_desc()
    else:
        ret = t.do_test()
        if ret == 0:
            res = 'pass'
        else:
            res = 'fail'
        print()
        print('test result = {} {}'.format(ret, res))
    print()
    print('-' * 50)
    print()
    exit(ret)


if __name__ == '__main__':
    __argc = len(sys.argv)
    __show_desc = False
    if __argc == 2:
        pass
    elif __argc == 3 and sys.argv[2] == 'show':
        __show_desc = True
    else:
        print()
        print('Usage:')
        print('  python3 auto.py <xxx.tc> [show]')
        print()
        exit(1)
    __main(sys.argv[1], __show_desc)

