# import re
# import numpy as np
# import pkg_resources
# import yaml
# import inspect
#
# import gherkan.utils.constants as c
#
# class SignalCondition():
#     def __init__(self, string, kind, negated=False):
#         self.kind = kind
#         self.string = string
#         self.variable = None
#         self.value = None
#         self.variableTr = None
#         self.templateID = None
#         self.variableNLP = None
#         self.variableNLPCZ = None
#         self.variableNL_full = None
#         self.variableNL_full_cs = None
#
#         if self.kind == c.EQUALITY or kind == c.INEQUALITY:
#             match = re.search(r'(?P<variable>\w+)\s*[=!]+\s*(?P<value>\w+)', self.string)
#             if negated:
#                 if self.kind == c.EQUALITY:
#                     self.kind = c.INEQUALITY
#                 else:
#                     self.kind = c.EQUALITY
#         elif self.kind == c.BOOL:
#             match = re.search(r'(?P<variable>\w+)', self.string)
#             self.value = 1 if not negated else 0
#         elif self.kind == c.EDGE:
#             match = re.search(r'edge\((?P<variable>\w+)\s*,\s*(?P<value>\w+)', self.string)
#         elif self.kind == c.FORCE:
#             match = re.search(r'force\((?P<variable>\w+)\s*,\s*(?P<value>\w+)', self.string)
#         elif self.kind == c.UNFORCE:
#             match = re.search(r'unforce\((?P<variable>\w+)', self.string)
#         else:
#             raise Exception("Error while parsing a signal condition (whaaat?). Related string: '{}'. Unexpected condition kind: '{}'.".format(self.string, self.kind))
#         if match:
#             self.variable = match.group("variable")
#             if "value" in match.groupdict().keys():
#                 self.value = match.group("value")
#         else:
#             raise Exception("Error while parsing a signal condition. Phrase matching failed!\nRelated string: '{}'\nCondition kind: '{}'".format(self.string, self.kind))
#
#
# class NLCondition():
#     def __init__(self, strFullEn = None, strFullCs = None, strEng = None, strCZ = None):
#         self.kind = None
#         self.string = strFullEn
#         self.variable = None
#         self.value = None
#         self.variableTr = None
#         self.templateID = None
#         self.variableNL_full = strFullEn
#         self.variableNL_full_cs = strFullCs
#         self.variableNLP = strEng
#         self.variableNLPCZ = strCZ
#
#
# # TODO defined elsewhere, remove
# # class SignalStatementTreeNode():
# #
# #     def __init__(self, kind=None, data=None):
# #         self.__kind = kind
# #         self.__data = data
# #         self.__parent = None
# #
# #     def setParent(self, parent):
# #         self.__parent = parent
# #
# #     @property
# #     def kind(self):
# #         return self.__kind
# #
# #     @property
# #     def parent(self):
# #         return self.__parent
# #
# #     @property
# #     def data(self):
# #         return self.__data
# #
# #     def getIncompleteParent(self):
# #         raise NotImplementedError()
# #
# #
# #
# # class SignalStatementTreeOperatorNode(SignalStatementTreeNode):
# #     AND = 'and'
# #     OR = 'or'
# #
# #     def __init__(self, kind):
# #         super().__init__(kind.lower())
# #         self.__lchild = None  # type: SignalStatementTreeNode
# #         self.__rchild = None  # type: SignalStatementTreeNode
# #         self.templateID = None
# #         self.variableNLP = None
# #         self.variableNL_full = None
# #         self.variableNLPCZ = None
# #         self.variableNL_full_cs = None
# #
# #     @property
# #     def lchild(self):
# #         return self.__lchild
# #
# #     @property
# #     def rchild(self):
# #         return self.__rchild
# #
# #     @property
# #     def children(self):
# #         return [self.lchild, self.rchild]
# #
# #     @property
# #     def full(self):
# #         return (self.lchild is not None) and (self.rchild is not None)
# #
# #     def getIncompleteParent(self):
# #         if self.full:
# #             if self.parent:
# #                 return self.parent.getIncompleteParent()
# #             else:
# #                 return None
# #         else:
# #             return self
# #
# #     def attachChild(self, child: SignalStatementTreeNode):
# #         """
# #         Returns True if the node is "full" (i.e. both children are assigned)
# #         """
# #         child.setParent(self)
# #         if self.lchild:
# #             self.__rchild = child
# #             return True
# #         else:
# #             self.__lchild = child
# #             return False
# #
# #     def __str__(self):
# #         return 'Operator(type: {})'.format(self.kind.upper())
#
#
# # class SignalStatementTreeOperandNode(SignalStatementTreeNode):
# #
# #     def __init__(self, data: SignalCondition):
# #         super().__init__(data.kind, data)
# #
# #     def getIncompleteParent(self):
# #         self.parent.getIncompleteParent()
# #
# #     def __str__(self):
# #         return 'Operand(type: {}, variable: {}, value: {}, variableNLP: {}, variableNL_full: {})'.format(self.kind.upper() if self.kind else 'None', self.data.variable, self.data.value, self.data.variableNLP, self.data.variableNL_full)
# #
# #     @property
# #     def variable(self):
# #         return self.data.variable
# #
# #     @property
# #     def kind(self):
# #         return self.data.kind
# #
# #     @property
# #     def variableNLP(self):
# #         return self.data.variableNLP
# #
# #     @property
# #     def variableNL_full(self):
# #         return self.data.variableNL_full
# #
# #     @property
# #     def value(self):
# #         return self.data.value
# #
# #
# # class SignalStatementTree():
# #     dash, line, left, right = '\u2500', '\u2502', '\u251c\u2500\u2500 ', '\u2514\u2500\u2500 '
# #
# #     def __init__(self, root: SignalStatementTreeNode, string: str):
# #         self.__root = root
# #         self.__string = string
# #
# #     @property
# #     def root(self):
# #         return self.__root
# #
# #     @property
# #     def string(self):
# #         return self.__string
# #
# #     def __printNode(self, node: SignalStatementTreeNode, leftChild, levelsOpened):
# #         string = ''.join([SignalStatementTree.line + "\t" if lo else "\t" for lo in levelsOpened[:-1]])
# #         if leftChild:
# #             if node:
# #                 string += SignalStatementTree.left + str(str(node) if bool(node) else "ERROR!!!") + '\n'
# #         else:
# #             if node:
# #                 string += SignalStatementTree.right + str(str(node) if bool(node) else "ERROR!!!") + '\n'
# #
# #         if type(node) is SignalStatementTreeOperatorNode:
# #             string += self.__printNode(node.lchild, True, levelsOpened + [True])
# #             string += self.__printNode(node.rchild, False, levelsOpened + [False])
# #         return string
# #
# #     def __str__(self):
# #         levelsOpened = [False]
# #
# #         node = self.root
# #         string = str(node) + '\n'
# #         if type(node) is SignalStatementTreeOperatorNode:
# #             string += self.__printNode(node.lchild, True, levelsOpened + [True])
# #             string += self.__printNode(node.rchild, False, levelsOpened + [False])
# #         return string
# #
#
# class EvalFunction():
#     """
#     Place holder for functions to be evaluated on the SignalStatementTree.
#     Contains additional functionality to enable creation of more complex templates.
#
#     Attributes
#     ----------
#     func : Function
#         The function to be evaluated on SignalStatementTreeNode objects (altough the implementation does not enforce any class)
#
#     succeeded : bool
#         True if the function was evaluated to True sufficient number of times
#
#     successes : int
#         The number of times when the function was evaluated successfully
#     """
#
#     def __init__(self, func, minSuccesses=1, maxSuccesses=None, failFast=False):
#         """
#         Parameters
#         ----------
#         func : Function
#             The function to be evaluated on SignalStatementTreeNode objects
#
#         minSuccesses : int
#             The minimum number of times the function needs to evaluate to True
#             to declare overall success. Use this in combination with maxSuccesses
#             to have a range of possible nodes that comply to the requirements
#             enforced by the function.
#
#         maxSuccesses : int
#             The maximum number of cases the function can be evaluated to True.
#             After the maxSuccesses has been reached, all following evaluations
#             will fail, even if they would succeed otherwise. Set this value
#             to a very large number to achieve unlimited number of successful
#             evaluations.
#
#         failFast : bool
#             If True, the first case when the function is evaluated to False
#             will result in complete failure of this condition. I.e. all future
#             evaluations will only fail and overall success will be False
#             no matter what. Use this to enforce a condition on all tested nodes.
#             failFast will also cause permanent failure if number of maxSuccesses
#             is exceeded. This can be used to limit the number of nodes in a subtree.
#             E.g., EvalFunction(lambda x: True, maxSuccesses=5, failFast=True)
#             Will generate a function that will make sure that there are at most 5
#             nodes in the subtree.
#         """
#         self.__func = func
#         self.__succeeded = None
#         self.__successes = 0
#         self.__minSuccesses = minSuccesses
#         self.__failFast = failFast
#         self.__valid = True
#         if self.__failFast:
#             self.__maxSuccesses = maxSuccesses if maxSuccesses else np.iinfo(np.int).max
#         else:
#             self.__maxSuccesses = maxSuccesses if maxSuccesses else minSuccesses
#
#     def invalidate(self):
#         self.__valid = False
#
#     def __bool__(self):
#         if self.__succeeded is None:
#             if self.successes >= self.minSuccesses:
#                 self.__succeeded = True
#                 return True
#             else:
#                 return False
#         elif self.__succeeded is True:
#             return True
#         elif self.__succeeded is False:
#             return False
#
#     def __call__(self, value):
#         """Calls the associated function and evaluates the result depending on other conditions as well.
#         If maxSuccesses has been exceeded, the call will fail no matter the actual result
#         (the function won't even be evaluated). It the number of successes (evaluations/calls resulting in True)
#         is smaller than maxSuccesses, the function, associated with this placeholder, is called with the provided value.
#         If the call returns True, number of successes is increased. The success, i.e. the result of the call is returned.
#         If failFast is set to True, any call that will result in return value equal to False will also fail the success
#         of the entire placeholder (EvalFunction instance)
#
#         Parameters
#         ----------
#         value : any
#             Function parameters
#
#         Returns
#         -------
#         bool
#             The success of the call (depending on other parameters)
#         """
#         if self.__succeeded is not None and not self.__succeeded:
#             return False
#         if self.successes >= self.maxSuccesses:
#             if self.failFast and self.func(value):
#                 self.__succeeded = False
#             return False
#         success = self.func(value)
#         if success:
#             self.__successes += 1
#         elif self.failFast:
#             self.__succeeded = False
#         return success
#
#     @property
#     def successes(self):
#         return self.__successes
#
#     @property
#     def succeeded(self):
#         return bool(self)
#
#     @property
#     def func(self):
#         return self.__func
#
#     @property
#     def minSuccesses(self):
#         return self.__minSuccesses
#
#     @property
#     def maxSuccesses(self):
#         return self.__maxSuccesses
#
#     @property
#     def valid(self):
#         return self.__valid
#
#     @property
#     def failFast(self):
#         return self.__failFast
#
#     def __repr__(self):
#         sig = inspect.signature(self.func)
#
#         def displayParam(p, d):
#             return "\t\t\t{}:\n{}".format(p, "\n".join(["\t\t\t\t{}".format(item) for item in d])) if type(d) is list else "\t\t\t{}: {}".format(p, d)
#
#         return "\n".join([
#             ">>> EvalFunction object <<<",
#             "\tNumber of successes = {}".format(self.successes),
#             "\tMinimum number of successes = {}".format(self.minSuccesses),
#             "\tMaximum number of successes = {}".format(self.maxSuccesses),
#             "\tSucceeded = {}".format(self.succeeded),
#             "\tAssociated function:",
#             "\t\tSignature: {}".format(str(sig)),
#             "\t\tParameters: ",
#             "\n".join(["\t\t\t" + param if sig.parameters[param].default is inspect._empty else displayParam(param, sig.parameters[param].default) for param in sig.parameters]),
#             "\t\tSource code: \n" + inspect.getsource(self.func).strip()
#         ])
#
#
# class EvalFunctionList():
#
#         def __init__(self, functionList):
#             """
#             Helper function to generate so called structure list from a list of functions.
#             Changed to generate a list of EvalFunction objects
#             For example:
#             [lambda x: x + 2, lambda x: x * 3] -> [EvalFunction(lambda x: x + 2), EvalFunction(lambda x: x * 3)]
#             """
#             self.evalList = []
#             for item in functionList:
#                 if callable(item):  # just the function; default arguments will be used
#                     evalList.append(EvalFunction(item))
#                 elif type(item) is tuple:  # a list of positional arguments
#                     evalList.append((EvalFunction(*item)))
#                 elif type(item) is dict:  # dictionary with kwargs
#                     evalList.append((EvalFunction(**item)))
#                 else:
#                     raise Exception("Unknown object type encountered while constructing structure list.")
#
# # TODO make iterable and validable
# # TODO incorporate additional methods into SignalStatementTree
#
# # class SignalTemplateTree(SignalStatementTree):
# #
# #     def __init__(self, signalTree: SignalStatementTree):
# #         super().__init__(signalTree.root, signalTree.string)
# #
# #     def __isTwig(self, node: SignalStatementTreeNode):
# #         """
# #         Checks if a node is an operator node but has only leaves (i.e. no consecutive operator nodes == no further branching)
# #         """
# #         if type(node) is SignalStatementTreeOperatorNode:
# #             return (type(node.lchild) is SignalStatementTreeOperandNode) and (type(node.rchild) is SignalStatementTreeOperandNode)
# #         else:
# #             return False
# #
# #     def __recursiveBoolEval(self, node: SignalStatementTreeNode, func):
# #         """
# #         Recursively attempts to evaluate the function on all subsequent nodes.
# #         Returns True if all evaluations were successful. That is, if the function
# #         is holds true for all nodes in the subtree.
# #         """
# #         result = func(node)
# #         if type(node) is SignalStatementTreeOperandNode:
# #             return result
# #         elif type(node) is SignalStatementTreeOperatorNode:
# #             return result and self.__recursiveBoolEval(node.lchild, func) and self.__recursiveBoolEval(node.rchild, func)
# #         else:
# #             # Unknown node type
# #             return False
# #
# #     def __recursiveStructureEval(self, node: SignalStatementTreeNode, structureList: list):
# #         """
# #         Recursively enters nodes and attempts to evalute functions in the structureList list.
# #         If one of the evaluations is successful it then attempts to continue with evaluations
# #         on the node's children.
# #
# #         Old version:
# #         "However, the successfully evaluated function is omitted
# #         from further evaluations. That is, each function must succeed exactly once!"
# #
# #         Newer version:
# #         "The number of successful evaluations depends on the specific conditions
# #         imposed by the EvalFunction object"
# #
# #         Functions are evaluated in a greedy manner. The order of the functions
# #         should therefore be considered - e.g., if some function A can succeed on more nodes
# #         than other function B in the list (i.e., domain of B(x) = True is a subset of A(x) = True),
# #         B should precede A in the list. Otherwise function A might take node that should
# #         normally be captured by B.
# #         """
# #         if len(structureList) == 0:  # either empty list has been provided or some node emptied it (see !success condition below)
# #             return False
# #         success = False
# #         allTrue = True
# #         for i, evalFunc in enumerate(structureList):
# #             if not evalFunc.valid:
# #                 # TODO how to handle allTrue?????
# #                 continue
# #             # Run the eval function on the node.
# #             # The boolean value of the function object is assigned to the allTrue variable to check if the structure is completed
# #             # the internal success of the function is handled by the EvalFunction object
# #             if not success:  # if no function succeeded so far
# #                 # call the function with the current node as a parameter
# #                 success = evalFunc(node)  # if the call returned True, i.e. the node comforms to the condition imposed by the function
# #                 # capture the first successful evaluation and do not call any other function
# #                 # the list has to be iterated through though to check if all function succeeded already
# #             allTrue &= bool(evalFunc)
# #             if success and not allTrue:
# #                 break
# #         if allTrue:  # structureList has been completed
# #             return True
# #         if success:
# #             if type(node) is SignalStatementTreeOperatorNode:
# #                 # call function on both children
# #                 self.__recursiveStructureEval(node.lchild, structureList)
# #                 self.__recursiveStructureEval(node.rchild, structureList)
# #                 if len(structureList) > 0:  # if the list hasn't been emptied yet - the structure check did not fail so far
# #                     return all([bool(e) for e in structureList])  # return the current completion status of the structure check
# #             return False
# #         else:
# #             # if none of the functions in the list succeeded (i.e. the node is not part of the structure), then the structure check failed
# #             # that is, this was not the structure we were looking for...
# #             for evalFunc in structureList:
# #                 evalFunc.invalidate()
# #             return False
# #
# #     def __recursiveSubTreeSearch(self, node: SignalStatementTreeNode, func):
# #         """
# #         Returns all subtrees (returns their respective roots in a list, to be more exact),
# #         for which the function evalutes to True.
# #
# #         Parameters
# #         ----------
# #         node : SignalStatementTreeNode
# #             A node from the tree on which the function should be evaluted
# #
# #         func: Function
# #             Function to be evaluated
# #
# #         Returns
# #         -------
# #         list OR bool:
# #             List of roots of subtrees for which the function was evaluted to True.
# #             Returns just boolean True if this node evaluted to True. Otherwise,
# #             if this node evaluted to False but its child evaluted to True,
# #             a list containing this child will be returned.
# #         """
# #         if func(node):
# #             return node
# #         else:
# #             if type(node) is not SignalStatementTreeOperatorNode:
# #                 return False
# #             else:
# #                 rootList = []
# #                 # Evaluate the function on children and iterate over the results
# #                 for res in [self.__recursiveSubTreeSearch(node.lchild, func), self.__recursiveSubTreeSearch(node.rchild, func)]:
# #                     if not res:
# #                         continue
# #                     if type(res) is list:
# #                         rootList += res
# #                     elif type(res) is SignalStatementTreeNode:
# #                         rootList += [res]
# #
# #                 return rootList
# #
# #     def __genNextTemplate(self):
# #         """
# #         Generates function that should search for templates in the tree.
# #
# #         Raises:
# #             Exception -- Raises an exception if the ID of the requested template
# #             does not exist. That is, function for the template is not specified, yet.
# #         """
# #         with pkg_resources.resource_stream("gherkan", '/'.join(["containers", "templates_dic.yaml"])) as f:
# #             templateDict = yaml.load(f)
# #
# #         for templateID, templateSignature in templateDict.items():
# #             if "SignalTemplate" in templateSignature:  # find signal template that has the property called "SignalTemplate"
# #                 signalTemplateSignature = templateSignature["SignalTemplate"]
# #                 template = None
# #                 # find what kind of template it has (currently only structure is supported)
# #                 if type(signalTemplateSignature) is list or "structure" in signalTemplateSignature:
# #                     if type(signalTemplateSignature) is list:
# #                         templateStructure = signalTemplateSignature
# #                     elif type(signalTemplateSignature) is dict:
# #                         templateStructure = signalTemplateSignature["structure"]
# #                     structureList = []
# #                     for item in templateStructure:
# #                         if type(item) is str:
# #                             structureList.append(lambda nd, ndkind=item: type(nd) is SignalStatementTreeOperatorNode and nd.kind == ndkind)
# #                         elif type(item) is dict:
# #                             lamlist = []
# #                             kind, paramdict = item.popitem()
# #                             for key, value in paramdict.items():
# #                                 lamlist.append(lambda nd, var=key, val=value:  val.lower() in getattr(nd.data, var).lower())
# #                             structureList.append(lambda nd, ndkind=kind, paramCheckList=lamlist: type(nd) is SignalStatementTreeOperandNode and nd.kind == ndkind and all([check(nd) for check in paramCheckList]))
# #                         else:
# #                             raise Exception("Unknown type in signalTemplateSignature.\n{}".format(signalTemplateSignature))
# #
# #                     def template(node: SignalStatementTreeNode, structure=self.__genStructureFromFunctionList(structureList)):
# #                         def searchFunction(node: SignalStatementTreeNode):
# #                             return self.__recursiveStructureEval(node, structure)
# #                         return self.__recursiveSubTreeSearch(node, searchFunction)
# #
# #                 elif "condition" in signalTemplateSignature:
# #                     pass
# #                 elif "script" in signalTemplateSignature:
# #                     pass
# #
# #                 yield((templateID, template))
# #
# #     def parseTemplates(self):
# #         for templateID, template in self.__genNextTemplate():
# #             if not template:
# #                 raise Exception("Error while generating template from SignalTemplateTree!")
# #             tempResult = template(self.root)
# #             if tempResult:
# #                 print(tempResult)
# #                 if type(tempResult) is not list:
# #                     tempList = [tempResult]
# #                 for subtreeRoot in tempList:
# #                     subtreeRoot.templateID = templateID
#
