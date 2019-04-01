
import bdb
import re
import pdb
import sys
import linecache
from hrepr import HTML
from .repr import hrepr


H = HTML()


class BucheDb(bdb.Bdb):
    # Note: Many methods have been lifted from pdb.py in the standard lib
    # and slightly adapted

    def __init__(self, repl):
        super().__init__()
        self.repl = repl
        self.frame = None
        self.display_frame = True
        self.stack = []
        self.current = 0

    def eval(self, repl, code, code_globals):
        frame = self.get_frame()
        gs = {**frame.f_globals, **code_globals.globals}
        ls = frame.f_locals
        m = re.match(r'^[?!]+', code)
        if m:
            cmd = code[:m.end()]
            arg = code[m.end():]
        elif ' ' in code:
            cmd, arg = code.split(' ', 1)
        else:
            cmd = code
            arg = ''
        method = self.__commands__.get(cmd, None)
        if method:
            return method(self, arg, gs, ls)
        else:
            return self.command_print(code, gs, ls)

    def setup(self, frame, tb):
        self.stack, self.current = self.get_stack(frame, tb)

    def checkline(self, filename, lineno):
        """Check whether specified line seems to be executable.

        Return `lineno` if it is, 0 if not (e.g. a docstring, comment, blank
        line or EOF). Warning: testing is not comprehensive.
        """
        # this method should be callable before starting debugging, so default
        # to "no globals" if there is no current frame
        curframe = self.get_frame()
        globs = curframe.f_globals if curframe else None
        line = linecache.getline(filename, lineno, globs)
        if not line:
            self.message('End of file')
            return 0
        line = line.strip()
        # Don't allow setting breakpoint at a blank line
        if (not line or (line[0] == '#') or
             (line[:3] == '"""') or line[:3] == "'''"):
            self.error('Blank or comment')
            return 0
        return lineno

    def print_stack_trace(self):
        res = H.boxTabs()
        stack = self.stack[:self.current + 1]
        for i, (entry, lineno) in enumerate(stack):
            code = entry.f_code
            res = res(H.tabEntry(
                hrepr(entry),
                label=f'{code.co_name}@{code.co_filename}:{entry.f_lineno}',
                active=(i == len(stack) - 1)
            ))
        self.repl.log(res, interactive=True)

    def command_step(self, arg, gs, ls):
        """<b>s(tep)</b>

        Execute the current line, stop at the first possible occasion
        (either in a function that is called or in the current function).
        """
        self.set_step()
        self.proceed = True

    def command_next(self, arg, gs, ls):
        """<b>n(ext)</b>

        Continue execution until the next line in the current function
        is reached or it returns.
        """
        self.set_next(self.get_frame())
        self.proceed = True

    def command_continue(self, arg, gs, ls):
        """<b>c(ont(inue))</b>

        Continue execution, only stop when a breakpoint is encountered.
        """
        self.set_continue()
        self.proceed = True

    def command_return(self, arg, gs, ls):
        """<b>r(eturn)</b>

        Continue execution until the current function returns.
        """
        self.set_return()
        self.proceed = True

    def command_until(self, arg, gs, ls):
        """<b>unt(il) [lineno]</b>

        Without argument, continue execution until the line with a
        number greater than the current one is reached.  With a line
        number, continue execution until a line with a number greater
        or equal to that is reached.  In both cases, also stop when
        the current frame returns.
        """
        curframe = self.get_frame()
        if arg:
            try:
                lineno = int(arg)
            except ValueError:
                self.error('Error in argument: %r' % arg)
                return
            if lineno <= curframe.f_lineno:
                self.error('"until" line number is smaller than current '
                           'line number')
                return
        else:
            lineno = None
        self.set_until(curframe, lineno)
        self.proceed = True

    def command_up(self, arg, gs, ls):
        """<b>u(p) [count]</b>

        Move the current frame count (default one) levels up in the
        stack trace (to an older frame).
        """
        if self.current == 0:
            self.error('Oldest frame')
            return
        try:
            count = int(arg or 1)
        except ValueError:
            self.error('Invalid frame count (%s)' % arg)
            return
        if count < 0:
            self.current = 0
        else:
            self.current = max(0, self.current - count)
        self.repl.log(self.get_frame())

    def command_down(self, arg, gs, ls):
        """<b>d(own) [count]</b>

        Move the current frame count (default one) levels down in the
        stack trace (to a newer frame).
        """
        if self.current + 1 == len(self.stack):
            self.error('Newest frame')
            return
        try:
            count = int(arg or 1)
        except ValueError:
            self.error('Invalid frame count (%s)' % arg)
            return
        if count < 0:
            self.current = len(self.stack) - 1
        else:
            self.current = min(len(self.stack) - 1, self.current + count)
        self.repl.log(self.get_frame())

    def command_break(self, arg, gs, ls, temporary = 0):
        """<b>b(reak) [ ([filename:]lineno | function) [, condition] ]</b>

        Without argument, list all breaks.

        With a line number argument, set a break at this line in the
        current file.  With a function name, set a break at the first
        executable line of that function.  If a second argument is
        present, it is a string specifying an expression which must
        evaluate to true before the breakpoint is honored.

        The line number may be prefixed with a filename and a colon,
        to specify a breakpoint in another file (probably one that
        hasn't been loaded yet).  The file is searched for on
        sys.path; the .py suffix may be omitted.
        """
        curframe = self.get_frame()
        if not arg:
            if self.breaks:
                t = H.table()
                t = t(H.tr(
                    H.th('Num'),
                    H.th('Disp'),
                    H.th('Enb'),
                    H.th('Where'),
                ))
                for bp in bdb.Breakpoint.bpbynumber:
                    if bp:
                        disp = 'del' if bp.temporary else 'keep'
                        enb = 'yes' if bp.enabled else 'no'
                        t = t(H.tr(
                            H.td(bp.number),
                            H.td(disp),
                            H.td(enb),
                            H.td(f'{bp.file}:{bp.line}'),
                        ))
                self.repl.log.html(t)
            return
        # parse arguments; comma has lowest precedence
        # and cannot occur in filename
        filename = None
        lineno = None
        cond = None
        comma = arg.find(',')
        if comma > 0:
            # parse stuff after comma: "condition"
            cond = arg[comma+1:].lstrip()
            arg = arg[:comma].rstrip()
        # parse stuff before comma: [filename:]lineno | function
        colon = arg.rfind(':')
        funcname = None
        if colon >= 0:
            filename = arg[:colon].rstrip()
            f = self.lookupmodule(filename)
            if not f:
                self.error('%r not found from sys.path' % filename)
                return
            else:
                filename = f
            arg = arg[colon+1:].lstrip()
            try:
                lineno = int(arg)
            except ValueError:
                self.error('Bad lineno: %s' % arg)
                return
        else:
            # no colon; can be lineno or function
            try:
                lineno = int(arg)
            except ValueError:
                try:
                    func = eval(arg,
                                curframe.f_globals,
                                curframe_locals)
                except:
                    func = arg
                try:
                    if hasattr(func, '__func__'):
                        func = func.__func__
                    code = func.__code__
                    #use co_name to identify the bkpt (function names
                    #could be aliased, but co_name is invariant)
                    funcname = code.co_name
                    lineno = code.co_firstlineno
                    filename = code.co_filename
                except:
                    # last thing to try
                    (ok, filename, ln) = self.lineinfo(arg)
                    if not ok:
                        self.error('The specified object %r is not a function '
                                   'or was not found along sys.path.' % arg)
                        return
                    funcname = ok # ok contains a function name
                    lineno = int(ln)
        if not filename:
            filename = curframe.f_code.co_filename
        # Check for reasonable breakpoint
        line = self.checkline(filename, lineno)
        if line:
            # now set the break point
            err = self.set_break(filename, line, temporary, cond, funcname)
            if err:
                self.error(err)
            else:
                bp = self.get_breaks(filename, line)[-1]
                self.message("Breakpoint %d at %s:%d" %
                             (bp.number, bp.file, bp.line))

    def command_tbreak(self, arg, gs, ls):
        """<b>tbreak [ ([filename:]lineno | function) [, condition] ]</b>

        Same arguments as break, but sets a temporary breakpoint: it
        is automatically deleted when first hit.
        """
        self.command_break(arg, gs, ls, 1)

    def command_enable(self, arg, gs, ls):
        """<b>enable bpnumber [bpnumber ...]</b>

        Enables the breakpoints given as a space separated list of
        breakpoint numbers.
        """
        args = arg.split()
        for i in args:
            try:
                bp = self.get_bpbynumber(i)
            except ValueError as err:
                self.error(err)
            else:
                bp.enable()
                self.message('Enabled %s' % bp)

    def command_disable(self, arg, gs, ls):
        """<b>disable bpnumber [bpnumber ...]</b>

        Disables the breakpoints given as a space separated list of
        breakpoint numbers.  Disabling a breakpoint means it cannot
        cause the program to stop execution, but unlike clearing a
        breakpoint, it remains in the list of breakpoints and can be
        (re-)enabled.
        """
        args = arg.split()
        for i in args:
            try:
                bp = self.get_bpbynumber(i)
            except ValueError as err:
                self.error(err)
            else:
                bp.disable()
                self.message('Disabled %s' % bp)

    def command_condition(self, arg, gs, ls):
        """<b>condition bpnumber [condition]</b>

        Set a new condition for the breakpoint, an expression which
        must evaluate to true before the breakpoint is honored.  If
        condition is absent, any existing condition is removed; i.e.,
        the breakpoint is made unconditional.
        """
        args = arg.split(' ', 1)
        try:
            cond = args[1]
        except IndexError:
            cond = None
        try:
            bp = self.get_bpbynumber(args[0].strip())
        except IndexError:
            self.error('Breakpoint number expected')
        except ValueError as err:
            self.error(err)
        else:
            bp.cond = cond
            if not cond:
                self.message('Breakpoint %d is now unconditional.' % bp.number)
            else:
                self.message('New condition set for breakpoint %d.' % bp.number)

    def command_ignore(self, arg, gs, ls):
        """<b>ignore bpnumber [count]</b>

        Set the ignore count for the given breakpoint number.  If
        count is omitted, the ignore count is set to 0.  A breakpoint
        becomes active when the ignore count is zero.  When non-zero,
        the count is decremented each time the breakpoint is reached
        and the breakpoint is not disabled and any associated
        condition evaluates to true.
        """
        args = arg.split()
        try:
            count = int(args[1].strip())
        except:
            count = 0
        try:
            bp = self.get_bpbynumber(args[0].strip())
        except IndexError:
            self.error('Breakpoint number expected')
        except ValueError as err:
            self.error(err)
        else:
            bp.ignore = count
            if count > 0:
                if count > 1:
                    countstr = '%d crossings' % count
                else:
                    countstr = '1 crossing'
                self.message('Will ignore next %s of breakpoint %d.' %
                             (countstr, bp.number))
            else:
                self.message('Will stop next time breakpoint %d is reached.'
                             % bp.number)

    def command_clear(self, arg, gs, ls):
        """<b>cl(ear) filename:lineno\ncl(ear) [bpnumber [bpnumber...]]</b>
    
        With a space separated list of breakpoint numbers, clear
        those breakpoints.  Without argument, clear all breaks (but
        first ask confirmation).  With a filename:lineno argument,
        clear all breaks at that line in that file.
        """
        if not arg:
            try:
                reply = input('Clear all breaks? ')
            except EOFError:
                reply = 'no'
            reply = reply.strip().lower()
            if reply in ('y', 'yes'):
                bplist = [bp for bp in bdb.Breakpoint.bpbynumber if bp]
                self.clear_all_breaks()
                for bp in bplist:
                    self.message('Deleted %s' % bp)
            return
        if ':' in arg:
            # Make sure it works for "clear C:\foo\bar.py:12"
            i = arg.rfind(':')
            filename = arg[:i]
            arg = arg[i+1:]
            try:
                lineno = int(arg)
            except ValueError:
                err = "Invalid line number (%s)" % arg
            else:
                bplist = self.get_breaks(filename, lineno)
                err = self.clear_break(filename, lineno)
            if err:
                self.error(err)
            else:
                for bp in bplist:
                    self.message('Deleted %s' % bp)
            return
        numberlist = arg.split()
        for i in numberlist:
            try:
                bp = self.get_bpbynumber(i)
            except ValueError as err:
                self.error(err)
            else:
                self.clear_bpbynumber(i)
                self.message('Deleted %s' % bp)

    def command_where(self, arg, gs, ls):
        """<b>w(here)</b>

        Print a stack trace, with the most recent frame at the bottom.
        An arrow indicates the "current frame", which determines the
        context of most commands.  'bt' is an alias for this command.
        """
        self.print_stack_trace()

    def command_print(self, code, gs, ls):
        """<b>p(rint) expression</b>

        Print the value of the expression. Synonyms: !, pp
        """
        try:
            return eval(code, gs, ls)
        except SyntaxError:
            return exec(code, gs, ls)

    def command_quit(self, arg, gs, ls):
        """<b>q(uit)</b>

        Quit from the debugger. The program being executed is aborted.
        """
        self._user_requested_quit = True
        self.set_quit()
        self.proceed = True

    def command_help(self, arg, gs, ls):
        """<b>h(elp)</b>

        Without argument, print the list of available commands.
        With a command name as argument, print help about that command.
        """
        if arg:
            self.repl.log.html(self.__commands__[arg].__doc__)
        else:
            commands = [x.__doc__ for x in set(self.__commands__.values())]
            commands.sort()
            for cmd in commands:
                self.repl.log.html(cmd)

    __commands__ = {
        'step': command_step,
        's': command_step,
        'next': command_next,
        'n': command_next,
        'continue': command_continue,
        'c': command_continue,
        'return': command_return,
        'r': command_return,
        'until': command_until,
        'unt': command_until,
        'up': command_up,
        'u': command_up,
        'down': command_down,
        'd': command_down,
        'print': command_print,
        'p': command_print,
        'pp': command_print,
        '!': command_print,
        'help': command_help,
        'h': command_help,
        '?': command_help,
        'break': command_break,
        'tbreak': command_tbreak,
        'enable': command_enable,
        'disable': command_disable,
        'condition': command_condition,
        'ignore': command_ignore,
        'clear': command_clear,
        'cl': command_clear,
        'where': command_where,
        'w': command_where,
        'bt': command_where,
        'quit': command_quit,
        'q': command_quit,
    }

    def error(self, message):
        self.repl.log.html.logEntry['error'](message)

    def message(self, message):
        self.repl.log.html.logEntry(message)

    def get_frame(self):
        return self.stack[self.current][0]

    def set_frame(self, frame, tb=None):
        self.setup(frame, tb)
        self.repl.log(self.get_frame())
        self.proceed = False
        while not self.proceed:
            self.repl.query(eval=self.eval)

    # def user_call(self, frame, args):
    #     self.repl.log.html('<b>Enter call</b>')
    #     self.set_frame(frame)

    def user_line(self, frame):
        self.repl.log.html('<b>Next line</b>')
        self.set_frame(frame)

    # def user_return(self, frame, rval):
    #     self.repl.log.html('<b>Return</b>')
    #     self.set_frame(frame)

    def user_exception(self, frame, exc_info):
        self.repl.log.html('<b>An exception occurred</b>')
        self.repl.log(exc_info)
        self.set_frame(frame)

    def set_trace(self, frame=None):
        self.repl.start(synchronous=True)
        super().set_trace(frame or sys._getframe(1))

    def interaction(self, frame, tb):
        self.repl.start(synchronous=True)
        self.set_frame(frame, tb)
