import json
from jinja2 import Environment, Template, FileSystemLoader
class Parser:
    """
    parse the state, transition and init configuration
    """
    def __init__(self, stateConf, initConf):
        self.stateConf, self.initConf = stateConf, initConf
        self.info = {}
        self.info['statenames'], self.info['transitionnames'] = [], []
        self.info['initstate'], self.info['initaction'] = '', ''
        self.parse()

    def parse(self):
        content = {}
        with open(self.stateConf, 'r') as f:
            data = json.load(f)
            self.info['statenames'] = list(data.keys())
            self.info['transitionnames'] = list(set([x for y in [d['transitions'].keys() for s, d in data.items()] for x in y]))
            self.info['machine'] = data

        with open(self.initConf, 'r') as f:
            data = json.load(f)
            self.info['initstate'], self.info['initaction'] = data['state'], data['action']
        self.info['statenames'].remove(self.info['initstate'])
        self.info['statenames'].insert(0, self.info['initstate'])

