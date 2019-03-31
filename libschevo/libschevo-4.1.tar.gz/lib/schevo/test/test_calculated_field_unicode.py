"""Calculated field unicode representation tests."""

# Copyright (c) 2001-2009 ElevenCraft Inc.
# See LICENSE for details.

from textwrap import dedent

from schevo.test import CreatesSchema, PREAMBLE


class BaseCalculatedUnicode(CreatesSchema):

    body = '''

    class Thing(E.Entity):
        image = f.image()
        password = f.hashed_password()
        @f.image()
        def calc_image(self):
            return self.image
        @f.hashed_password()
        def calc_password(self):
            return self.password
    '''

    def test_representations(self):
        thing = db.execute(db.Thing.t.create(
            image='some-image-data',
            password='some-password',
            ))
        # Unicode reprs of fields on thing itself.
        assert str(thing.f.image) == '(Binary data)'
        assert str(thing.f.password) == '(Encrypted)'
        assert str(thing.f.calc_image) == '(Binary data)'
        assert str(thing.f.calc_password) == '(Encrypted)'
        # Unicode reprs of fields on thing's default view.
        thing_view = thing.v.default()
        assert str(thing_view.f.image) == '(Binary data)'
        assert str(thing_view.f.password) == '(Encrypted)'
        assert str(thing_view.f.calc_image) == '(Binary data)'
        assert str(thing_view.f.calc_password) == '(Encrypted)'


# class TestCalculatedUnicode1(BaseCalculatedUnicode):

#     include = True

#     format = 1


class TestCalculatedUnicode2(BaseCalculatedUnicode):

    include = True

    format = 2
