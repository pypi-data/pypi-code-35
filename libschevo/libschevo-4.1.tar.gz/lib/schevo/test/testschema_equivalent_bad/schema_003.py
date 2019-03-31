"""Evolution test schema, version 3."""

# All Schevo schema modules must have these lines.
from schevo.schema import *
schevo.schema.prep(locals())


class Foo(E.Entity):

    name = f.string()

    _key(name)

    _initial = [
        ('two', ),
        ('one', ),
        ('four', ),
        ('three', ),
        ('five', ),
        ]


def after_evolve(db):
    db.execute(db.Foo.t.create(name='nine'))
