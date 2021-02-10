import socket

s = socket.socket()

host = socket.gethostname()
port = 8000

s.connect((host, port))
data = 'I\'m XHR'
s.send(data.encode())
s.close()
