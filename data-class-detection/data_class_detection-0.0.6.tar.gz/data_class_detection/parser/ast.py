import json

import re
from antlr4 import *
from data_class_detection.parser.Java8Lexer import Java8Lexer
from data_class_detection.parser.Java8Parser import Java8Parser


class ASTree:
    def __init__(self, name, children):
        self.name = name
        self.children = children

    def __repr__(self):
        return self.name


class ASTParser:
    def __init__(self, path):
        self.tree = self.parse(path)

    def parse(self, path):

        def getChild(ast):
            if ast.name == 'classDeclaration':
                return ast
            else:
                for child in ast.children:
                    node = getChild(child)
                    if node is not None:
                        return node
            return None

        def obj2dict(obj):
            if (isinstance(obj, ASTree)):
                return {
                    'name': obj.name,
                    'children': obj.children
                }
            else:
                return obj

        input_stream = FileStream(path, encoding='utf8')
        lexer = Java8Lexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = Java8Parser(stream)
        tree = parser.compilationUnit()
        return json.loads(json.dumps(getChild(ast=self._build_ASTree(tree, parser)), default=obj2dict))

    def _build_ASTree(self, tree, recog):
        def build(tree, recog):

            def getNodeText(t, ruleNames, recog):
                if recog is not None:
                    ruleNames = recog.ruleNames
                if ruleNames is not None:
                    if isinstance(t, RuleNode):
                        if t.getAltNumber() != 0:  # should use ATN.INVALID_ALT_NUMBER but won't compile
                            return ruleNames[t.getRuleIndex()] + ":" + str(t.getAltNumber())
                        return ruleNames[t.getRuleIndex()]
                    elif isinstance(t, ErrorNode):
                        return str(t)
                    elif isinstance(t, TerminalNode):
                        if t.symbol is not None:
                            return t.symbol.text
                # no recog for rule names
                payload = t.getPayload()
                if isinstance(payload, Token):
                    return payload.text
                return str(t.getPayload())

            ruleNames = recog.ruleNames
            name = getNodeText(tree, ruleNames, recog)
            if tree.getChildCount() == 0:
                return ASTree('[%s]' % name, [])

            children = []
            for i in range(0, tree.getChildCount()):
                child = tree.getChild(i)
                children.append(build(child, recog))

            return ASTree(name, children)

        return build(tree, recog)


def break_word(text):
    if '_' in text and text.upper() == text:
        word = text.lower().split('_')
    else:
        i = 0
        j = 0
        word = []
        while j < len(text):
            while j < len(text) and not (text[j] >= 'A' and text[j] <= 'Z'):
                j += 1
            if i == j:
                j += 1
                continue
            word.append(text[i:j].lower())
            i = j
            j += 1
        if not i == j and j < len(text):
            word.append(text[i:j])
    word = [w for w in word if len(w)>1]
    return word


def variable(text):
    if len(text) < 2:
        return False
    regex = '^[_a-zA-Z][_a-zA-Z0-9]*$'
    matched = re.match(regex, text)
    return matched is not None


def _get_node(source):
    isToken = lambda x: x.startswith('[')
    if not isToken(source['name']):
        return source['name']
    elif isToken(source['name']) and variable(source['name'][1:-1]):
        bword = break_word(source['name'][1:-1])
        if len(bword) > 0:
            return bword


def compress(source):

    isToken = lambda x: x.startswith('[')

    if 'children' in source and len(source['children']) == 1:
        if not isToken(source['name']) and not isToken(source['children'][0]['name']):
            return compress(source['children'][0])
    node = _get_node(source)
    if node is None:
        return
    ast_node = {
        'node': node,
        'children': []
    }
    if 'children' in source:
        for child in source['children']:
            ast_child = compress(child)
            if ast_child is not None:
                ast_node['children'].append(ast_child)
    return ast_node
