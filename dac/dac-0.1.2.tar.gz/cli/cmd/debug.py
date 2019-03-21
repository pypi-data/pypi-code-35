from tabulate import tabulate
from cli.utils.Lexer.Lex import Lex

class Debug():

    def main(self, args):
        props = []
        if args['--props'] is not None:
            props = args['--props'].split(',')
        
        with open(args['<file>']) as dac:
            content = Lex(dac.read())
            tab = []
            tab.append(props)
            for block in content.dom.document.blocks:          
                for uuid, line in block.lines.items():
                    s = []
                    for prop in props:
                        if hasattr(line, prop):
                            s.append(getattr(line, prop))
                    tab.append(s)
                    
            if len(props) > 0:
                print(tabulate(tab, headers="firstrow"))