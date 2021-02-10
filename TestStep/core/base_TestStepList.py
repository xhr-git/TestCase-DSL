from base_TestStep import TestStep
from find_test_step import get_module
from multiprocessing import Process
import time
import os
import sys


class ts_item:
    def __init__(self, name: str, paras: dict = None):
        self.name: str = name
        self.paras: dict = paras
        if paras is None:
            self.paras = {}

    def show(self):
        print(f'  {self.name}\tparas= {self.paras}')


# Do not instantiate the class directly
class __TestStepList(TestStep):
    def __init__(self, desc: str = None, prefix: str = None, deep: int = 0, paras: dict = None, _list: list = None):
        super().__init__(desc=desc, prefix=prefix, deep=deep, paras=paras)
        self.stepList = []
        if _list is None:
            return
        i = 0
        for step in _list:
            step: ts_item
            print(step.__class__)
            print(ts_item)
            assert step.__class__ == ts_item
            i = i + 1
            ts: TestStep = get_module(step.name)(prefix=self.next_prefix(prefix, i), deep=deep+1, paras=step.paras)
            self.stepList.append(ts)

    def show_desc(self):
        super().show_desc()
        for step in self.stepList:
            step.show_desc()

    def exit_pid(self, sig: int):
        ans = 0
        for step in self.stepList:
            p: Process = step.proc
            if p is not None:
                if p.is_alive():
                    self.log('pid-{} list kill pid-{}'.format(os.getpid(), p.pid))
                    p.terminate()
                p.join()
                ret = p.exitcode
                step.proc = None
                p.close()
                step.log('exit ret = {}'.format(ret))
                if ret != 0:
                    ans = ret
        return ans


class TestStepSeq(__TestStepList):
    def __init__(self, desc: str = None, prefix: str = None, deep: int = 0, paras: dict = None, _list: list = None):
        super().__init__(desc=desc, prefix=prefix, deep=deep, paras=paras, _list=_list)

    def action(self):
        # self.log('start, paras={}'.format(self.paras))
        for step in self.stepList:
            ret = step.do_test()
            if ret != 0:
                return ret
        return 0


class TestStepSync(__TestStepList):
    __test_sync_exit = 123

    def __init__(self, desc: str = None, prefix: str = None, deep: int = 0, paras: dict = None, _list: list = None):
        super().__init__(desc=desc, prefix=prefix, deep=deep, paras=paras, _list=_list)
        if self.desc is None:
            self.desc = ''
        self.desc = '[Concurrent] ' + self.desc
        if self.duration is not None:
            if self.timeout <= 0:
                self.timeout = 20  # Leave a margin of 20 seconds
            self.timeout = self.timeout + self.duration

    def action(self):
        class SyncStep:
            def __init__(self, __step: TestStep):
                self.step: TestStep = __step
                self.loop: int
                self.i = 0
                if __step.loop == 0:
                    self.loop = 1
                else:
                    self.loop = __step.loop
                assert self.loop >= 1

            def start(self, __start_time):
                assert self.step.proc is None
                self.step.start_time = __start_time
                self.i = self.i + 1
                if self.loop > 1:
                    self.step._loop_times(self.i)
                self.step.proc = Process(target=self.step._action_in_mp)
                self.step.proc.start()

            def stop(self):
                __p = self.step.proc
                assert __p is not None
                if __p is not None:
                    if __p.is_alive():
                        __p.terminate()
                    __p.join()
                    __ret = __p.exitcode
                    self.step.proc = None
                    __p.close()
                    return __ret
                else:
                    return 0

            def is_finish(self, __now_time):
                if 0 < self.step.timeout <= __now_time - self.step.start_time:
                    self.step.print_timeout()
                    return self.stop()
                if not self.step.proc.is_alive():
                    self.step.proc.join()
                    __ret = self.stop()
                    if __ret != 0:
                        self.step.print_fail()
                    return __ret
                return None

        t_list: list = []
        for step in self.stepList:
            t_list.append(SyncStep(step))
        start_time = self.start_time = time.time()
        for t in t_list:
            t.start(start_time)
        ans = 0
        while True:
            time.sleep(0.33)
            now_time = time.time()
            if self.duration is not None and now_time - start_time >= self.timeout:
                self.print_timeout()
                break
            alive_proc = 0
            __rm_t_list = []
            for t in t_list:
                t: SyncStep
                ret = t.is_finish(now_time)
                if ret is None:
                    alive_proc = alive_proc + 1
                else:
                    if ret != 0:
                        ans = ret
                        alive_proc = 0
                        break
                    else:
                        if t.i < t.loop:
                            t.start(now_time)
                            alive_proc = alive_proc + 1
                        else:
                            __rm_t_list.append(t)
            for t in __rm_t_list:
                t_list.remove(t)
            if alive_proc == 0:
                break
        ret = self.exit_pid(self.__test_sync_exit)
        if ans == 0 and ret != 0:
            ans = ret
        return ans


if __name__ == '__main__':
    pass
