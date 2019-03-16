# This module is derived from astunparse: https://github.com/simonpercivall/astunparse
##########################################################################
### astunparse LICENSES
# LICENSE
# ==================
#
# Copyright (c) 2014, Simon Percivall
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
# * Neither the name of AST Unparser nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#
# PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2
# --------------------------------------------
#
# 1. This LICENSE AGREEMENT is between the Python Software Foundation
# ("PSF"), and the Individual or Organization ("Licensee") accessing and
# otherwise using this software ("Python") in source or binary form and
# its associated documentation.
#
# 2. Subject to the terms and conditions of this License Agreement, PSF hereby
# grants Licensee a nonexclusive, royalty-free, world-wide license to reproduce,
# analyze, test, perform and/or display publicly, prepare derivative works,
# distribute, and otherwise use Python alone or in any derivative version,
# provided, however, that PSF's License Agreement and PSF's notice of copyright,
# i.e., "Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
# 2011, 2012, 2013, 2014 Python Software Foundation; All Rights Reserved" are retained
# in Python alone or in any derivative version prepared by Licensee.
#
# 3. In the event Licensee prepares a derivative work that is based on
# or incorporates Python or any part thereof, and wants to make
# the derivative work available to others as provided herein, then
# Licensee hereby agrees to include in any such work a brief summary of
# the changes made to Python.
#
# 4. PSF is making Python available to Licensee on an "AS IS"
# basis.  PSF MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR
# IMPLIED.  BY WAY OF EXAMPLE, BUT NOT LIMITATION, PSF MAKES NO AND
# DISCLAIMS ANY REPRESENTATION OR WARRANTY OF MERCHANTABILITY OR FITNESS
# FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF PYTHON WILL NOT
# INFRINGE ANY THIRD PARTY RIGHTS.
#
# 5. PSF SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF PYTHON
# FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS AS
# A RESULT OF MODIFYING, DISTRIBUTING, OR OTHERWISE USING PYTHON,
# OR ANY DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.
#
# 6. This License Agreement will automatically terminate upon a material
# breach of its terms and conditions.
#
# 7. Nothing in this License Agreement shall be deemed to create any
# relationship of agency, partnership, or joint venture between PSF and
# Licensee.  This License Agreement does not grant permission to use PSF
# trademarks or trade name in a trademark sense to endorse or promote
# products or services of Licensee, or any third party.
#
# 8. By copying, installing or otherwise using Python, Licensee
# agrees to be bound by the terms and conditions of this License
# Agreement.
##########################################################################
### END OF astunparse LICENSES

from __future__ import print_function, unicode_literals
import inspect
import six
import sys
import ast
import os
import tokenize
from six import StringIO

# Large float and imaginary literals get turned into infinities in the AST.
# We unparse those infinities to INFSTR.
INFSTR = "1e" + repr(sys.float_info.max_10_exp + 1)

_py2c_nameconst = {True: "true", False: "false", None: "nullptr"}

_py2c_reserved = {"True": "true", "False": "false", "None": "nullptr"}


def interleave(inter, f, seq):
    """Call f on each item in seq, calling inter() in between.
    """
    seq = iter(seq)
    try:
        f(next(seq))
    except StopIteration:
        pass
    else:
        for x in seq:
            inter()
            f(x)


class LocalScheme(object):
    def is_defined(self, local_name, current_depth):
        raise NotImplementedError('Abstract class')

    def define(self, local_name, lineno, depth):
        raise NotImplementedError('Abstract class')

    def clear_scope(self, from_indentation):
        raise NotImplementedError('Abstract class')


class CPPLocals(LocalScheme):
    def __init__(self):
        # Maps local name to a 2-tuple of line number and scope (measured in indentation)
        self.locals = {}

    def is_defined(self, local_name, current_depth):
        return local_name in self.locals

    def define(self, local_name, lineno, depth):
        self.locals[local_name] = (lineno, depth)

    def clear_scope(self, from_indentation):
        """Clears all locals defined in indentation 'from_indentation' and deeper"""
        toremove = set()
        for local_name, (lineno, depth) in self.locals.items():
            if depth >= from_indentation:
                toremove.add(local_name)

        for var in toremove:
            del self.locals[var]


