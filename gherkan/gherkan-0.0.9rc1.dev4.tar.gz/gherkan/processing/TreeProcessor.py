import re

import pkg_resources
import yaml
import warnings
from gherkan.containers.SignalStatementTree import SignalPhrase
from gherkan.containers.SignalStatementTreeNode import SignalStatementTreeOperatorNode, SignalStatementTreeOperandNode, \
    SignalStatementTreeNode

from enum import Enum
from pprint import pprint as pp
from gherkan.processing.Temp2NL import FillActions
from gherkan.utils import constants as c


class TreeProcessor:
    class Direction(Enum):
        SIGNAL_TO_NL = 0
        NL_TO_SIGNAL = 1

    def __init__(self, language):
        self.templ_dic = None
        self.language = language

    def translate_to_signal(self, node: SignalStatementTreeOperandNode, sp: SignalPhrase, template: dict):
        # take the initial pattern TempStr from the template
        variable = template["TempStr"][0]

        # replace all named patterns by their value
        for group, value in sp.vars.items():
            if value is not None:
                strToReplace = re.compile(r"\(\?P\<{}\>[^\)]+\)".format(group))
                variable = re.sub(strToReplace, value, variable)

        # the result should be a variable name without any whitespaces
        node.data.variable = re.sub(r'\s+', '', variable)

        # TODO agree how to fill in the value (hardcoding "1" here does not make much sense)
        node.data.value = sp.vars["value"] if "value" in sp.vars else "[empty]"


    def translate_to_nl(self, node: SignalStatementTreeOperandNode, signalPhrase: SignalPhrase):
        # call Temp2NL
        fill_action = FillActions()
        fill_action.ParseMainAction(data=signalPhrase)

        node.data.variableNL_full = signalPhrase.niceStr

    def extract_variables(self, node: SignalStatementTreeOperandNode, template: dict, match: re.match):
        # fill in fields in SignalPhrase object which will be sent to Temp2NL for further processing
        sp = SignalPhrase()
        sp.tempName = template["Name"]
        sp.tempStr = template["TempStr"][0]
        sp.tempToNL = template["EnTempToNLP"] if self.language == c.LANG_EN else template["CzTempToNLP"]
        sp.inclinations = template["Inclinations"]
        sp.language = self.language

        # TODO should not take only the first element
        type = template["Type"][0]
        node.data.kind = type

        # find all (named) groups in template patterns
        varStrGroups = re.findall(r'(?<=\<).*?(?=\>)', sp.tempStr)
        varNLGroups = re.findall(r'(?<=\<).*?(?=\>)', sp.tempToNL)

        for group in varNLGroups:
            if group in varStrGroups:
                # fill in the matched value of the named pattern
                sp.vars[group] = match[group]

            elif group == "value":
                # value is usually present in matches from NL, otherwise we use the value saved in the node
                sp.vars[group] = match[group] if group in match.groupdict() else node.value
                sp.valTypes[type] = node.value

        return sp

    def process_node(self, node: SignalStatementTreeOperandNode, dir: Direction):
        template, match = self.match_template(node, dir)

        if match is None:
            warnings.warn("No match found for phrase: " + node.data.string)
            return

        signalPhrase = self.extract_variables(node, template, match)

        if dir == TreeProcessor.Direction.SIGNAL_TO_NL:
            # make the real translation to NL using Temp2NL
            self.translate_to_nl(node, signalPhrase)
        elif dir == TreeProcessor.Direction.NL_TO_SIGNAL:
            self.translate_to_signal(node, signalPhrase, template, match)
        else:
            raise NotImplementedError("Direction {} unknown".format(dir))


    def process_tree(self, node: SignalStatementTreeNode, dir: Direction):
        if type(node) is SignalStatementTreeOperatorNode:
            self.process_tree(node.lchild, dir)
            self.process_tree(node.rchild, dir)

        elif type(node) is SignalStatementTreeOperandNode:
            self.process_node(node, dir)
        else:
            raise NotImplementedError("Unrecognized type of node: {}".format(type(node)))


    def match_template(self, node: SignalStatementTreeOperandNode, dir: Direction):
        # finds a matching template in the YAML file (works for both directions)
        template = None
        match = None

        if dir == TreeProcessor.Direction.NL_TO_SIGNAL:
            str_to_match = node.data.variableNLP
        elif dir == TreeProcessor.Direction.SIGNAL_TO_NL:
            str_to_match = node.data.variable
        else:
            raise NotImplementedError("Direction {} unknown".format(dir))

        for index, template in self.templ_dic.items():
            if dir == TreeProcessor.Direction.NL_TO_SIGNAL:
                template_str = template["TempToNLP"]
            else:
                # TODO we take only first element, we should look for all elements in the list
                template_str = template["TempStr"][0]

            expToMatch = re.compile(r"" + template_str)
            match = expToMatch.search(str_to_match)

            if match:
                break

        return template, match

    def load_templ_dic(self, file):
        # load templates to be matched
        with pkg_resources.resource_stream("gherkan", file) as stream:
            try:
                self.templ_dic = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)