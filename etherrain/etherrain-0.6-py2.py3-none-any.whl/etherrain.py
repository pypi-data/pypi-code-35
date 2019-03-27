import requests
import logging

class EtherRain:
    def __init__(self, addr, user, pw, timeout):
        self.addr = addr
        self.user = user
        self.pw = pw
        self.timeout = timeout
        self.status = {}
        self.status['ac'] = ''
        self.status['os'] = ''
        self.status['cs'] = ''
        self.status['rz'] = ''
        self.status['ri'] = ''
        self.status['rn'] = ''
            

    def _request(self, uri):
        try:
            req = requests.get(uri, timeout=self.timeout)
        except requests.exceptions.ConnectionError:
            print("Received a bad status line from EtherRain")
            return False

        if not req.ok:
            print("Connection error logging into EtherRain")
            return False

        return req

    def login(self):
        # ergetcfg.cgi?lu=admin\&lp=deadbeef
        uri = "http://{0}/ergetcfg.cgi?lu={1}&lp={2}".format(self.addr,self.user,self.pw)
        ret = self._request(uri)
        if not ret.ok:
            print("Unable to log in")
            return False
        if "Guest" in ret.text:
            print("Invalid username or password")
            return False
        return True 

    def stop(self):
        uri = 'http://{0}/result.cgi?xr'.format(self.addr)
        return self._request(uri)

    # retrieve current status
    # http://<addr>/result.cgi?xs
    #
    # <body>
    #       EtherRain Device Status <br>
    #       un:EtherRain 8
    #       ma: 01.00.44.03.0A.01  <br>
    #       ac: <br>
    #       os: RD <br>
    #       cs: OK <br>
    #       rz: UK <br>
    #       ri: 0 <br>
    #       rn: 0 <br>
    # </body>
    #
    def update_status(self):
        uri = "http://{0}/result.cgi?xs".format(self.addr)
        ret = self._request(uri)

        if ret is False:
            self.status['cs'] = "nr"
            self.status['os'] = ''
            self.status['rn'] = '0'
            return False

        for b_line in ret.iter_lines():
            line = b_line.decode('utf8').strip()
            if ":" in line:
                attr,value=line.split(":")
                value = value.replace(" <br>","").strip()
                attr = attr.strip()
                if attr in [ 'ac', 'os', 'cs', 'rz', 'ri', 'rn' ] :
                    self.status[attr]=value
        return True

    def get_status(self):
        return self.status

    def operating_state(self):
        return self.status['os']

    def rain(self):
        return self.status['rn']

    def last_valve(self):
        l = int(self.status['ri'])
        return l+1

    def irrigate(self, valve, time):
        valve = valve - 1
        out = "0:"       # Start with a delay of "0" minutes.
        out = out + valve * "0:"
        out = "{0}{1}".format(out,time)
        out = out + (7-valve)*":0"
        uri = "http://{0}/result.cgi?xi={1}".format(self.addr, out)
        return self._request(uri)
