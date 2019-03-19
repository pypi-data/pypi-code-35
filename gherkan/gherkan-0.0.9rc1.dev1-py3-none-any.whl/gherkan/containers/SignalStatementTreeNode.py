from gherkan.containers.signal_conditional_statement import SignalCondition


class SignalStatementTreeNode():

    def __init__(self, kind=None, data=None):
        self.__lchild = None
        self.__rchild = None
        self.__kind = kind
        self.__data = data
        self.__parent = None

    def setParent(self, parent):
        self.__parent = parent

    @property
    def kind(self):
        return self.__kind

    @property
    def parent(self):
        return self.__parent

    @property
    def data(self):
        return self.__data

    @property
    def lchild(self):
        return self.__lchild

    @property
    def rchild(self):
        return self.__rchild

    @property
    def getIncompleteParent(self):
        raise NotImplementedError()


class SignalStatementTreeOperatorNode(SignalStatementTreeNode):
    def __init__(self, kind):
        super().__init__(kind)
        self.__lchild = None  # type: SignalStatementTreeNode
        self.__rchild = None  # type: SignalStatementTreeNode
        self.templateID = None
        self.variableNLP = None
        self.variableNL_full = None
        self.variableNLPCZ = None
        self.variableNL_full_cs = None

    @property
    def lchild(self):
        return self.__lchild

    @property
    def rchild(self):
        return self.__rchild

    @property
    def children(self):
        return [self.lchild, self.rchild]

    @property
    def full(self):
        return (self.lchild is not None) and (self.rchild is not None)

    def getIncompleteParent(self):
        if self.full:
            if self.parent:
                return self.parent.getIncompleteParent()
            else:
                return None
        else:
            return self

    def attachChild(self, child: SignalStatementTreeNode):
        """
        Returns True if the node is "full" (i.e. both children are assigned)
        """
        child.setParent(self)
        if self.lchild:
            self.__rchild = child
            return True
        else:
            self.__lchild = child
            return False

    def __str__(self):
        return 'Operator(type: {})'.format(self.kind.upper())


class SignalStatementTreeOperandNode(SignalStatementTreeNode):

    def __init__(self, data: SignalCondition):
        super().__init__(data.kind, data)

    def getIncompleteParent(self):
        self.parent.getIncompleteParent()

    def __str__(self):
        return 'Operand(type: {}, variable: {}, value: {}, variableNLP: {}, variableNL_full: {})'.format(
            self.kind.upper() if self.kind else 'None', self.data.variable, self.data.value, self.data.variableNLP,
            self.data.variableNL_full)

    @property
    def variable(self):
        return self.data.variable

    @property
    def kind(self):
        return self.data.kind

    @property
    def variableNLP(self):
        return self.data.variableNLP

    @property
    def variableNL_full(self):
        return self.data.variableNL_full

    @property
    def value(self):
        return self.data.value
