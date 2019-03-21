# -*- coding: utf-8 -*-
from gherkan.containers.signal_batch import SignalBatch
from gherkan.containers.StatementTreeNode import StatementTreeBinaryOperatorNode, \
    StatementTreeNode, StatementTreeOperandNode, StatementTreeMergedNode
from gherkan.containers.StatementTree import StatementTree
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

    def tree_to_str(self, tree: StatementTree):
        tp = TreeProcessor(self.language)

        # loads yaml file with templates
        tp.load_templ_dic('utils/templates_dic.yaml')
        tree.root = tp.process_tree(tree.root, TreeProcessor.Direction.NL_TO_SIGNAL)

        return self.node_to_str(tree.root)

    def node_to_str(self, node: StatementTreeNode):
        if type(node) == StatementTreeBinaryOperatorNode:
            return self.operator_to_str(node)
        elif type(node) == StatementTreeMergedNode:
            return self.merged_operator_to_str(node)
        elif type(node) == StatementTreeOperandNode:
            return self.operand_to_str(node)

    def merged_operator_to_str(self, node: StatementTreeMergedNode):
        return " && ".join([self.operand_to_str(subnode) for subnode in node.subnodes])

    def operator_to_str(self, node: StatementTreeBinaryOperatorNode):
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

    def operand_to_str(self, node: StatementTreeOperandNode):
        kind = node.kind

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
            return "{}{}".format(
                "" if node.data.value else "! ",
                node.data.variable,
            )
        elif kind in [c.EDGE,
                      c.FORCE,
                      c.UNFORCE]:
            return "{}({}, {})".format(
                node.kind,
                node.data.variable,
                node.data.value
            )
        elif kind == "ACTION":
            # TODO recognize action by NL2Temp
            return "{}({}, {})".format(
                node.kind,
                node.data.variable,
                node.data.value
            )
        else:
            warnings.warn("Node kind {} not recognized!".format(kind))