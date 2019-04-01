import tatsu
import tatsu.exceptions
import abc
import typing

__all__ = ["lambdapy", "l", "assign", "get", "FORWARD_DECL"]

_lambdapy_grammar: str = r"""
start = term $ ;
term = application | abstraction | variable ;
application = "(" term { term }+ ")" ;
abstraction = "(" "\" ",".{ variable }+ "." term ")" ;
variable = /[^\\\.\(\)\s\n\tλ,=]+/ ;
"""

LAMBDA = "λ"

_lambdapy_namespace: dict = {}


def _tail(msg: str):
    print(msg)
    return msg


class _lambdapy_error(Exception):
    pass


class LambdaPyNotFound(_lambdapy_error):
    pass


class LambdaPySyntaxError(_lambdapy_error):
    pass


class LambdaPyArgumentError(_lambdapy_error):
    pass


class _lambdapy_reference:
    def __init__(self, value):
        self._value = value

    def _replace(self, *args, **kwargs):
        return self._value._replace(*args, **kwargs)

    def __str__(self):
        if self._value is None:
            return "none"
        return str(self._value)

    def __repr__(self):
        if self._value is None:
            return "\033[31mnone\033[0m"
        return repr(self._value)

    def __eq__(self, other):
        if type(self) == type(other):
            return self._value == other._value
        else:
            return self._value == other

    def __ne__(self, other):
        return not self == other

    def display(self):
        print(repr(self))


class _lambdapy_forward_decl:
    def __eq__(self, other):
        return type(self) == type(other)

    def __ne__(self, other):
        return not self == other


class _lambdapy_semantics:
    def application(self, ast):
        return _lambdapy_application.from_ast(ast)

    def abstraction(self, ast):
        return _lambdapy_statement.from_ast(ast)

    def variable(self, ast):
        return _lambdapy_variable.from_ast(ast)


_lambdapy_parser = tatsu.compile(_lambdapy_grammar, semantics=_lambdapy_semantics())


class _lambdapy_object(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def from_ast(cls, ast):
        pass

    @classmethod
    def make(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    @abc.abstractmethod
    def _replace(self, e1, e2):
        pass

    @abc.abstractmethod
    def __str__(self):
        pass

    @abc.abstractmethod
    def __repr__(self):
        pass

    @abc.abstractmethod
    def __eq__(self, other):
        pass

    def __ne__(self, other):
        return not self == other

    def display(self):
        print(repr(self))


class _lambdapy_statement(_lambdapy_object):
    __slots__ = ["_arg", "_expr"]

    @classmethod
    def from_ast(cls, ast) -> "_lambdapy_statement":
        if len(ast[2]) == 1:
            return cls.make(ast[2][0], ast[4])
        else:
            nast_arg = ast[2][1:]
            nast = (None, None, nast_arg, None, ast[4])
            return cls.make(ast[2][0], cls.from_ast(nast))

    def __init__(self, arg, expr):
        self._arg = arg
        self._expr = expr

    def _replace(self, e1, e2) -> "_lambdapy_statement":
        return _lambdapy_statement(self._arg, self._expr._replace(e1, e2))

    def beta_reduce(self, e) -> typing.Union["_lambdapy_statement", "_lambdapy_variable", "_lambdapy_application"]:
        return self._expr._replace(self._arg, e)

    def __str__(self):
        return "(λ" + str(self._arg) + "." + str(self._expr) + ")"

    def __repr__(self):
        return "(\033[35mλ\033[0m" + repr(self._arg) + "." + repr(self._expr) + ")"

    def __eq__(self, other):
        return type(self) == type(other) and self._arg == other._arg


class _lambdapy_application(_lambdapy_object):
    __slots__ = ["_e1", "_e2"]

    @classmethod
    def from_ast(cls, ast):
        if len(ast[2]) == 1:
            return cls.make(ast[1], ast[2][0])
        else:
            return cls.from_ast((None, cls.make(ast[1], ast[2][0]), ast[2][1:]))

    @classmethod
    def make(cls, e1, e2) -> typing.Union:
        if type(e1) == _lambdapy_statement:
            return e1.beta_reduce(e2)
        if type(e1) == _lambdapy_reference and type(e1._value) == _lambdapy_statement:
            return e1._value.beta_reduce(e2)
        return cls(e1, e2)

    def __init__(self, e1, e2):
        self._e1 = e1
        self._e2 = e2

    def _replace(self, e1, e2) -> "_lambdapy_application":
        return _lambdapy_application.make(self._e1._replace(e1, e2), self._e2._replace(e1, e2))

    def __str__(self):
        return "(" + str(self._e1) + " " + str(self._e2) + ")"

    def __repr__(self):
        return "(" + repr(self._e1) + " " + repr(self._e2) + ")"

    def __eq__(self, other):
        return type(self) == type(other) and self._e1 == other._e1 and self._e2 == other._e2


class _lambdapy_variable(_lambdapy_object):
    __slots__ = ["_value"]

    @classmethod
    def from_ast(cls, ast) -> typing.Union["_lambdapy_variable", _lambdapy_reference]:
        return cls.make(ast)

    @classmethod
    def make(cls, ast):
        if ast not in _lambdapy_namespace:
            return cls(ast)
        return _lambdapy_namespace[ast]

    def __init__(self, value):
        self._value = value

    def _replace(self, e1, e2):
        if e1._value == self._value:
            return e2
        return self

    def __str__(self):
        return self._value

    def __repr__(self):
        return "\033[36m" + self._value + "\033[0m"

    def __eq__(self, other):
        return type(self) == type(other) and self._value == other._value


def church_numeral(n: int) -> _lambdapy_statement:
    if type(n) != int or n < 0:
        raise LambdaPyArgumentError("n must be an integer ≥ 0")
    value = CHURCH_ZERO
    for i in range(n):
        value = _lambdapy_application.make(CHURCH_INCR, value)
    return value


def lambdapy(expr: str) -> typing.Union[
    _lambdapy_statement, _lambdapy_application, _lambdapy_variable, _lambdapy_reference]:
    try:
        return _lambdapy_parser.parse(expr.replace("λ", "\\"))
    except tatsu.exceptions.FailedParse as e:
        info = e.buf.line_info(e.pos)
        err = LambdaPySyntaxError(e.message.rstrip() + "\n" + expr + "\n" + (" " * info.col) + "^")
    raise err


def l(expr: str) -> typing.Union[_lambdapy_statement, _lambdapy_application, _lambdapy_variable, _lambdapy_reference]:
    return lambdapy(expr)


FORWARD_DECL = _lambdapy_forward_decl()

CHURCH_ZERO = lambdapy(r"(λf,x.x)")

CHURCH_INCR = lambdapy(r"(λn,f,x.(f (n f x)))")


def assign(name: str, value: typing.Union[
    _lambdapy_statement, _lambdapy_application, _lambdapy_variable, _lambdapy_forward_decl] = FORWARD_DECL) -> typing.NoReturn:
    if FORWARD_DECL == value:
        val = _lambdapy_reference(None)
    else:
        val = _lambdapy_reference(value)
    if name in _lambdapy_namespace:
        _lambdapy_namespace[name]._value = val
    else:
        _lambdapy_namespace[name] = val


def get(name: str) -> typing.Union[_lambdapy_reference]:
    try:
        return _lambdapy_namespace[name]
    except KeyError:
        raise LambdaPyNotFound("undefined variable: " + name)