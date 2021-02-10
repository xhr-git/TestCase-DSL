from core.include import *
import socket

default_client = 'host_default_client_random__'
default_port = 8000


class ts_send_data(TestStep):
    desc = 'send data to server, client={}'

    def __init__(self, prefix, deep, paras):
        self.clt_name = paras.get('client', default_client)
        super().__init__(desc=self.desc.format(self.clt_name),
                         prefix=prefix, deep=deep, paras=paras)

    def action(self):
        data = self.clt_name
        clt: socket.socket = self.get_del_global(self.clt_name)
        clt.send(data.encode())
        clt.close()
        self.log('send data server successfully (client={})'.format(self.clt_name))
        return 0


if __name__ == '__main__':
    pass

