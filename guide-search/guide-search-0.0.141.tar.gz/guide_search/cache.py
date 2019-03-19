import uuid
import time
import hashlib

class store():
    that = None
    cache = {}
    dirty = {}
    last_check = 0

    def __init__(self, that, save=True, latency=60):
        self.that = that
        self.save = save
        self.latency = latency

    def hash(self, vals):
        h = hashlib.md5()
        for val in vals:
            h.update(val.encode())
        return h.hexdigest()


    def get_dirty(self):
        url = self.that.make_url('common', 'cache', 'dirty')
        if (time.time() - self.last_check) > self.latency:
            try:
                self.dirty = self.that.request("get", url)['_source']
                self.last_check = time.time()
            except:
                self.dirty = {}
                self.put_dirty()

    def put_dirty(self):
        url = self.that.make_url('common', 'cache', 'dirty')
        return self.that.request("put", url, data=self.dirty)


    def get(self, function, name, *args):
        if not self.save:
            return function(self.that, *args)

        self.get_dirty()
        func_cache = self.cache.setdefault(name, {"values": {}, 'dirty' : {}})
        flag = self.dirty.setdefault(name, {})
        hash_args = self.hash(args)
        if hash_args not in flag:
            flag.update({hash_args: uuid.uuid4().hex[:8]})
            self.put_dirty()

        if ((hash_args not in func_cache['values']) or
                (func_cache['dirty'][hash_args] != flag[hash_args])):
            func_cache['values'][hash_args] = function(self.that, *args)
            func_cache['dirty'][hash_args] = self.dirty[name][hash_args]
        return func_cache['values'][hash_args]

    def put(self, function, name, *args):
        try:
            hash_args = self.hash(args[:len(args)-1])
        except:
            hash_args = self.hash(())

        self.get_dirty()
        self.dirty.setdefault(name, {})[hash_args] = uuid.uuid4().hex[:8]
        self.put_dirty()
        function(self.that, *args)
       

 

 


