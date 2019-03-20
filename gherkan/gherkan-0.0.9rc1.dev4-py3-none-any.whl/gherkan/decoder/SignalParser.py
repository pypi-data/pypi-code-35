import re

from gherkan.containers.SignalStatementTreeNode import SignalStatementTreeOperandNode, \
    SignalStatementTreeOperatorNode
from gherkan.containers.SignalStatementTree import SignalStatementTree
from gherkan.containers.signal_conditional_statement import SignalCondition
from gherkan.decoder.Parser import Parser

import gherkan.utils.constants as c


class SignalParser(Parser):
    def __init__(self):
        super().__init__()

        self.tokens_specs = [  # Regex collection for tokens (operators and operands) that can occur in conditions
            (c.AND, r"&&"),
            (c.OR, r"\|\|"),
            (c.NOT, r"!(?!=)"),
            (c.EQUALITY, r"\w+\s*==\s*\w+"),
            (c.INEQUALITY, r"\w+\s*!=\s*\w+"),
            (c.BOOL, r'(\w+)\s*(?![=,!\(\w]+)'),
            (c.EDGE, r"edge\([\w ,]+\)"),
            (c.FORCE, r"force\([\w ,]+\)"),
            (c.UNFORCE, r"unforce\([\w ,]+\)"),
            (c.LBRACKET, r"(?<!\w)\("),
            (c.RBRACKET, r"\)\s*(?=$|[&\|])"),
            (c.SKIP, r'[ \t]+'),
            (c.MISMATCH, r'.'),
        ]
        self.tok_regex = '|'.join(
            '(?P<%s>%s)' % pair for pair in self.tokens_specs)  # combine regex specifications into one giant regex
        self.operands = frozenset([c.EQUALITY, c.INEQUALITY, c.BOOL, c.EDGE, c.FORCE, c.UNFORCE])
        self.operators = [c.NOT, c.AND, c.OR]  # in the order of precedence/priority from highest to lowest

    def parseStatement(self, statement: str):
        """
        Parses a single conditional statement. Uses the regex token specification (see attributes of this class).

        Parameters
        ----------
        statement : str
            A single conditional statement in the form of a string.

        Returns
        -------
        SignalStatementTree:
            Signal tree containing the root of the extracted tree and the corresponding statement string (input to this function)
        """
        operatorStack = []
        outputStack = []

        # TODO: NOT operator is not handled in case it appears in front of brackets
        for mo in re.finditer(self.tok_regex, statement):
            kind = mo.lastgroup
            value = mo.group()
            if kind in self.operators:
                if len(operatorStack) > 0:
                    topOperator = operatorStack[-1]
                    while len(operatorStack) > 0 and self.operatorAPrecedesB(topOperator, kind) and operatorStack[-1] != c.LBRACKET:
                        outputStack.append(operatorStack.pop())
                        topOperator = operatorStack[-1]
                operatorStack.append(kind)
            elif kind == c.LBRACKET:
                # NOT can be handled here by appling DeMorgan to the entire bracket...
                operatorStack.append(kind)
            elif kind == c.RBRACKET:
                while len(operatorStack) > 0 and operatorStack[-1] != c.LBRACKET:
                    outputStack.append(operatorStack.pop())
                operatorStack.pop()  # pop the left bracket onto the output
                if len(operatorStack) > 0 and operatorStack[-1] == c.NOT:
                    # ...or NOT can be handled here somehow
                    operatorStack.pop()
            elif kind in self.operands:
                if len(operatorStack) > 0 and operatorStack[-1] == c.NOT:
                    negate = True
                    operatorStack.pop()
                else:
                    negate = False
                cond = SignalCondition(value, kind, negate)
                outputStack.append(cond)
            elif kind == c.SKIP:
                continue
            elif kind == c.MISMATCH:
                raise RuntimeError(f'{value!r} unexpected')
        while len(operatorStack) > 0:
            outputStack.append(operatorStack.pop())

        # At this point, the statement has been converted to a suffix notation. Now it needs to be converted into a tree
        if len(outputStack) == 1:  # single node tree
            root = SignalStatementTreeOperandNode(outputStack[0])
        elif len(outputStack) > 1:
            outputStack.reverse()
            root = None
            lastOperatorNode = None
            for item in outputStack:
                if type(item) is str:  # item == operator or bracket
                    node = SignalStatementTreeOperatorNode(item)
                    if lastOperatorNode:
                        lastOperatorNode.attachChild(node)
                    elif root:
                        raise Exception("Multiple roots!")
                    lastOperatorNode = node
                else:  # item == operand
                    node = SignalStatementTreeOperandNode(item)
                    if lastOperatorNode is not None and lastOperatorNode.attachChild(node):
                        lastOperatorNode = lastOperatorNode.getIncompleteParent()
                if not root:
                    root = node
        else:
            raise Exception("Statement parsing resulted in an empty tree!\n{}".format(statement))

        signalTree = SignalStatementTree(root, statement)
        return signalTree

    def operatorAPrecedesB(self, a, b):
        """
        Returns True if "a" has higher priority than "b", returns False otherwise.
        """
        if a in self.operators and b in self.operators:
            return self.operators.index(a) < self.operators.index(b)
        else:
            return None