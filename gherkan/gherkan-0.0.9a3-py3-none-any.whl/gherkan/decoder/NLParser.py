import json
import re
import copy

from gherkan.containers.SignalStatementTreeNode import SignalStatementTreeOperandNode, \
    SignalStatementTreeOperatorNode
from gherkan.containers.SignalStatementTree import SignalStatementTree
from gherkan.containers.signal_conditional_statement import SignalCondition, NLCondition
from gherkan.decoder.Parser import Parser

class NLParser(Parser):
    def __init__(self):
        super().__init__()

    # TODO rewrite to something more readable
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

        dataStack = re.split(r'( AND | OR | A | NEBO )', statement)  # brackets to save also the separator value
        dataStackFull = copy.deepcopy(dataStack)  # saves NL statements in original version not with program numbers

        with open(
                self.ROBOT_PROGRAMS_EN) as f:  # loads json with program numbers and descriptions which were extracted from NL input
            programs = json.load(f)

        for id, ot in enumerate(dataStack):
            # checks if the statement is in robot actions. If yes, then it
            # detects robot programs in json file to exchange the actions for program numbers
            re_robotPrograms = re.compile(r"\brobot\s(?P<name>[a-z]\d{1})\s+(?P<text>.*)")
            cond = re_robotPrograms.search(ot)
            if cond:
                robProg = cond.group("text")
                robName = cond.group("name")
                for phrase in programs[robName]:
                    if programs[robName][phrase] in robProg:
                        dataStack[id] = "robot" + robName.upper() + " program number is " + phrase

        for id, ot in enumerate(dataStack):
            if ot in [' AND ', ' OR ', ' A ', ' NEBO ']:
                ot = ot.replace(' ', '')
                operatorStack.append(ot)
            else:
                cond = NLCondition(dataStackFull[id], dataStackFull[id], ot,
                                   ot)  # (strFullEn, strFullCs, strEng, strCZ)
                outputStack.append(cond)

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