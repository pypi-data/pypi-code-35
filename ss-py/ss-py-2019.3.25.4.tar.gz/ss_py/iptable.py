import time
from netfilter.rule import Rule,Match
from netfilter.table import Table

NAME_SSINPUT  = "SS-PY-INPUT"
NAME_SSOUTPUT = "SS-PY-OUTPUT"

class IPTable(object):
    def __init__(self):
        self.table  = Table('filter')
        self.ports  = {}
        self.reject = []

    def __loadRule(self, dport, sport, protocolStr, mode):
        if dport != None:
            portStr = '--dport ' + str(dport)
        if sport != None:
            portStr = '--sport ' + str(sport)
        rule = Rule(protocol=protocolStr,matches=[Match(protocolStr, portStr)],jump=mode)
        return rule

    def __AddOrDelRule(self, chainName, dport, sport, protocolStr, mode, isDel=False):
        rule = self.__loadRule(dport, sport, protocolStr, mode)
        if isDel:
            self.table.delete_rule(chainName, rule)
        else:
            self.table.append_rule(chainName, rule)

    def __getPortFlow(self, port):
        byte  = 0
        rule  = self.__loadRule(port, None, "tcp", "ACCEPT")
        rule2 = self.__loadRule(port, None, "udp", "ACCEPT")
        array = self.table.list_rules(NAME_SSINPUT)
        tmp   = rule2.find(array)
        if tmp != None:
            byte = byte + tmp.bytes
        tmp   = rule.find(array)
        if tmp != None:
            byte = byte + tmp.bytes

        rule  = self.__loadRule(None, port, "tcp", "ACCEPT")
        rule2 = self.__loadRule(None, port, "udp", "ACCEPT")
        array = self.table.list_rules(NAME_SSINPUT)
        tmp   = rule2.find(array)
        if tmp != None:
            byte = byte + tmp.bytes
        tmp   = rule.find(array)
        if tmp != None:
            byte = byte + tmp.bytes
        return byte

    def delChain(self):
        rule1 = Rule(jump=NAME_SSINPUT)
        rule2 = Rule(jump=NAME_SSOUTPUT)
        arr   = self.table.list_rules('INPUT')
        temp  = rule1.find(arr)
        if temp != None:
            self.table.delete_rule('INPUT', temp)
        arr   = self.table.list_rules('OUTPUT')
        temp  = rule1.find(arr)
        if temp != None:
            self.table.delete_rule('OUTPUT', temp)

        list = self.table.list_chains()
        if NAME_SSINPUT in list:
            # arr = self.table.list_rules(NAME_SSINPUT)
            # for item in arr:
            #     self.table.delete_rule(NAME_SSINPUT, item)
            self.table.flush_chain(NAME_SSINPUT)
            self.table.delete_chain(NAME_SSINPUT)
        if NAME_SSOUTPUT in list:
            # arr = self.table.list_rules(NAME_SSOUTPUT)
            # for item in arr:
            #     self.table.delete_rule(NAME_SSOUTPUT, item)
            self.table.flush_chain(NAME_SSOUTPUT)
            self.table.delete_chain(NAME_SSOUTPUT)


    def initChain(self):
        self.delChain()
        self.table.create_chain(NAME_SSINPUT)
        self.table.create_chain(NAME_SSOUTPUT)
        rule1 = Rule(jump=NAME_SSINPUT)
        rule2 = Rule(jump=NAME_SSOUTPUT)
        self.table.append_rule('INPUT',rule1)
        self.table.append_rule('OUTPUT',rule2)

    def addPortRule(self, port, isRejct=False):
        if isRejct:
            mode = "REJECT"
            if port not in self.reject:
                self.reject.append(port)
            else:
                return
        else:
            mode = "ACCEPT" 
            if port not in self.ports:
                self.ports[port] = 0
            else:
                return
        self.__AddOrDelRule(NAME_SSINPUT, port, None, "tcp", mode)
        self.__AddOrDelRule(NAME_SSINPUT, port, None, "udp", mode)
        self.__AddOrDelRule(NAME_SSOUTPUT, None, port, "tcp", mode)
        self.__AddOrDelRule(NAME_SSOUTPUT, None, port, "udp", mode)
    
    def deletePortRule(self, port, isRejct=False):
        if isRejct:
            mode = "REJECT"
            if port in self.reject:
                self.reject.remove(port)
            else:
                return
        else:
            mode = "ACCEPT" 
            if port in self.ports:
                self.ports.pop(port)
            else:
                return
        self.__AddOrDelRule(NAME_SSINPUT, port, None, "tcp", mode, True)
        self.__AddOrDelRule(NAME_SSINPUT, port, None, "udp", mode, True)
        self.__AddOrDelRule(NAME_SSOUTPUT, None, port, "tcp", mode, True)
        self.__AddOrDelRule(NAME_SSOUTPUT, None, port, "udp", mode, True)
    
    def getPortsFlowIncrease(self):
        increase = {}
        for port in self.ports:
            flow = self.__getPortFlow(port)
            increase[port]   = flow - self.ports[port]
            self.ports[port] = flow
        return increase

# ta = IPTable()
# ta.initChain()
# ta.addPortRule(8089)
# t = 0