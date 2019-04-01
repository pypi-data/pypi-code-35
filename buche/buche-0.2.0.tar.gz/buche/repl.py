
from uuid import uuid4


class CodeGlobals:
    def __init__(self, glb=None):
        self.globals = glb or {}
        self.saved = []

    def getvar(self, obj):
        try:
            rank = self.saved.index(obj)
            varname = f'_{rank + 1}'
        except ValueError:
            self.saved.append(obj)
            rank = len(self.saved)
            varname = f'_{rank}'
            self.globals[varname] = obj
        return varname


class Repl:

    @staticmethod
    def default_evaluate(repl, code, code_globals):
        glob = code_globals.globals
        try:
            return eval(code, glob)
        except SyntaxError:
            exec(code, glob)

    def __init__(self,
                 buche,
                 reader,
                 evaluator=None,
                 code_globals=None,
                 address=None,
                 log_address=None):
        self.buche = buche
        self.reader = reader
        self.code_globals = code_globals or CodeGlobals()
        if not isinstance(self.code_globals, CodeGlobals):
            self.code_globals = CodeGlobals(self.code_globals)
        self.address = address or str(uuid4())
        self.relative_log_address = log_address or 'log'
        self.log_address = log_address or f'{self.address}/log'
        self.cmdidx = 0
        self.cmdlog = ['']
        self.input_address = f'{self.address}/input'
        self.input = buche[self.address]['input']
        self.log = buche[self.log_address]
        self.code_globals.globals['buche'] = self.log
        self.eval = evaluator or self.default_evaluate
        self.started = False

    def _repl_key(self, event, message):
        if not message.path.endswith(self.input_address):
            return

        key = message.which
        if key == 'Up':
            self.cmdidx = (self.cmdidx - 1) % len(self.cmdlog)
            self.input.command_set(value=self.cmdlog[self.cmdidx])
        elif key == 'Down':
            self.cmdidx = (self.cmdidx + 1) % len(self.cmdlog)
            self.input.command_set(value=self.cmdlog[self.cmdidx])

    def _repl_line(self, event, message):
        return self.handle_message(message)

    def _repl_select(self, event, message):
        if self.log_address not in message.enclosingPath:
            return

        if hasattr(message, 'obj'):
            varname = self.code_globals.getvar(message.obj)
            self.input.command_append(value=varname)
            self.input.command_focus()

    def handle_message(self, message, eval=None):
        if message.eventType != 'submit':
            return False
        if not message.path.endswith(self.input_address):
            return False
        return self.run(message.value, eval)

    def run(self, code, eval=None):
        if code.strip() == '':
            return False
        self.log.html.logEntry['echo'](code)
        self.input.command_set()
        try:
            res = (eval or self.eval)(self, code, self.code_globals)
        except Exception as exc:
            self.log.show.logEntry['error'](exc)
        else:
            if res is not None:
                self.log.show.logEntry['result'](res, interactive=True)
        self.cmdlog.append(code)
        self.cmdidx = 0
        return True

    def start(self, nodisplay=False, synchronous=False):
        if self.started:
            return

        if not nodisplay:
            self.buche(self)

        if not synchronous:
            self.reader.on_submit(self._repl_line)
        self.reader.on_keyup(self._repl_key)
        self.reader.on_click(self._repl_select)
        self.reader.start()
        self.input.command_focus()
        self.started = True

    def query(self, eval=None):
        while True:
            message = self.reader.read()
            if not self.handle_message(message, eval):
                continue
            break

    def __hrepr__(self, H, hrepr):
        return H.div['repl-box'](
            H.bucheLog(address=self.relative_log_address),
            H.bucheInput(address='input'),
            style="height:100%;width:100%;display:flex;flex-direction:column",
            address=self.address
        )
