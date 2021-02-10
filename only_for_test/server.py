import threading
import socket


def worker(c: socket.socket, i: int):
    data = c.recv(1024).decode()
    print('[{}] recv: {}'.format(i, data))
    c.shutdown(socket.SHUT_WR)
    print('[{}] end {}'.format(i, '*' * 30))
    # c.close()


s = socket.socket()

host = socket.gethostname()
print(host)
port = 8000
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))

s.listen(5)
i = 0
while True:
    i = i + 1
    c, addr = s.accept()
    print("[{}] got connection from {}".format(i, addr))
    t = threading.Thread(target=worker, args=(c, i,))
    t.start()
