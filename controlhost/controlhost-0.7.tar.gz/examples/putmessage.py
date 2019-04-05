import socket

import controlhost as ch

s = socket.socket()
host = '131.188.167.62'
port = 5553

s.connect((host, port))

message = ch.Message('foo', 'test')
print(s.send(message.data))

s.close()

