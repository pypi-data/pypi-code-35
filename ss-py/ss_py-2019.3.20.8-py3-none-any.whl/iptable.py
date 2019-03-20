import time
import iptc

TIME_INTERVEL = 0.3
NAME_SSINPUT  = "SS-PY-INPUT"
NAME_SSOUTPUT = "SS-PY-OUTPUT"

class IPTable(object):
    def __init__(self):
        self.initChain()

    def __insertRule(self, chain, dport, sport, protocol, mode):
        rule           = iptc.Rule()
        rule.protocol  = protocol
        match          = iptc.Match(rule,protocol)
        match.protocol = protocol
        match.dport    = dport
        match.sport    = sport
        rule.add_match(match)
        target      = iptc.Target(rule, mode)
        rule.target = target
        chain.insert_rule(rule)

    def delChain(self):
        table = iptc.Table(iptc.Table.FILTER)
        table.delete_chain(NAME_SSINPUT)
        table.delete_chain(NAME_SSOUTPUT)
        self.input  = None
        self.output = None

    def initChain(self):
        self.delChain()
        table       = iptc.Table(iptc.Table.FILTER)
        self.input  = table.create_chain(NAME_SSINPUT)
        self.output = table.create_chain(NAME_SSOUTPUT)
    
    def addPortRule(self, port, isRejct=False):
        mode = "ACCEPT"
        if isRejct:
            mode = "REJECT"
        self.__insertRule(self.input, port, None, "tcp", mode)
        self.__insertRule(self.input, port, None, "udp", mode)
        self.__insertRule(self.output, None, port, "tcp", mode)
        self.__insertRule(self.output, None, port, "udp", mode)
    
    def deletePortRule(self, port, isRejct=False):
        pass
