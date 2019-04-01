import time
import tdt

host = '10.10.10.117'

udp = tdt.TDTUDP(host=host, send_type=int, recv_type=int)

ct = 0
while 1:
    ct += 1
    udp.send([ct for i in range(6)])