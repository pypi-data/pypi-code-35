from cli.utils.Lexer.Lex import Lex
from cli.utils.JitR import JitR

class Render():

    def main(self, args):

        with open(args['<file>']) as dac:
            content = Lex(dac.read())
        
        jitr = JitR(args['--tpl'])
        for block in content.dom.document.blocks:
            jitr.render(block)
        
        for output in jitr.output:
            print(output)
        