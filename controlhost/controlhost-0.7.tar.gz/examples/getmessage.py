import socket

import controlhost as ch

s = socket.socket()
host = '131.188.167.62'
port = 5553

s.connect((host, port))

message = ch.Message('_Subscri', ' w foo')
print(s.send(message.data))

message = ch.Message('_Always')
print(s.send(message.data))

print(s.recv(1024))

s.close()

