import re

from gherkan.containers.SignalStatementTreeNode import SignalStatementTreeNode, SignalStatementTreeOperatorNode


class SignalPhrase:
    def __init__(self):
        self.language = None
        self.tempName = None
        self.tempStr = None
        self.tempToNL = None
        self.inclinations = None
        self.vars = {}
        self.valTypes = {}
        self.niceStr = None


class SignalStatementTree():
    dash, line, left, right = '\u2500', '\u2502', '\u251c\u2500\u2500 ', '\u2514\u2500\u2500 '

    def __init__(self, root: SignalStatementTreeNode, string: str):
        self.__root = root
        self.__string = string

    @property
    def root(self):
        return self.__root

    @property
    def string(self):
        return self.__string

    def __printNode(self, node: SignalStatementTreeNode, leftChild, levelsOpened):
        string = ''.join([SignalStatementTree.line + "\t" if lo else "\t" for lo in levelsOpened[:-1]])
        if leftChild:
            if node:
                string += SignalStatementTree.left + str(str(node) if bool(node) else "ERROR!!!") + '\n'
        else:
            if node:
                string += SignalStatementTree.right + str(str(node) if bool(node) else "ERROR!!!") + '\n'

        if type(node) is SignalStatementTreeOperatorNode:
            string += self.__printNode(node.lchild, True, levelsOpened + [True])
            string += self.__printNode(node.rchild, False, levelsOpened + [False])
        return string

    def __str__(self):
        levelsOpened = [False]

        node = self.root
        string = str(node) + '\n'
        if type(node) is SignalStatementTreeOperatorNode:
            string += self.__printNode(node.lchild, True, levelsOpened + [True])
            string += self.__printNode(node.rchild, False, levelsOpened + [False])
        return string



