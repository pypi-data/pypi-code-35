from qlib.data import  dbobj, Cache
import os
E = os.path.exists
Mk = os.mkdir
J = os.path.join
iD = os.path.isdir
Home = os.path.expanduser

DB_PATH = Home("~/.config/xproj")
DB = J(DB_PATH, "db.sql")

if not E(DB_PATH):
    Mk(DB_PATH)


class Proj(dbobj):pass

class Con(Cache):

    def fuzzy_search(self, Obj, key):
        for i in self.query(Obj):
            v,r = i.search(key)
            if r:
                yield v,r

def search(key):
    c = Con(DB)
    for v,r in c.fuzzy_search(Proj, key):
        return v,r

def create(name, path, desc=' some desc'):
    c = Con(DB)
    d = Proj(name=name, path=path, desc=desc)
    d.save(c)

