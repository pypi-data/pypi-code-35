from CalcModel import calcmethods


def run(a, b, op_name=""):
    op = getattr(calcmethods, "my_" + op_name, "my_add")
    return op(a, b)

