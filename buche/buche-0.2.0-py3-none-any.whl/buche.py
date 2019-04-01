
import asyncio
import json
import re
from threading import Thread
from uuid import uuid4 as uuid
from hrepr import Tag
from .event import EventDispatcher
from .repr import id_registry


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Tag):
            return str(obj)
        else:
            super().default(obj)


encoder = Encoder()


class BucheMessage:
    def __init__(self, d):
        self.__dict__.update(d)

    def __hrepr__(self, H, hrepr):
        return hrepr.stdrepr_object('BucheMessage', self.__dict__.items())


class BucheSeq:
    def __init__(self, objects):
        self.objects = list(objects)

    @classmethod
    def __hrepr_resources__(cls, H):
        return H.style('''
        .multi-print { display: flex; align-items: center; }
        .multi-print > * { margin-right: 10px; }
        ''')

    def __hrepr__(self, H, hrepr):
        return H.div['multi-print'](*map(hrepr, self.objects))


class BucheDict:
    def __init__(self, keys):
        if hasattr(keys, 'items'):
            self.keys = keys.items()
        else:
            self.keys = keys

    def __hrepr__(self, H, hrepr):
        return hrepr.stdrepr_object(None, self.keys)


class MasterBuche:
    def __init__(self, hrepr, write):
        self.hrepr = hrepr
        self.write = write
        self.resources = set()

    def require(self, plugin):
        self.send(command='plugin', name=plugin)

    def send(self, d={}, **params):
        message = {**d, **params}
        self.write(encoder.encode(message))

    def generate(self, obj, hrepr_params={}):
        x = self.hrepr(obj, **hrepr_params)
        for res in self.hrepr.resources - self.resources:
            if res.name == 'buche-require':
                self.send(
                    command = 'plugin',
                    name = res.attributes['name']
                )
            else:
                self.send(
                    command = 'resource',
                    content = str(res)
                )
            self.resources.add(res)
        return x

    def show(self, obj, hrepr_params={}, **params):
        x = self.generate(obj, hrepr_params)
        self.send(format='html', content=str(x), **params)


class HTMLSender:
    def __init__(self, buche, current, open=False, repr=False):
        self.__buche = buche
        self.__current = current
        self.__open = open
        self.__repr = repr

    def __getattr__(self, attr):
        return HTMLSender(self.__buche,
                          getattr(self.__current, attr),
                          self.__open,
                          self.__repr)

    def __getitem__(self, item):
        return HTMLSender(self.__buche,
                          self.__current[item],
                          self.__open,
                          self.__repr)

    def __call__(self, *args, **kwargs):
        args = [self.__buche.master.generate(arg, kwargs)
                if self.__repr else arg
                for arg in args]
        address = None
        if isinstance(self.__current, Tag):
            if self.__repr:
                res = self.__current(*args)
            else:
                res = self.__current(*args, **kwargs)
            if self.__open and 'address' not in res.attributes:
                res = res(address=f'/{str(uuid())}')
            address = res.attributes.get('address', None)
        else:
            res = "".join(map(str, args))
        self.__buche.send(content=str(res))
        if self.__open:
            if address is not None:
                return self.__buche[address]
            else:
                raise Exception('Buche.open cannot be called directly.')


class Buche:
    def __init__(self, master, parent):
        self.master = master
        self.parent = parent

    def require(self, plugin, **opts):
        self.master.require(plugin, **opts)

    def send(self, parent=None, **params):
        if parent is None:
            cmd = params.get('command', 'log')
            if cmd in {'template', 'plugin', 'redirect', 'resource'}:
                self.master.send(**params)
                return
            parent = self.parent
        elif parent.startswith('/'):
            pass
        else:
            parent = self.join_path(parent)
        self.master.send(parent=parent, **params)

    @property
    def html(self):
        return HTMLSender(self, self.master.hrepr.H, False)

    @property
    def show(self):
        return HTMLSender(self, self.master.hrepr.H, False, True)

    @property
    def open(self):
        return HTMLSender(self, self.master.hrepr.H, True)

    def join_path(self, p):
        return f'{self.parent.rstrip("/")}/{p.strip("/")}'

    def __getattr__(self, attr):
        if attr.startswith('command_'):
            def cmd(**kwargs):
                self.send(
                    command=attr[8:],
                    **kwargs
                )
            return cmd
        else:
            return getattr(super(), attr)

    def __getitem__(self, item):
        if not item.startswith('/'):
            item = self.join_path(item)
        return Buche(self.master, item)

    def dict(self, **keys):
        self(BucheDict(keys))

    def __call__(self, *objs, **hrepr_params):
        if len(objs) == 1:
            o, = objs
        else:
            o = BucheSeq(objs)
        self.master.show(o, hrepr_params=hrepr_params, parent=self.parent)


class Reader(EventDispatcher):
    def __init__(self, source):
        super().__init__()
        self.ev_loop = asyncio.get_event_loop()
        self.source = source
        self.thread = Thread(target=self.loop)
        self.futures = []

    def read(self):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.read_async())

    def parse(self, line):
        d = json.loads(line)
        if 'argument' in d and 'obj' not in d:
            arg = d['argument']
            if arg:
                d['obj'] = id_registry.resolve(int(arg))
        message = BucheMessage(d)
        self.emit(d.get('eventType', 'UNDEFINED'), message)
        # Provide the message to all the coroutines waiting for one
        futs, self.futures = self.futures, []
        for fut in futs:
            self.ev_loop.call_soon_threadsafe(fut.set_result, message)
        return message

    def __iter__(self):
        for line in self.source:
            yield self.parse(line)

    def loop(self):
        for _ in self:
            pass

    def start(self):
        if not self.thread.is_alive():
            self.thread.start()

    def read_async(self):
        fut = asyncio.Future()
        self.futures.append(fut)
        return fut
