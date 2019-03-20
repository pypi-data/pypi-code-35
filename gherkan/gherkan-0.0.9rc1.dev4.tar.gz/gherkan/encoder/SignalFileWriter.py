from gherkan.containers.signal_batch import SignalBatch
from gherkan.containers.SignalStatementTreeNode import SignalStatementTreeOperatorNode, \
    SignalStatementTreeNode, SignalStatementTreeOperandNode
from gherkan.containers.SignalStatementTree import SignalStatementTree
from gherkan.processing.TreeProcessor import TreeProcessor

import gherkan.utils.constants as c
import gherkan.utils.gherkin_keywords as g

import warnings

class SignalFileWriter():
    """ TODO docs """

    def __init__(self, nlBatch : SignalBatch):
        self.nlBatch = nlBatch
        self.outLines = []
        self.language = nlBatch.language

        self.encode(nlBatch)

    def encode(self, nlBatch: SignalBatch):
        self.outLines.append("# language: {}\n\n".format(self.language))
        self.outLines.append("{}: {}\n".format(g.FEATURE, nlBatch.name))
        self.outLines.append("  {}\n".format(nlBatch.desc))

        if nlBatch.context:
            self.outLines.append("{}:\n".format(g.BACKGROUND))
            self.outLines.append("  {} {}\n\n".format(g.GIVEN, self.tree_to_str(nlBatch.context)))

        for scenario in nlBatch.scenarios:
            self.outLines.append("{}: {}\n".format(g.SCENARIO, scenario.name))

            for tree in scenario.givenStatements:
                self.outLines.append("  {} {}\n".format(g.GIVEN, self.tree_to_str(tree)))
            for tree in scenario.whenStatements:
                self.outLines.append("  {} {}\n".format(g.WHEN, self.tree_to_str(tree)))
            for tree in scenario.thenStatements:
                self.outLines.append("  {} {}\n".format(g.THEN, self.tree_to_str(tree)))

    def write(self, outputFilePath: str):
       with open(outputFilePath, "w") as out:
           out.writelines(self.outLines)

    def tree_to_str(self, tree: SignalStatementTree):
        tp = TreeProcessor(self.language)

        # loads yaml file with templates
        tp.load_templ_dic('utils/templates_dic.yaml')
        tp.process_tree(tree.root, TreeProcessor.Direction.NL_TO_SIGNAL)

        return self.node_to_str(tree.root)

    def node_to_str(self, node: SignalStatementTreeNode):
        if type(node) == SignalStatementTreeOperatorNode:
            return self.operator_to_str(node)
        elif type(node) == SignalStatementTreeOperandNode:
            return self.operand_to_str(node)

    def operator_to_str(self, node: SignalStatementTreeOperatorNode):
        if node.kind == c.AND:
            operator = "&&"
        elif node.kind == c.OR:
            operator = "||"
        else:
            raise NotImplementedError("Unrecognized operator {}".format(node.kind))

        return ("({}) {} ({})".format(
            self.node_to_str(node.lchild),
            operator,
            self.node_to_str(node.rchild)))

    def operand_to_str(self, node: SignalStatementTreeOperandNode):
        kind = node.data.kind

        # TODO make node.data.kind uppercase as well
        if kind:
            kind = kind.upper()

        if kind == c.EQUALITY:
            return "{} == {}".format(
                node.data.variable,
                node.data.value
            )
        elif kind == c.INEQUALITY:
            return  "{} != {}".format(
                node.data.variable,
                node.data.value
            )
        elif kind == c.BOOL:
            return "{} is {}".format(
                node.data.variable,
                node.data.value
            )
        elif kind in [c.EDGE,
                      c.FORCE,
                      c.UNFORCE]:
            return "{}({}, {})".format(
                node.data.kind,
                node.data.variable,
                node.data.value
            )
        # else:
        #     warnings.warn("Node kind {} not recognized!".format(kind))