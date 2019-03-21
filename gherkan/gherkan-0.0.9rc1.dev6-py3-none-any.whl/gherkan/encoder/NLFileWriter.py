# -*- coding: utf-8 -*-
from gherkan.containers.signal_batch import SignalBatch
from gherkan.containers.StatementTreeNode import StatementTreeBinaryOperatorNode, \
    StatementTreeNode, StatementTreeOperandNode, StatementTreeMergedNode
from gherkan.containers.StatementTree import StatementTree
from gherkan.processing.TreeProcessor import TreeProcessor
import gherkan.utils.gherkin_keywords as g

class NLFileWriter():
    """ TODO docs """

    def __init__(self, signalBatch : SignalBatch):
        self.signalBatch = signalBatch
        self.outLines = []
        self.language = signalBatch.language

        self.encode(signalBatch)

    def encode(self, signalBatch: SignalBatch):
        self.outLines.append("# language: {}\n\n".format(self.language))
        self.outLines.append("{}: {}\n".format(g.FEATURE, signalBatch.name))
        self.outLines.append("  {}\n".format(signalBatch.desc))

        if signalBatch.context:
            self.outLines.append("{}:\n".format(g.BACKGROUND))
            self.outLines.append("  {} {}\n\n".format(g.GIVEN, self.tree_to_str(signalBatch.context)))

        for scenario in signalBatch.scenarios:
            self.outLines.append("{}: {}\n".format(g.SCENARIO, scenario.name))

            for tree in scenario.givenStatements:
                self.outLines.append("  {} {}\n".format(g.GIVEN, self.tree_to_str(tree)))
            for tree in scenario.whenStatements:
                self.outLines.append("  {} {}\n".format(g.WHEN, self.tree_to_str(tree)))
            for tree in scenario.thenStatements:
                self.outLines.append("  {} {}\n".format(g.THEN, self.tree_to_str(tree)))

    def write(self, outputFilePath: str):
       with open(outputFilePath, "w", encoding="utf-8") as out:
           out.writelines(self.outLines)

    def tree_to_str(self, tree: StatementTree):
        tp = TreeProcessor(self.language)

        # loads yaml file with templates
        tp.load_templ_dic('utils/templates_dic.yaml')
        tree.root = tp.process_tree(tree.root, TreeProcessor.Direction.SIGNAL_TO_NL)

        return self.node_to_str(tree.root)

    def node_to_str(self, node: StatementTreeNode):
        if type(node) == StatementTreeBinaryOperatorNode:
            return self.operator_to_str(node)
        elif type(node) == StatementTreeOperandNode or \
              type(node) == StatementTreeMergedNode:
            return self.operand_to_str(node)

    def operator_to_str(self, node: StatementTreeBinaryOperatorNode):
        return ("({} {} {})".format(
            self.node_to_str(node.lchild),
            node.kind.upper(),
            self.node_to_str(node.rchild))
        )

    def operand_to_str(self, node: StatementTreeOperandNode):
        return "{}".format(node.data.variableNL)