"""Evolution test schema, version 2."""

# All Schevo schema modules must have these lines.
from schevo.schema import *
schevo.schema.prep(locals())


class Foo(E.Entity):

    name = f.string()

    _key(name)

    _initial = [
        ('three', ),
        ('one', ),
        ('two', ),
        ('four', ),
        ]


def after_evolve(db):
    db.execute(db.Foo.t.create(name='four'))
