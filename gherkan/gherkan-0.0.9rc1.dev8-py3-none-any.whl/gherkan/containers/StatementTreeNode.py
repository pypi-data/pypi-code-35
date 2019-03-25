# -*- coding: utf-8 -*-
from gherkan.utils import constants as c


class StatementTreeNode():
    def __init__(self, kind, parent):
        self.kind = kind
        self.parent = parent

    def negate(self):
        if self.kind == c.AND:
            self.kind = c.OR
        elif self.kind == c.OR:
            self.kind = c.AND
        elif self.kind == c.EQUALITY:
            self.kind = c.INEQUALITY
        elif self.kind == c.INEQUALITY:
            self.kind = c.EQUALITY
        elif self.kind == c.BOOL:
            self.data.value = not self.data.value
        elif self.kind == c.FORCE:
            self.kind = c.UNFORCE
        elif self.kind == c.UNFORCE:
            self.kind = c.FORCE
        else:
            raise NotImplementedError("Cannot negate {}".format(self.kind))


class StatementTreeBinaryOperatorNode(StatementTreeNode):
    def __init__(self, kind, parent=None):
        super().__init__(kind, parent)
        self.lchild = None
        self.rchild = None

    def __str__(self):
        return 'Operator(type: {})'.format(self.kind)


class StatementTreeOperandNode(StatementTreeNode):
    def __init__(self, kind, parent=None):
        super().__init__(kind, parent)
        self.data = StatementTreeNodeData()

    def __str__(self):
        return 'Operand(type: {}, variable: {}, value: {}, variableNLP: {})'.format(
            self.kind, self.data.variable, self.data.value, self.data.variableNL)

class StatementTreeMergedNode(StatementTreeNode):
    def __init__(self, kind="MERGED_NODE", parent=None):
        super().__init__(kind, parent)
        self.subnodes = []
        self.data = StatementTreeNodeData()

    def __str__(self):
        return 'MergedNode(contains {} nodes)'.format(len(self.subnodes))

class StatementTreeNodeData():
    def __init__(self):
        self.string = None
        self.variable = None
        self.value = None
        self.variableNL = None
        self.valueId = None