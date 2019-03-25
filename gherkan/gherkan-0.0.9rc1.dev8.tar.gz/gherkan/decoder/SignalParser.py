# -*- coding: utf-8 -*-
from gherkan.containers.StatementTree import StatementTree
from gherkan.decoder.Parser import Parser

from lark import Lark

class SignalParser(Parser):
    def __init__(self):
        super().__init__()

        self.statement_grammar = """
            ?start: expression

            ?expression: statement
                | "(" expression ")"
                | expression "&&" expression       -> and
                | expression "||" expression       -> or
                | "!" "(" expression ")"           -> not

            ?statement: function
                | NAME "==" atom                -> equality
                | NAME "!=" atom                -> inequality
                | NAME                          -> bool
                | "!" statement                 -> not

            ?function: function_name "(" NAME "," atom ")"

            ?function_name: "edge"           -> edge 
                          | "force"          -> force
                          | "unforce"        -> unforce
            
            ?atom: NAME
                | NUMBER

            %import common.CNAME -> NAME
            %import common.NUMBER
            %import common.WS_INLINE

            %ignore WS_INLINE
        """


    def parseStatement(self, statement: str):
        parser = Lark(self.statement_grammar, parser='earley', ambiguity='resolve', propagate_positions=True)
        tree = parser.parse(statement)

        print(tree.pretty())

        st = StatementTree(statement)
        st.buildFromSignalTree(tree)

        print(st)

        return st
