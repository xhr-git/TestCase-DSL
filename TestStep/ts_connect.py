from core.include import *
import socket

default_client = 'host_default_client_random__'  # DO NOT use the prefix "__"
default_port = 8000


class ts_connect(TestStep):
    desc = 'connect to a server, client={}'

    def __init__(self, prefix, deep, paras):
        self.clt_name = paras.get('client', default_client)
        super().__init__(desc=self.desc.format(self.clt_name),
                         prefix=prefix, deep=deep, paras=paras)

    def action(self):
        s = socket.socket()
        host = socket.gethostname()
        s.connect((host, default_port))
        self.set_global_val(self.clt_name, s)
        self.log('connect to server successfully (client={})'.format(self.clt_name))
        s.close()
        return 0


if __name__ == '__main__':
    pass