# Python scheme: All global variables can be read, but not written to (unless defined as "global")
class PythonLocals(LocalScheme):
    def __init__(self):
        # Maps local name to a 2-tuple of line number and scope (measured in indentation)
        self.locals = {}

    def is_defined(self, local_name, current_depth):
        return local_name in self.locals and self.locals[local_name][1] == current_depth

    def define(self, local_name, lineno, depth):
        self.locals[local_name] = (lineno, depth)

    def clear_scope(self, from_indentation):
        """Clears all locals defined in indentation 'from_indentation' and deeper"""
        toremove = set()
        for local_name, (lineno, depth) in self.locals.items():
            if depth >= from_indentation:
                toremove.add(local_name)
        for var in toremove:
            del self.locals[var]


class CPPUnparser:
    """Methods in this class recursively traverse an AST and
    output C++ source code for the abstract syntax; original formatting
    is disregarded. """

    def __init__(self,
                 tree,
                 depth,
                 locals,
                 file=sys.stdout,
                 indent_output=True,
                 expr_semicolon=True,
                 indent_offset=0):

        self.f = file
        self.future_imports = []
        self._indent = depth
        self.indent_output = indent_output
        self.indent_offset = indent_offset
        self.expr_semicolon = expr_semicolon
        if not isinstance(locals, LocalScheme):
            raise TypeError('Locals must be a LocalScheme object')
        self.locals = locals
        self.firstfill = True

        self.dispatch(tree)
        print("", file=self.f)
        self.f.flush()

    def fill(self, text=""):
        """Indent a piece of text, according to the current indentation level"""
        if self.firstfill:
            if self.indent_output:
                self.f.write("    " * (self._indent + self.indent_offset) +
                             text)
            else:
                self.f.write(text)
            self.firstfill = False
        else:
            if self.indent_output:
                self.f.write("\n" + "    " *
                             (self._indent + self.indent_offset) + text)
            else:
                self.f.write("\n" + text)

    def write(self, text):
        """Append a piece of text to the current line."""
        self.f.write(six.text_type(text))

    def enter(self):
        """Print '{', and increase the indentation."""
        self.write(" {")
        self._indent += 1

    def leave(self):
        """Decrease the indentation and print '}'."""
        self._indent -= 1
        self.fill()
        self.write("}")
        # Clear locals defined inside scope
        self.locals.clear_scope(self._indent + 1)

    def dispatch(self, tree):
        """Dispatcher function, dispatching tree type T to method _T."""
        try:
            tree = iter(tree)
            for t in tree:
                self.dispatch(t)
        except TypeError:
            meth = getattr(self, "_" + tree.__class__.__name__)
            meth(tree)

    ############### Unparsing methods ######################
    # There should be one method per concrete grammar type #
    # Constructors should be grouped by sum type. Ideally, #
    # this would follow the order in the grammar, but      #
    # currently doesn't.                                   #
    ########################################################

    def _Module(self, tree):
        for stmt in tree.body:
            self.dispatch(stmt)

    def _Interactive(self, tree):
        for stmt in tree.body:
            self.dispatch(stmt)

    def _Expression(self, tree):
        self.dispatch(tree.body)

    # stmt
    def _Expr(self, tree):
        self.fill()
        self.dispatch(tree.value)
        if self.expr_semicolon:
            self.write(';')

    def _Import(self, t):
        raise SyntaxError('Invalid C++')

    def _ImportFrom(self, t):
        raise SyntaxError('Invalid C++')

    def dispatch_lhs_tuple(self, targets):
        # Decide whether to use the C++17 syntax for undefined variables or std::tie for defined variables
        if all(
                self.locals.is_defined(target.id, self._indent)
                for target in targets):
            defined = True
        elif any(
                self.locals.is_defined(target.id, self._indent)
                for target in targets):
            raise SyntaxError(
                'Invalid C++ (some variables in tuple were already defined)')
        else:
            defined = False

        if not defined:  # C++17 syntax: auto [a,b,...,z] = ...
            self.write("auto [")
        else:  # C++14 syntax: std::tie(a,b,...,z) = ...
            self.write("std::tie(")

        first = True
        for target in targets:
            if not first:
                self.write(', ')
            self.locals.define(target.id, target.lineno, self._indent)
            self.dispatch(target)
            first = False

        if not defined:
            self.write("]")
        else:
            self.write(")")

    def _Assign(self, t):
        self.fill()

        # Handle the case of a tuple output
        if len(t.targets) > 1:
            self.dispatch_lhs_tuple(t.targets)
        else:
            target = t.targets[0]
            if isinstance(target, ast.Tuple):
                if len(target.elts) > 1:
                    self.dispatch_lhs_tuple(target.elts)
                target = target.elts[0]

            if not isinstance(target,
                              ast.Subscript) and not self.locals.is_defined(
                                  target.id, self._indent):
                self.locals.define(target.id, t.lineno, self._indent)
                self.write('auto ')
            self.dispatch(target)

        self.write(" = ")
        self.dispatch(t.value)
        self.write(';')

    def _AugAssign(self, t):
        self.fill()
        self.dispatch(t.target)
        # Operations that require a function call
        if t.op.__class__.__name__ in self.funcops:
            separator, func = self.funcops[t.op.__class__.__name__]
            self.write(" = " + func + "(")
            self.dispatch(t.target)
            self.write(separator + " ")
            self.dispatch(t.value)
            self.write(")")
        else:
            self.write(" " + self.binop[t.op.__class__.__name__] + "= ")
            self.dispatch(t.value)
        self.write(';')

    def _AnnAssign(self, t):
        self.fill()

        if isinstance(t.target, ast.Tuple):
            if len(t.target.elts) > 1:
                self.dispatch_lhs_tuple(t.target.elts)
            else:
                target = target.elts[0]
        else:
            target = t.target

        # Assignment of the form x: int = 0 is converted to int x = (int)0;
        if not self.locals.is_defined(target.id, self._indent):
            self.locals.define(target.id, t.lineno, self._indent)
            self.dispatch(t.annotation)
            self.write(' ')
        if not t.simple:
            self.write("(")
        self.dispatch(t.target)
        if not t.simple:
            self.write(")")
        if t.value:
            self.write(" = (")
            self.dispatch(t.annotation)
            self.write(")")
            self.dispatch(t.value)
        self.write(';')

    def _Return(self, t):
        self.fill("return")
        if t.value:
            self.write(" ")
            self.dispatch(t.value)
        self.write(';')

    def _Pass(self, t):
        raise SyntaxError('Invalid C++')

    def _Break(self, t):
        self.fill("break;")

    def _Continue(self, t):
        self.fill("continue;")

    def _Delete(self, t):
        raise SyntaxError('Invalid C++')

    def _Assert(self, t):
        self.fill("assert(")
        self.dispatch(t.test)
        if t.msg:
            self.write(", ")
            self.dispatch(t.msg)
        self.write(");")

    def _Exec(self, t):
        raise SyntaxError('Invalid C++')

    def _Print(self, t):
        do_comma = False
        if t.dest:
            self.fill("fprintf(")
            self.dispatch(t.dest)
            do_comma = True
        else:
            self.fill("printf(")

        for e in t.values:
            if do_comma: self.write(", ")
            else: do_comma = True
            self.dispatch(e)
        if not t.nl:
            self.write(",")

        self.write(');')

    def _Global(self, t):
        raise SyntaxError('Invalid C++')

    def _Nonlocal(self, t):
        raise SyntaxError('Invalid C++')

    def _Yield(self, t):
        raise SyntaxError('Invalid C++')

    def _YieldFrom(self, t):
        raise SyntaxError('Invalid C++')

    def _Raise(self, t):
        self.fill("throw")
        if six.PY3:
            if not t.exc:
                assert not t.cause
                return
            self.write(" ")
            self.dispatch(t.exc)
            if t.cause:
                raise SyntaxError('Invalid C++')
        else:
            self.write(" ")
            if t.type:
                self.dispatch(t.type)
            if t.inst:
                self.write(", ")
                self.dispatch(t.inst)
            if t.tback:
                self.write(", ")
                self.dispatch(t.tback)
        self.write(';')

    def _Try(self, t):
        self.fill("try")
        self.enter()
        self.dispatch(t.body)
        self.leave()
        for ex in t.handlers:
            self.dispatch(ex)
        if t.orelse:
            raise SyntaxError('Invalid C++')
        if t.finalbody:
            self.fill("finally")
            self.enter()
            self.dispatch(t.finalbody)
            self.leave()

    def _TryExcept(self, t):
        self.fill("try")
        self.enter()
        self.dispatch(t.body)
        self.leave()

        for ex in t.handlers:
            self.dispatch(ex)
        if t.orelse:
            raise SyntaxError('Invalid C++')

    def _TryFinally(self, t):
        if len(t.body) == 1 and isinstance(t.body[0], ast.TryExcept):
            # try-except-finally
            self.dispatch(t.body)
        else:
            self.fill("try")
            self.enter()
            self.dispatch(t.body)
            self.leave()

        self.fill("finally")
        self.enter()
        self.dispatch(t.finalbody)
        self.leave()

    def _ExceptHandler(self, t):
        self.fill("catch (")
        if t.type:
            self.dispatch(t.type)
        if t.name:
            if six.PY3:
                self.write(t.name)
            else:
                self.dispatch(t.name)
        self.write(')')
        self.enter()
        self.dispatch(t.body)
        self.leave()

    def _ClassDef(self, t):
        raise NotImplementedError('Classes are unsupported')

        # Original class definition from astunparse
        #self.write("\n")
        #for deco in t.decorator_list:
        #    self.fill("@")
        #    self.dispatch(deco)
        #self.fill("class "+t.name)
        #if six.PY3:
        #    self.write("(")
        #    comma = False
        #    for e in t.bases:
        #        if comma: self.write(", ")
        #        else: comma = True
        #        self.dispatch(e)
        #    for e in t.keywords:
        #        if comma: self.write(", ")
        #        else: comma = True
        #        self.dispatch(e)
        #    if sys.version_info[:2] < (3, 5):
        #        if t.starargs:
        #            if comma: self.write(", ")
        #            else: comma = True
        #            self.write("*")
        #            self.dispatch(t.starargs)
        #        if t.kwargs:
        #            if comma: self.write(", ")
        #            else: comma = True
        #            self.write("**")
        #            self.dispatch(t.kwargs)
        #    self.write(")")
        #elif t.bases:
        #        self.write("(")
        #        for a in t.bases:
        #            self.dispatch(a)
        #            self.write(", ")
        #        self.write(")")
        #self.enter()
        #self.dispatch(t.body)
        #self.leave()

    def _generic_FunctionDef(self, t, is_async=False):
        self.write("\n")
        for deco in t.decorator_list:
            self.fill("// Decorator: ")
            self.dispatch(deco)
        if is_async:
            self.write('/* async */ ')

        if getattr(t, "returns", False):
            if isinstance(t.returns, ast.NameConstant):
                if t.returns.value is None:
                    self.write('void')
                else:
                    self.dispatch(t.returns)
            else:
                self.dispatch(t.returns)

            self.fill(" " + t.name + "(")
        else:
            self.fill("auto " + t.name + "(")

        self.dispatch(t.args)

        self.write(")")
        self.enter()
        self.dispatch(t.body)
        self.leave()

    def _FunctionDef(self, t):
        self._generic_FunctionDef(t)

    def _AsyncFunctionDef(self, t):
        self._generic_FunctionDef(t, is_async=True)

    def _generic_For(self, t, is_async=False):
        if is_async:
            self.fill("/* async */ for (")
        else:
            self.fill("for (")
        if isinstance(t.target, ast.Tuple):
            self.write("auto ")
            if len(t.target.elts) == 1:
                (elt, ) = t.target.elts
                self.locals.define(elt.id, t.lineno, self._indent + 1)
                self.dispatch(elt)
            else:
                self.write("[")
                interleave(lambda: self.write(", "), self.dispatch,
                           t.target.elts)
                for elt in t.target.elts:
                    self.locals.define(elt.id, t.lineno, self._indent + 1)
                self.write("]")

        else:
            if not self.locals.is_defined(t.target.id, self._indent):
                self.locals.define(t.target.id, t.lineno, self._indent + 1)
                self.write('auto ')
            self.dispatch(t.target)

        self.write(" : ")
        self.dispatch(t.iter)
        self.write(")")
        self.enter()
        self.dispatch(t.body)
        self.leave()
        if t.orelse:
            raise SyntaxError('Invalid C++')

    def _For(self, t):
        self._generic_For(t)

    def _AsyncFor(self, t):
        self._generic_For(t, is_async=True)

    def _If(self, t):
        self.fill("if (")
        self.dispatch(t.test)
        self.write(')')
        self.enter()
        self.dispatch(t.body)
        self.leave()
        # collapse nested ifs into equivalent elifs.
        while (t.orelse and len(t.orelse) == 1
               and isinstance(t.orelse[0], ast.If)):
            t = t.orelse[0]
            self.fill("else if (")
            self.dispatch(t.test)
            self.write(')')
            self.enter()
            self.dispatch(t.body)
            self.leave()
        # final else
        if t.orelse:
            self.fill("else")
            self.enter()
            self.dispatch(t.orelse)
            self.leave()

    def _While(self, t):
        self.fill("while (")
        self.dispatch(t.test)
        self.write(')')
        self.enter()
        self.dispatch(t.body)
        self.leave()
        if t.orelse:
            raise SyntaxError('Invalid C++')

    def _generic_With(self, t, is_async=False):
        raise SyntaxError('Invalid C++')

    def _With(self, t):
        self._generic_With(t)

    def _AsyncWith(self, t):
        self._generic_With(t, is_async=True)

    # expr
    def _Bytes(self, t):
        self.write(repr(t.s))

    def _Str(self, tree):
        result = ''
        if six.PY3:
            result = repr(tree.s)
        else:
            # if from __future__ import unicode_literals is in effect,
            # then we want to output string literals using a 'b' prefix
            # and unicode literals with no prefix.
            if "unicode_literals" not in self.future_imports:
                result = repr(tree.s)
            elif isinstance(tree.s, str):
                result = "b" + repr(tree.s)
            elif isinstance(tree.s, unicode):
                result = repr(tree.s).lstrip("u")
            else:
                assert False, "shouldn't get here"

        self.write(result.replace('\'', '\"'))

    format_conversions = {97: 'a', 114: 'r', 115: 's'}

    def _FormattedValue(self, t):
        # FormattedValue(expr value, int? conversion, expr? format_spec)
        self.write("{")
        self.dispatch(t.value)
        if t.conversion is not None and t.conversion != -1:
            self.write("!")
            self.write(self.format_conversions[t.conversion])
            #raise NotImplementedError(ast.dump(t, True, True))
        if t.format_spec is not None:
            self.write(":")
            if isinstance(t.format_spec, ast.Str):
                self.write(t.format_spec.s)
            else:
                self.dispatch(t.format_spec)
        self.write("}")

    def _JoinedStr(self, t):
        # JoinedStr(expr* values)
        self.write("f'''")
        for value in t.values:
            if isinstance(value, ast.Str):
                self.write(value.s)
            else:
                self.dispatch(value)
        self.write("'''")

    def _Name(self, t):
        if t.id in _py2c_reserved:
            self.write(_py2c_reserved[t.id])
        else:
            self.write(t.id)

    def _NameConstant(self, t):
        self.write(_py2c_nameconst[t.value])

    def _Repr(self, t):
        raise SyntaxError('Invalid C++')

    def _Num(self, t):
        repr_n = repr(t.n)
        if six.PY3:
            if repr_n.endswith("j"):
                # FIXME: Complex is not a native type in C++, this type-hack should deduce the target type
                self.write(
                    "dace::complexJ()*%s" % repr_n.replace("inf", INFSTR)[:-1])
            else:
                self.write(repr_n.replace("inf", INFSTR))
        else:
            # Parenthesize negative numbers, to avoid turning (-1)**2 into -1**2.
            if repr_n.startswith("-"):
                self.write("(")
            if "inf" in repr_n and repr_n.endswith("*j"):
                repr_n = repr_n.replace("*j", "j")

            if repr_n.endswith("j"):
                # FIXME: Complex is not a native type in C++, this type-hack should deduce the target type
                self.write(
                    "dace::complexJ()*%s" % repr_n.replace("inf", INFSTR)[:-1])
            else:
                # Substitute overflowing decimal literal for AST infinities.
                self.write(repr_n.replace("inf", INFSTR))

            if repr_n.startswith("-"):
                self.write(")")

    def _List(self, t):
        raise SyntaxError('Invalid C++')
        #self.write("[")
        #interleave(lambda: self.write(", "), self.dispatch, t.elts)
        #self.write("]")

    def _ListComp(self, t):
        raise SyntaxError('Invalid C++')
        #self.write("[")
        #self.dispatch(t.elt)
        #for gen in t.generators:
        #    self.dispatch(gen)
        #self.write("]")

    def _GeneratorExp(self, t):
        raise SyntaxError('Invalid C++')
        #self.write("(")
        #self.dispatch(t.elt)
        #for gen in t.generators:
        #    self.dispatch(gen)
        #self.write(")")

    def _SetComp(self, t):
        raise SyntaxError('Invalid C++')
        #self.write("{")
        #self.dispatch(t.elt)
        #for gen in t.generators:
        #    self.dispatch(gen)
        #self.write("}")

    def _DictComp(self, t):
        raise SyntaxError('Invalid C++')
        #self.write("{")
        #self.dispatch(t.key)
        #self.write(": ")
        #self.dispatch(t.value)
        #for gen in t.generators:
        #    self.dispatch(gen)
        #self.write("}")

    def _comprehension(self, t):
        raise SyntaxError('Invalid C++')
        #if getattr(t, 'is_async', False):
        #    self.write(" async")
        #self.write(" for ")
        #self.dispatch(t.target)
        #self.write(" in ")
        #self.dispatch(t.iter)
        #for if_clause in t.ifs:
        #    self.write(" if ")
        #    self.dispatch(if_clause)

    def _IfExp(self, t):
        self.write("(")
        self.dispatch(t.test)
        self.write(" ? ")
        self.dispatch(t.body)
        self.write(" : ")
        self.dispatch(t.orelse)
        self.write(")")

    def _Set(self, t):
        raise SyntaxError('Invalid C++')
        #assert(t.elts) # should be at least one element
        #self.write("{")
        #interleave(lambda: self.write(", "), self.dispatch, t.elts)
        #self.write("}")

    def _Dict(self, t):
        raise SyntaxError('Invalid C++')
        #self.write("{")
        #def write_pair(pair):
        #    (k, v) = pair
        #    self.dispatch(k)
        #    self.write(": ")
        #    self.dispatch(v)
        #interleave(lambda: self.write(", "), write_pair, zip(t.keys, t.values))
        #self.write("}")

    def _Tuple(self, t):
        self.write("std::make_tuple(")
        if len(t.elts) == 1:
            (elt, ) = t.elts
            self.dispatch(elt)
            self.write(",")
        else:
            interleave(lambda: self.write(", "), self.dispatch, t.elts)
        self.write(")")

    unop = {"Invert": "~", "Not": "!", "UAdd": "+", "USub": "-"}

    def _UnaryOp(self, t):
        self.write("(")
        self.write(self.unop[t.op.__class__.__name__])
        self.write(" ")
        if six.PY2 and isinstance(t.op, ast.USub) and isinstance(
                t.operand, ast.Num):
            # If we're applying unary minus to a number, parenthesize the number.
            # This is necessary: -2147483648 is different from -(2147483648) on
            # a 32-bit machine (the first is an int, the second a long), and
            # -7j is different from -(7j).  (The first has real part 0.0, the second
            # has real part -0.0.)
            self.write("(")
            self.dispatch(t.operand)
            self.write(")")
        else:
            self.dispatch(t.operand)
        self.write(")")

    binop = {
        "Add": "+",
        "Sub": "-",
        "Mult": "*",
        "Div": "/",
        "Mod": "%",
        "LShift": "<<",
        "RShift": ">>",
        "BitOr": "|",
        "BitXor": "^",
        "BitAnd": "&"
    }
    funcops = {
        "FloorDiv": (" /", "dace::math::ifloor"),
        "MatMult": (",", "dace::gemm")
    }

    def _BinOp(self, t):
        # Operations that require a function call
        if t.op.__class__.__name__ in self.funcops:
            separator, func = self.funcops[t.op.__class__.__name__]
            self.write(func + "(")
            self.dispatch(t.left)
            self.write(separator + " ")
            self.dispatch(t.right)
            self.write(")")
        # Special case for integer power
        elif t.op.__class__.__name__ == 'Pow':
            if (isinstance(t.right, ast.Num) and int(t.right.n) == t.right.n
                    and t.right.n >= 0):
                self.write("(")
                if t.right.n == 0:
                    self.write("1")
                else:
                    self.dispatch(t.left)
                    for i in range(int(t.right.n) - 1):
                        self.write(" * ")
                        self.dispatch(t.left)
                self.write(")")
            else:
                self.write("dace::math::pow(")
                self.dispatch(t.left)
                self.write(", ")
                self.dispatch(t.right)
                self.write(")")
        else:
            self.write("(")
            self.dispatch(t.left)
            self.write(" " + self.binop[t.op.__class__.__name__] + " ")
            self.dispatch(t.right)
            self.write(")")

    cmpops = {
        "Eq": "==",
        "NotEq": "!=",
        "Lt": "<",
        "LtE": "<=",
        "Gt": ">",
        "GtE": ">=",
        "Is": "==",
        "IsNot": "!=",
        #"In":"in", "NotIn":"not in"
    }

    def _Compare(self, t):
        self.write("(")
        self.dispatch(t.left)
        for o, e in zip(t.ops, t.comparators):
            if o.__class__.__name__ not in self.cmpops:
                raise SyntaxError('Invalid C++')

            self.write(" " + self.cmpops[o.__class__.__name__] + " ")
            self.dispatch(e)
        self.write(")")

    boolops = {ast.And: '&&', ast.Or: '||'}

    def _BoolOp(self, t):
        self.write("(")
        s = " %s " % self.boolops[t.op.__class__]
        interleave(lambda: self.write(s), self.dispatch, t.values)
        self.write(")")

    def _Attribute(self, t):
        self.dispatch(t.value)
        # Special case: 3.__abs__() is a syntax error, so if t.value
        # is an integer literal then we need to either parenthesize
        # it or add an extra space to get 3 .__abs__().
        if isinstance(t.value, ast.Num) and isinstance(t.value.n, int):
            self.write(" ")
        self.write(".")
        self.write(t.attr)

    def _Call(self, t):
        self.dispatch(t.func)
        self.write("(")
        comma = False
        for e in t.args:
            if comma: self.write(", ")
            else: comma = True
            self.dispatch(e)
        for e in t.keywords:
            if comma: self.write(", ")
            else: comma = True
            self.dispatch(e)
        if sys.version_info[:2] < (3, 5):
            if t.starargs:
                raise SyntaxError('Invalid C++')
            if t.kwargs:
                raise SyntaxError('Invalid C++')
        self.write(")")

    def _Subscript(self, t):
        self.dispatch(t.value)
        self.write("[")
        self.dispatch(t.slice)
        self.write("]")

    def _Starred(self, t):
        raise SyntaxError('Invalid C++')

    # slice
    def _Ellipsis(self, t):
        self.write("...")

    def _Index(self, t):
        self.dispatch(t.value)

    def _Slice(self, t):
        if t.lower:
            self.dispatch(t.lower)
        self.write(":")
        if t.upper:
            self.dispatch(t.upper)
        if t.step:
            self.write(":")
            self.dispatch(t.step)

    def _ExtSlice(self, t):
        interleave(lambda: self.write(', '), self.dispatch, t.dims)

    # argument
    def _arg(self, t):
        if t.annotation:
            self.dispatch(t.annotation)
            self.write(' ')
        else:
            self.write("auto ")
        self.write(t.arg)
        self.locals.define(t.arg, t.lineno, self._indent)

    # others
    def _arguments(self, t):
        first = True
        # normal arguments
        defaults = [None] * (len(t.args) - len(t.defaults)) + t.defaults
        for a, d in zip(t.args, defaults):
            if first: first = False
            else: self.write(", ")

            # ast.arg does not exist in python2
            if six.PY2:
                self.write("auto ")
                self.locals.define(a.id, a.lineno, self._indent)

            self.dispatch(a)
            if d:
                self.write("=")
                self.dispatch(d)

        # varargs, or bare '*' if no varargs but keyword-only arguments present
        if t.vararg or getattr(t, "kwonlyargs", False):
            raise SyntaxError('Invalid C++')

        # keyword-only arguments
        if getattr(t, "kwonlyargs", False):
            raise SyntaxError('Invalid C++')

        # kwargs
        if t.kwarg:
            raise SyntaxError('Invalid C++')

    def _keyword(self, t):
        raise SyntaxError('Invalid C++')

    def _Lambda(self, t):
        self.write("(")
        self.write("[] (")
        self.dispatch(t.args)
        self.write(") { return ")
        self.dispatch(t.body)
        self.write("; } )")

    def _alias(self, t):
        self.write('using ')
        self.write(t.name)
        if t.asname:
            self.write(" = " + t.asname)
        self.write(';')

    def _withitem(self, t):
        raise SyntaxError('Invalid C++')

    def _Await(self, t):
        raise SyntaxError('Invalid C++')


def cppunparse(node, expr_semicolon=True):
    strio = StringIO()
    CPPUnparser(node, 0, CPPLocals(), strio, expr_semicolon=expr_semicolon)
    return strio.getvalue().strip()


# Code can either be a string or a function
def py2cpp(code, expr_semicolon=True):
    if isinstance(code, str):
        return cppunparse(ast.parse(code), expr_semicolon)
    elif code.__class__.__name__ == 'function':
        try:
            code_str = inspect.getsource(code)

            # Remove leading indentation
            lines = code_str.splitlines()
            leading_spaces = len(lines[0]) - len(lines[0].lstrip())
            code_str = ''
            for line in lines:
                code_str += line[leading_spaces:] + '\n'

        except:  # Can be different exceptions coming from Python's AST module
            raise TypeError('Invalid function given')
        return cppunparse(ast.parse(code_str), expr_semicolon)

    else:
        raise TypeError('Unsupported type for py2cpp')


def pyexpr2cpp(expr):
    return py2cpp(expr, expr_semicolon=False)
