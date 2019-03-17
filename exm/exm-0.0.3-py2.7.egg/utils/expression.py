# coding=utf-8

import re


class ExpressionString:

    def __init__(self, astr):
        self.segs = list()
        matchs = re.finditer(r'\$\{(.*?)\}', astr)
        start = 0
        for match in matchs:
            expression = match.group(1)
            self.segs.append((astr[start:match.start()], False, None))
            start = match.end()
            self.segs.append((expression, True, match.group()))
        self.segs.append((astr[start:len(astr)], False, None))
        pass

    def evaluate(self, env):
        segValues = list()
        for seg, isExpr, expression in self.segs:
            if isExpr:
                segValue = self.getExpressionFromEnv(env, seg)
                segValue = str(segValue) if segValue else expression
            else:
                segValue = seg
            segValues.append(segValue)
        return "".join(segValues)

    def getExpressionFromEnv(self, env, expression):
        dt = env
        for key in expression.split("."):
            dt = dt.get(key)
            if not dt:
                return None
        return dt
        

def evaluate(env, obj):
    result = obj
    if type(obj) is dict:
        for key, value in obj.items():
            obj[key] = evaluate(env, value)
    elif type(obj) is list:
        for idx, value in enumerate(obj):
            obj[idx] = evaluate(env, value)
    else:
        if type(obj) is str:
            result = obj if obj.find(
                "${") == -1 else ExpressionString(obj).evaluate(env)
    return result
