import os,time
from proxer import *
def evilips(l):
 '''
 block a list of IPs
 
 (source: https://kirkkosinski.com/2013/11/mass-blocking-evil-ip-addresses-iptables-ip-sets/)
 '''
 os.system('ipset create evil_ips iphash')
 os.system('ipset flush evil_ips')
 for x in l:
  o='ipset add evil_ips '+x
  os.system(o)

def mass_block(l,duration=3600):
 evilips(l)
 t=time.time()
 os.system('iptables -A INPUT -m set --match-set evil_ips src -j DROP')
 os.system('iptables -A OUPUT -m set --match-set evil_ips dst -j DROP')
 while True:
  if time.time()-t>duration:
   break
 os.system('iptables -D INPUT -m set --match-set evil_ips src -j DROP')
 os.system('ipset flush evil_ips')

def anti_prox(duration=3600):
 li=bane.masshttp()
 li+=massocks4()
 li+=massocks5()
 mass_block(li,duration=duration)
 
def single_block(s,duration=3600):
 '''
 block a single IP
 '''
 t=time.time()
 o='iptables -A INPUT -s {} -j DROP'.format(s)
 os.system(o)
 while True:
  if time.time()-t>duration:
   break
 o='iptables -D INPUT -s {} -j DROP'.format(s)
 os.system(o)
 
def rate_limit(s,count=50,seconds=60,port=80):
 o='iptables -A INPUT -p tcp --dport {} -i eth0 -m state --state NEW -m recent --set'.format(port)
 os.system(o)
 o='iptables -A INPUT -p tcp --dport {} -i eth0 -m state --state NEW -m recent --update --seconds {} --hitcount {} -j DROP'.format(port,seconds,count)
 os.system(o)
 
def anti_loris(port,conn=50):
 '''
 this very useful against both slowloris and bruteforce attacks
 '''
 o='iptables  -A INPUT -p tcp --syn --dport {} -m connlimit --connlimit-above {} -j DROP'.format(port,conn)
 os.system(o)

def anti_spoof():
 '''
 reject invalid packets, it works against: ACK, PSH, ACK-PSH floods...
 '''
 os.system('iptables -t mangle -A PREROUTING -m conntrack --ctstate INVALID -j DROP')
 os.system('iptables -t mangle -A PREROUTING -p tcp ! --syn -m conntrack --ctstate NEW -j DROP')
 os.system('iptables -t mangle -A PREROUTING -p tcp -m conntrack --ctstate NEW -m tcpmss ! --mss 536:65535 -j DROP')
 os.system('iptables -t mangle -A PREROUTING -p tcp --tcp-flags FIN,SYN,RST,PSH,ACK,URG NONE -j DROP')
 os.system('iptables -t mangle -A PREROUTING -p tcp --tcp-flags FIN,SYN FIN,SYN -j DROP')
 os.system('iptables -t mangle -A PREROUTING -p tcp --tcp-flags SYN,RST SYN,RST -j DROP')
 os.system('iptables -t mangle -A PREROUTING -p tcp --tcp-flags FIN,RST FIN,RST -j DROP')
 os.system('iptables -t mangle -A PREROUTING -p tcp --tcp-flags FIN,ACK FIN -j DROP')
 os.system('iptables -t mangle -A PREROUTING -p tcp --tcp-flags ACK,URG URG -j DROP')
 os.system('iptables -t mangle -A PREROUTING -p tcp --tcp-flags ACK,FIN FIN -j DROP')
 os.system('iptables -t mangle -A PREROUTING -p tcp --tcp-flags ACK,PSH PSH -j DROP')
 os.system('iptables -t mangle -A PREROUTING -p tcp --tcp-flags ALL ALL -j DROP')
 os.system('iptables -t mangle -A PREROUTING -p tcp --tcp-flags ALL NONE -j DROP')
 os.system('iptables -t mangle -A PREROUTING -p tcp --tcp-flags ALL FIN,PSH,URG -j DROP')
 os.system('iptables -t mangle -A PREROUTING -p tcp --tcp-flags ALL SYN,FIN,PSH,URG -j DROP')
 os.system('iptables -t mangle -A PREROUTING -p tcp --tcp-flags ALL SYN,RST,ACK,FIN,URG -j DROP')
 
def anti_icmp():
 os.system('iptables -t mangle -A PREROUTING -p icmp -j DROP')
 
def conn_limit(conn=50):
 o='iptables -A INPUT -p tcp -m connlimit --connlimit-above {} -j DROP'.format(conn)
 os.system(o)
 
def anti_frag():
 os.system('iptables -t mangle -A PREROUTING -f -j DROP')
 
def ant_rst():
 os.system('iptables -A INPUT -p tcp --tcp-flags RST RST -m limit --limit 2/s --limit-burst 2 -j ACCEPT')
os.system('iptables -A INPUT -p tcp --tcp-flags RST RST -j DROP')
