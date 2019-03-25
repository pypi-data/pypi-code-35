import json, os
from jinja2 import Environment, Template, FileSystemLoader
class CodeGener:
    """
    Init templates 
    """
    def __init__(self, info):
        self.info = info
        tmpldir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
        env = Environment(
            loader=FileSystemLoader(searchpath=tmpldir)
        )

        self.tmpl = {}
        self.tmpl['concreatestate'] = env.get_template('state_tmpl.py')
        self.tmpl['transition_none'] = env.get_template('transition_none.py')
        self.tmpl['transition_ok'] = env.get_template('transition_ok.py')
        self.tmpl['absstate'] = env.get_template('state.py')
        self.tmpl['state_enum'] = env.get_template('state_enum.py')
        self.tmpl['ctx'] = env.get_template('context.py')
        self.tmpl['ctx_transition'] = env.get_template('ctx_transition.py')
        self.tmpl['import'] = env.get_template('import.py')

        self.codeinfo = {}

    def genCode(self):
        self.genAbsStateCode()
        self.genStatesCode()
        self.genContextCode()
        return self.codeinfo

    def genAbsStateCode(self):
        transition_code_arr = []
        for t in self.info['transitionnames']:
            transition_code_arr.append(self.tmpl['transition_none'].render(transition=t))
        transition_code = '\n'.join(transition_code_arr) + '\n'
        state_enum_code = '\n'.join([self.tmpl['state_enum'].render(state=s, index=i) for i, s in enumerate(self.info['statenames'])]) + '\n'
        state_code = self.tmpl['absstate'].render(state_enum_code=state_enum_code)
        self.codeinfo['state.py'] = '\n'.join([state_code, transition_code]) + '\n' 
 
    def genStatesCode(self):
        """
        Generate code file according to self.content
        codeinfo = {
            '<filename>': '<code>',
        }
        """
        for s, d in self.info['machine'].items():
            transition_code_arr = []
            for t in self.info['transitionnames']:
                tcode = self.tmpl['transition_none'].render(transition=t)
                if t in d['transitions'].keys():
                    tcode = self.tmpl['transition_ok'].render(transition=t, post=d['transitions'][t])
                transition_code_arr.append(tcode)
            transition_code = '\n'.join(transition_code_arr) + '\n'
            state_code = self.tmpl['concreatestate'].render(state=s.title(), description=d['description'])
            self.codeinfo[s.lower()+".py"] = '\n'.join([state_code, transition_code]) + '\n'

    def genContextCode(self):
        """
        Generate code file according to self.states, self.initstate, self.initaction
        """
        states_code = '['+', '.join([s.title()+'()' for s in self.info['statenames']])+']'
        import_code = '\n'.join([self.tmpl['import'].render(pkg=s.lower(), api=s.title()) for s in self.info['statenames']])
        transition_code = '\n'.join([self.tmpl['ctx_transition'].render(transition=t) for t in self.info['transitionnames']])
        self.codeinfo['context.py'] = self.tmpl['ctx'].render({"states": states_code, "initaction": self.info['initaction'], "import_code": import_code, "transition_code": transition_code})
