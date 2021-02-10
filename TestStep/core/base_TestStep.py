from multiprocessing import Process
from functools import wraps
import os
import time
import signal
import sys
import datetime

max_deep = 100
g_val = None


def sig_handler(sig: int, frame):
    global g_val
    ret = g_val.exit_pid(sig)
    exit(ret)


def _in_mp(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        global g_val
        g_val = self
        signal.signal(signal.SIGINT, sig_handler)
        signal.signal(signal.SIGTERM, sig_handler)
        ret = func(self, *args, **kwargs)
        assert ret is not None
        if ret != 0:
            self.print_fail()
        exit(ret)

    return wrapper


def _may_in_mp(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        global g_val
        g_val = self
        if self.timeout > 0:
            signal.signal(signal.SIGINT, sig_handler)
            signal.signal(signal.SIGTERM, sig_handler)
        ret = func(self, *args, **kwargs)
        assert ret is not None
        # s = 'timeout = {}'.format(self.timeout)
        if self.timeout > 0:
            # self.log(f'exit !!!! {s} ret = {ret}')
            exit(ret)
        # self.log(f'return !!!! {s} ret = {ret}')
        return ret

    return wrapper


def _loop_multiple_times(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        loop = self.loop
        i = 0
        assert loop >= 0
        ret = None
        if loop == 0:
            ret = func(self, *args, **kwargs)
            assert ret is not None
        else:
            while i < loop:
                i = i + 1
                self._loop_times(i)
                ret = func(self, *args, **kwargs)
                assert ret is not None
                if ret != 0:
                    break
        return ret

    return wrapper


# Do not instantiate the class directly
class TestStep:
    def __init__(self, desc: str = None, prefix: str = 'TestStep', deep: int = 0, paras: dict = None):
        self.name: str = self.__class__.__name__
        self.desc: str = desc
        self.prefix: str = prefix
        self.paras: dict = paras
        self.proc: Process = None
        self.timeout: float = paras.get('timeout', 0)
        self.loop: int = int(paras.get('loop', 0))
        self.duration: float = paras.get('duration')
        self.start_time: float = 0
        self._loop_str: str = ''
        self._mp_ns = None
        if deep >= max_deep:
            print('Illegal recursive nesting: {}'.format(self.name))
            exit(max_deep)
        self.deep: int = deep + 1

    # This method must NOT be overridden in a subclass
    @_may_in_mp
    def _action_may_in_mp(self):
        self.print_start()
        self.start_time = time.time()
        ret = self.action()
        # self.log('normal quit ret={}!!'.format(ret))
        return ret

    # This method must NOT be overridden in a subclass
    @_in_mp
    def _action_in_mp(self):
        self.print_start()
        ret = self.action()
        # self.log('normal quit ret={}!!'.format(ret))
        return ret

    @staticmethod
    def next_prefix(p: str, n: int):
        return '  ' + p + '-' + str(n)

    def show_desc(self):
        print(' {} [{}] {}: {}'.
              format(self.prefix, self.name, self.desc, self.paras))

    def log(self, s: str):
        print('[{}] {}{} PID-{}: {}'.
              format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f'),
                     self.prefix, self._loop_str, os.getpid(), s))

    def exit_pid(self, sig: int):
        self.log('exit sig = {}'.format(sig))
        return sig

    def action(self):
        print('[{}][{}] No "action" method implemented'.format(self.name, self.desc))
        raise NotImplemented

    # This method must NOT be overridden in a subclass
    @_loop_multiple_times
    def do_test(self):
        if self.timeout > 0:
            self.proc = Process(target=self._action_may_in_mp)
            self.proc.start()
            self.proc.join(self.timeout)
            if self.proc.is_alive():
                self.print_timeout()
                self.log('pid-{} kill pid-{}'.format(os.getpid(), self.proc.pid))
                self.proc.terminate()
            if self.proc.is_alive():
                assert 'terminate : but proc is alive {}'.format(self.name)
            self.proc.join()
            ret = self.proc.exitcode
            self.proc.close()
            self.proc = None
        else:
            ret = self._action_may_in_mp()
        if ret != 0:
            self.print_fail()
        return ret

    def set_global_val(self, name: str, val, force: bool = True):
        if force:
            self._mp_ns.__setattr__(name, val)
        else:
            v = self.get_global_val(name)
            if v is None:
                self._mp_ns.__setattr__(name, val)
            else:
                print('The field has been assigned: {}'.format(name))

    def del_global_val(self, name: str):
        try:
            self._mp_ns.__delattr__(name)
        except:
            pass

    def get_del_global(self, name: str):
        v = self.get_global_val(name)
        self.del_global_val(name)
        return v

    def get_global_val(self, name: str):
        try:
            v = self._mp_ns.__getattr__(name)
            return v
        except Exception as e:
            print('no attr: {}'.format(e))
            return None

    def time_up(self):
        if self.duration is None:
            return False
        return time.time() - self.start_time >= self.duration

    def _loop_times(self, idx: int):
        assert idx > 0
        self._loop_str = f' loop-{idx}'

    def print_start(self):
        print()
        self.log(f'[start{self._loop_str}] {self.desc}   [{self.name}] {self.paras}')

    def print_fail(self):
        print()
        self.log(f'This step is fail!  {self.desc}   [{self.name}] {self.paras}')
        print()

    def print_timeout(self):
        print()
        self.log(f'This step is timeout!  {self.desc}   [{self.name}] {self.paras}')
        print()


if __name__ == '__main__':
    pass
