from base_TestStepList import *
from tc_parser import *
import multiprocessing
import os


def __init_ts(ts: TestStep, *args):
    ts._mp_ns = args[0]


def __tco_to_ts(tco: TcObj, path: str, prefix: str = 'TestStep', deep: int = 0, *args):
    if tco.type == tp_import:
        p = os.path.join(path, tco.paras[tp_import])
        p = os.path.abspath(p)
        ts = __tco_to_ts(tc_parser_file(p), os.path.dirname(p), prefix, deep, *args)
        __init_ts(ts, *args)
        return ts
    elif tco.type == tp_sequence:
        ts_seq = TestStepSeq(prefix=prefix, deep=deep, paras=tco.paras)
        __init_ts(ts_seq, *args)
        i = 0
        for obj in tco.objs:
            i = i + 1
            ts_seq.stepList.append(__tco_to_ts(obj, path, TestStep.next_prefix(prefix, i), deep+1, *args))
        return ts_seq
    elif tco.type == tp_concurrent:
        ts_sync = TestStepSync(prefix=prefix, deep=deep, paras=tco.paras)
        __init_ts(ts_sync, *args)
        duration = tco.paras.get('duration')
        i = 0
        for obj in tco.objs:
            obj: TcObj
            i = i + 1
            if duration is not None:
                temp = obj.paras.get('duration')
                if temp is None:
                    obj.paras['duration'] = duration
            ts_sync.stepList.append(__tco_to_ts(obj, path, TestStep.next_prefix(prefix, i), deep + 1, *args))
        return ts_sync
    else:
        ts = get_module(tco.type)(prefix=prefix, deep=deep, paras=tco.paras)
        __init_ts(ts, *args)
        return ts


def get_test_step(file: str, show_desc: bool = False):
    path = os.path.abspath(file)
    if not os.path.isfile(path):
        print('tc file path is invalid: {}'.format(file))
        exit(1)
    if show_desc:
        mp_ns = None
    else:
        manager = multiprocessing.Manager()
        mp_ns = manager.Namespace()
    tco = tc_parser_file(path)
    return __tco_to_ts(tco, os.path.dirname(path), 'TestStep', 0, mp_ns)


if __name__ == '__main__':
    '''
    t = get_test_step('../../test.tc')
    print()
    print('-' * 50)
    print()
    ret = t.do_test()
    print()
    print('test result = {}'.format(ret))
    print()
    print('-' * 50)
    print(t._mp_ns)
    '''
    pass
