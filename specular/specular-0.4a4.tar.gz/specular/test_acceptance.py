# -*- coding: utf-8 -*-

from specular import (
    global_domain, make_constructor, normalize_source, getval,
    construct_after, construct_last, construct_skip_no_value,
    Error, Bytes, Source, Data, Spec, Processor, Runtime, negotiate,
    ANY, NULL, SkipConstructor,
)
from sortedcontainers import SortedDict
from collections import OrderedDict


test_domain = Spec()


def test_compile_names_are_bytes():

    source = {
        u'hello': (),
        u'καλημέρα': (),
    }

    spec = test_domain.compile_spec(source)
    assert all(type(key) is Bytes for key in spec.nodes)


def test_compile_paths_as_names():

    source = SortedDict({
        'one.two': 0,
        'one.two.three.four': 1,
        'one.foo': 2,
        '.alpha.beta': 3,
        '.alpha.beta.gamma.delta': 4,
        '.alpha.omega': 5,
        'one?two': 12,
        'one?two?three?four': 13,
        'one?foo': 14,
        '?alpha?beta': 15,
        '?alpha?beta?gamma?delta': 16,
        '?alpha?omega': 17,
        '/one.two/three': 1000,
        '/one.two/three?four:five': 1002,
        '/one?two/three': 1003,
        'a.b.': 1004,
        'a.b..': 1005,
        'a?b?': 1008,
        'a?b??': 1009,
        'a/b/': 1010,
        'a/b/c': 1011,
        'a/b/c//': 1012,
        'x': {
            '=': 1013,
            'y': 1014,
            'g': 1015,
        },
        'x/y/a': 1016,
        'x/z/b': 1017,
    })

    spec = test_domain.compile_spec(source)

    assert spec[('one', '.', 'two')] == 0
    assert spec[('one', '.', 'two', 'three', 'four')] == 1
    assert spec[('one', '.', 'foo')] == 2
    assert spec[('.', 'alpha', 'beta')] == 3
    assert spec[('.', 'alpha', 'beta', 'gamma', 'delta')] == 4
    assert spec[('.', 'alpha', 'omega')] == 5

    assert spec[('one', '?', 'two')] == 12
    assert spec[('one', '?', 'two', 'three', 'four')] == 13
    assert spec[('one', '?', 'foo')] == 14
    assert spec[('?', 'alpha', 'beta')] == 15
    assert spec[('?', 'alpha', 'beta', 'gamma', 'delta')] == 16
    assert spec[('?', 'alpha', 'omega')] == 17

    assert spec[('', 'one.two', 'three')] == 1000
    assert spec[('', 'one.two', 'three?four:five')] == 1002
    assert spec[('', 'one?two', 'three')] == 1003

    assert spec[('a', '.', 'b')] == 1004
    assert spec[('a', '.', 'b', '')] == 1005
    assert spec[('a', '?', 'b')] == 1008
    assert spec[('a', '?', 'b', '')] == 1009

    assert spec[('a', 'b')] == 1010
    assert spec[('a', 'b', 'c')] == 1011
    assert spec[('a', 'b', 'c', '')] == 1012

    assert spec[('x',)] == 1013
    assert spec[('x', 'y')] == 1014
    assert spec[('x', 'g')] == 1015
    assert spec[('x', 'y', 'a')] == 1016
    assert spec[('x', 'z', 'b')] == 1017


def test_compile_value_in_path():
    source = {
        'a/b/=': 1,
    }

    try:
        test_domain.compile_spec(source)
    except Exception as e:
        assert type(e) is Error
        assert e.what == 'invalid'
        assert "'='" in e.message
    else:
        raise AssertionError("Error not raised")


def test_compile_path_clash():

    clash_source = {
        'x': {
            'y': 0,
        },
        'x/y': 1,
    }

    try:
        test_domain.compile_spec(clash_source)
    except Error as e:
        assert e.what == 'cannot-normalize'

    simple_match_source = {
        'x': {
            'y': 999,
        },
        'x/y': 999,
    }
    simple_match_spec = test_domain.compile_spec(simple_match_source)
    assert simple_match_spec[('x', 'y')] == 999

    match_source = {
        'x': {
            'y': {
                'z': 999,
            },
        },
        'x/y': {
            'z': 999,
        },
    }
    match_spec = test_domain.compile_spec(match_source)
    assert match_spec[('x', 'y', 'z')] == 999

    faulty_source = {
        'x': {
            'y': {
                'z': 999,
            },
        },
        'x/y': Source({
            'z': 999,
        }),
    }
    try:
        match_spec = test_domain.compile_spec(faulty_source)
    except Exception as e:
        assert type(e) is AssertionError
        assert 'not normal' in e.message
    else:
        raise AssertionError("AssertionError not raised")

    extending_source = {
        'x/y': 1,
        'x/y/z': 2,
        'x/y/z/.': 3,
        'x/y/z/./?': 4,
        'x/y/z/./?/a': 5,
    }
    extending_spec = test_domain.compile_spec(extending_source)
    assert extending_spec[('x', 'y')] == 1
    assert extending_spec[('x', 'y', 'z')] == 2
    assert extending_spec[('x', 'y', 'z', '.')] == 3
    assert extending_spec[('x', 'y', 'z', '.', '?')] == 4
    assert extending_spec[('x', 'y', 'z', '.', '?', 'a')] == 5


def test_compile_autoregister():

    domain = Spec()

    animal_source = {
        '.animal': (),
        'feet': (),
        'diet': (),
    }

    domain.compile_schema('.animal', animal_source)
    animal_spec = domain.compile_spec(animal_source)

    assert domain.schemata.getpath('.animal/') == animal_spec

    no_parent_source = {
        '.thing.property': (),
    }

    try:
        domain.compile_schema('.thing.property', no_parent_source)
    except Exception as e:
        assert type(e) is Error
        assert e.what == 'compile-failed'
        assert len(e.errs) == 1
        assert e.errs[0].what == 'parent-predicate-not-found'
    else:
        m = "Error not raised"
        raise AssertionError(m)


def test_template_predicates_unknown():
    source = {
        'alpha': {
            '?': {
                '.object': (),
            },
        },
    }
    domain = Spec()
    spec = domain.compile_spec(source, register=True)
    try:
        spec.config({'alpha/beta': ()})
    except Exception as e:
        assert type(e) is Error
        assert e.what == 'config-failed'
        assert len(e.errs) == 1
        assert e.errs[0].what == 'template-predicates-unknown'
    else:
        m = "Error not raised"
        raise AssertionError(m)


def test_compile_apply_schemata():

    domain = global_domain.clone()

    massive_source = {
        '.massive': (),
        'mass': {
            '.integer': (),
        },
    }
    domain.compile_schema('.massive', massive_source)

    colorful_source = {
        '.colorful': (),
        'color': {
            '.text': (),
        },
    }
    domain.compile_schema('.colorful', colorful_source)

    stone_source = {
        '.colorful': (),
        '.massive': (),
    }

    stone_spec = domain.compile_spec(stone_source)

    assert stone_spec[('color',)] == ANY
    assert stone_spec[('mass',)] == ANY

    dry_stone_spec = test_domain.compile_spec(stone_source)
    assert dry_stone_spec[('color')] == NULL
    assert dry_stone_spec[('mass')] == NULL


def test_compile_dependencies():

    domain = Spec()

    painted_source = {
        '.painted': (),
        'color': (),
    }
    domain.compile_schema('.painted', painted_source)

    painted_material_source = {
        '.painted.material': (),
        'material': (),
        'density': (),
    }
    domain.compile_schema('.painted.material', painted_material_source)

    spec_source = {
        'wall': {
            '.painted.material': (),
        },
    }

    spec = domain.compile_spec(spec_source)

    assert spec[('wall', 'material')] == ANY
    assert spec[('wall', 'density')] == ANY
    assert spec[('wall', 'color')] == ANY
    assert spec[('wall', '.', 'painted',)] == ANY
    assert spec[('wall', '.', 'painted', 'material')] == ANY


def test_phantom_predicate():
    domain = Spec()
    phantom_source = {
        'alpha': (),
        'beta': (),
    }
    phantom_spec = domain.compile_spec(phantom_source)
    domain.schemata[('phantom',)] = phantom_spec

    unsuspecting_source = {
        '.phantom': (),
    }

    unsuspecting_spec = domain.compile_spec(unsuspecting_source)


def test_compile_simple_nodes_values():
    source = {
        'hello': {
            'world': {
                '=': {'one': 1},
            },
            'there': {
                'one': 1,
            },
            'you': {
                '=': (1, 2, 3),
            },
        },
    }
    spec = test_domain.compile_spec(source)
    assert spec[('hello', 'world')] == {'one': 1}
    assert spec[('hello', 'there', 'one')] == 1
    assert spec[('hello', 'you')] == (1, 2, 3)


def test_constructor_output():
    predicates_source = [
        ('.alpha', {'.alpha': ()}),
        ('.beta', {'.beta': ()}),
    ]

    domain = Spec()
    domain.compile_schemata(predicates_source)

    @make_constructor
    def construct_alpha(value, output):
        if output is NULL:
            output = int(value)
        else:
            output += 1
        return output

    @make_constructor
    def construct_beta(value, output):
        if output is not NULL:
            output += 2
        return output

    @make_constructor
    def construct_gamma(global_artifacts, loc, value):
        if 'hello_construction' not in global_artifacts:
            output = value
        else:
            output = global_artifacts['hello_construction'][loc]
        return output

    domain.constructions['world_construction'] = {
        '.gamma': construct_gamma,
    }

    domain.constructions['hello_construction'] = {
        '.alpha': construct_alpha,
        '.beta': construct_beta,
    }

    source = {
        'hello': {
            'there': {
                '=': 1,
                '.alpha': (),
                '.beta': (),
                '.gamma': (),
            },
        },
    }

    spec = domain.compile_spec(source)

    to_construct = ('world_construction', 'hello_construction')

    artifacts = spec.construct(constructibles=to_construct)
    assert artifacts['hello_construction'][('hello', 'there')] == 3
    assert artifacts['world_construction'][('hello', 'there')] == 1

    spec.construct(artifacts=artifacts, constructibles=to_construct)
    assert artifacts['hello_construction'][('hello', 'there')] == 6
    assert artifacts['world_construction'][('hello', 'there')] == 3


def test_constructor_error():
    predicates_source = [
        ('.one', ()),
        ('.two', ()),
    ]

    domain = Spec()
    domain.compile_schemata(predicates_source)

    @make_constructor
    def construct_one():
        raise Error(what='one-error')

    @make_constructor
    def construct_two():
        raise Error(what='two-error')

    domain.constructions['base'] = {
        '.one': construct_one,
        '.two': construct_two,
    }

    source = {
        '.one': (),
        '.two': (),
    }
    spec = domain.compile_spec(source)

    try:
        spec.construct()
    except Exception as e:
        assert type(e) is Error
        assert e.what == 'construction-failed'
        assert len(e.errs) == 2
        assert e.errs[0].what == 'one-error'
        assert e.errs[1].what == 'two-error'
    else:
        m = "Error not raised"
        raise AssertionError(m)


def test_construct_defer_skip():
    predicates_source = [
        ('.one', ()),
        ('.two', ()),
        ('.three', ()),
        ('.four', ()),
    ]

    domain = Spec()
    domain.compile_schemata(predicates_source)

    @make_constructor
    def construct_one(context, output):
        construct_last(context)
        return output + '1'

    @make_constructor
    def construct_two(output):
        return output + '2'

    @make_constructor
    def construct_three(context, output):
        construct_after(context, '.two')
        return output + '3'

    @make_constructor
    def construct_four(value):
        construct_skip_no_value(value)

    domain.constructions['base'] = {
        '.one': construct_one,
        '.two': construct_two,
        '.three': construct_three,
        '.four': construct_four,
    }

    source = {
        '.one': (),
        '.two': (),
        '.three': (),
        '.four': (),
    }
    spec = domain.compile_spec(source)

    artifacts = {}
    artifacts['base'] = {
        (): '',
    }

    spec.construct(artifacts=artifacts)

    assert artifacts['base'][()] == '231'
    assert artifacts['base#skipped'] == {(): {'.four'}}


def test_construct_deadlock():

    spec = Spec()

    predicates_source = [
        ('.one', ()),
        ('.two', ()),
    ]

    spec.compile_schemata(predicates_source)

    @make_constructor
    def construct_one(context):
        construct_last(context)
        return 1

    @make_constructor
    def construct_two(context):
        construct_last(context)
        return 2

    spec.constructions['base'] = {
        '.one': construct_one,
        '.two': construct_two,
    }

    source = {
        '.one': (),
        '.two': (),
    }
    spec.compile(source)

    try:
        spec.construct()
    except Exception as e:
        assert type(e) is TypeError
        assert 'deadlock' in e.message
    else:
        m = "TypeError not raised"
        raise AssertionError(m)


def test_error():
    def erroneous_function():
        raise Error(what='error-test', message='oops',
                    loc=('am', 'here'), one=1, two=2)

    try:
        erroneous_function()
    except Error as e:
        assert e.what == 'error-test'
        assert e.kwargs == {'one': 1, 'two': 2}
        assert e.loc == ('am', 'here')
        assert e.message == 'oops'
        assert 'erroneous_function' in e.codeloc
        assert len(e.errs) == 0
        e_repr = repr(e)
        from ast import literal_eval
        e_instance = literal_eval(e_repr)
        assert e_instance['Code'] == e.codeloc
        assert e_instance['What'] == e.what
        assert e_instance['Location'] == e.loc
        assert e_instance['Message'] == e.message
        assert len(e_instance['Errors']) == len(e.errs)
        assert e_instance['one'] == 1
        assert e_instance['two'] == 2


def test_compile_empty_key():
    source = {
        'one': {
            '/': 1,
        },
        'two': {
            '': 2,
        },
        'three': {
            '': {
                'four': 4,
                '': {
                    'five': 5,
                    '': {
                        'six': 6,
                    },
                },
            },
        },
    }
    spec = test_domain.compile_spec(source)
    assert spec[('one', '')] == 1
    assert spec[('two',)] == 2
    assert spec[('three', 'four')] == 4
    assert spec[('three', 'five')] == 5
    assert spec[('three', 'six')] == 6


def test_really_empty():
    source = {
        'hello': {
              '': {},
        },
    }
    spec = test_domain.compile_spec(source)
    assert not spec.getpath('hello')


def test_compile_extend_deps():
    predicates_source = [
        (
            '.thing',
            {
                '.thing': (),
                'properties': {
                    '?': ANY,
                },
                'something': (),
            }
        ),
        (
            '.colored',
            {
                '.colored': (),
                '.thing': (),
                'properties': {
                    'color': (),
                    'reflectivity': (),
                },
                'something': (),
            },
        ),
        (
            '.massive',
            {
                '.massive': (),
                '.thing': (),
                'properties': {
                    'mass': (),
                    'strength': (),
                },
            },
        ),
        (
            '.paint',
            {
                '.paint': (),
                '.colored': (),
                '.massive': (),
                'properties': {
                    'color': {
                        'cmyk': (),
                    },
                    'mass': {
                        'per_volume': (),
                    },
                },
            },
        ),
    ]

    domain = Spec()
    domain.compile_schemata(predicates_source)
    paint_spec = domain.get_schema('.paint')
    assert paint_spec[('properties', 'color', 'cmyk')] == ANY
    assert paint_spec[('properties', 'reflectivity')] == ANY
    assert paint_spec[('properties', 'mass', 'per_volume')] == ANY
    assert paint_spec[('properties', 'strength')] == ANY


def test_compile_node_literals():
    sources = [
        (
            '.alpha',
            {
                '.alpha': (),
                'thing': 1,
                'entity': (),
            },
        ),
        (
            '.beta',
            {
                '.beta': (),
                '.alpha': (),
                'thing': 1,
                'entity': 2,
            },
        ),
    ]
    spec = Spec()
    spec.compile_schemata(sources)
    source = {
        '.beta': (),
    }
    spec.compile(source)
    assert spec['thing'] == 1
    assert spec['entity'] == 2


def test_config_basic():
    stone_spec = test_domain.compile_spec({'.stone': ()})
    stone_spec.config({
        '.massive': (),
        'mass': {
            '.integer': (),
        },
    })

    stone_spec.config({
        '.colorful': (),
        'color': {
            '.text': (),
        },
    })

    stone_spec.config({
        'mass/measure': {
            '.text': (),
        },
    })

    stone_spec.config({
        'color': 'black',
        'mass': 9,
    })

    assert stone_spec[('mass', 'measure')] is ANY
    assert stone_spec[('color',)] == 'black'
    assert stone_spec[('mass',)] == 9

    try:
        stone_spec.config({
            'color/rgb': {
                '.text': (),
            },
        })
    except Error as e:
        assert e.what == 'config-failed'
        assert len(e.errs) == 1 and e.errs[0].what == 'immutable-key'

    stone_spec.config({
        'mass': 9,
    })
    assert stone_spec[('mass',)] == 9

    try:
        stone_spec.config({
            'mass': 0,
        })
    except Error as e:
        assert e.what == 'config-failed'
        assert len(e.errs) == 1 and e.errs[0].what == 'value-mismatch'

    try:
        stone_spec.config({
            'mass/measure': "oz",
        })
    except Error as e:
        assert e.what == 'config-failed'
        assert (
            len(e.errs) == 1 and
            e.errs[0].loc == ('mass', 'measure') and
            e.errs[0].what == 'immutable-value'
        )


def test_clone_empty():
    spec = Spec()
    cloned = spec.clone()
    assert cloned.nodes is ()
    assert cloned.value is ANY


def test_config_existing_value():
    source = {
        'alpha': 1,
    }
    spec = test_domain.compile_spec(source)
    spec.config({'alpha': 1})
    assert spec.getpath('alpha') == 1

    try:
        spec.config({'alpha': 2})
    except Exception as e:
        assert type(e) is Error
        assert e.what == 'config-failed'
        assert len(e.errs) == 1
        assert e.errs[0].what == 'value-mismatch'


def test_config_specify_value():
    source = {
        'alpha': (),
    }
    spec = test_domain.compile_spec(source)
    spec.config({'alpha': 1})
    assert spec.nodes['alpha'] == 1
    orig_items = spec.items()
    errs = []
    spec.config_value(ANY, errs=errs, mutable=True)
    assert not errs
    new_items = spec.items()
    assert new_items == orig_items


def test_extract_settings_deep():
    source = {
        'top': {
            'middle': {
                'bottom': (),
                ':bottom_setting_a': 5,
                ':bottom_setting_b': 6,
            },
            ':middle_setting_a': 3,
            ':middle_setting_b': 4,
        },
        ':top_setting_a': 1,
        ':top_setting_b': 2,
    }
    spec = test_domain.compile_spec(source)
    settings = spec.extract_settings()
    assert settings[':top_setting_a'] == 1
    assert settings[':top_setting_b'] == 2
    assert settings['top'][':middle_setting_a'] == 3
    assert settings['top'][':middle_setting_b'] == 4
    assert settings['top']['middle'][':bottom_setting_a'] == 5
    assert settings['top']['middle'][':bottom_setting_b'] == 6


def test_extract_settings_any():
    source = {
        'alpha': {
            ':set_alpha': (),
            'beta': {
                ':set_alpha': (),
            },
            'gamma': {
                ':set_gamma': (),
                ':set_alpha': 1,
                'delta': {
                    ':set_gamma': 3,
                    ':set_alpha': (),
                },
            },
            'epsilon': {
                'zetta': {
                    ':set_alpha': (),
                },
            },
        },
    }
    spec = test_domain.compile_spec(source)
    settings = spec.extract_settings()
    assert settings['alpha'][':set_alpha'] == ANY
    assert settings['alpha']['beta'][':set_alpha'] == ANY
    assert settings['alpha']['gamma'][':set_alpha'] == 1
    assert settings['alpha']['gamma']['delta'][':set_alpha'] == 1
    assert settings['alpha']['epsilon']['zetta'][':set_alpha'] == ANY
    assert settings['alpha']['gamma'][':set_gamma'] == ANY
    assert settings['alpha']['gamma']['delta'][':set_gamma'] == 3


def test_extract_settings_empty_parent():
    source = {
        'top': {
            'nothing': (),
        },
        'hello': {
            'world': {
                ':there': 9,
            },
        },
    }
    spec = test_domain.compile_spec(source)
    settings = spec.extract_settings()
    assert settings['hello']['world'][':there'] == 9


def test_extract_settings_inheritance():
    source = {
        'alpha': {
            ':alpha_setting': 1,
            'beta': {
                'gamma': {
                    ':alpha_setting': (),
                },
                ':alpha_setting': {
                    'foo': (),
                },
            },
            'delta': {
                ':alpha_setting': 2,
                'epsilon': {
                    ':alpha_setting': (),
                },
            },
        },
    }
    spec = test_domain.compile_spec(source)
    settings = spec.extract_settings()
    assert settings['alpha']['beta'][':alpha_setting'] == 1
    assert settings['alpha']['beta']['gamma'][':alpha_setting'] == 1
    assert settings['alpha']['delta'][':alpha_setting'] == 2
    assert settings['alpha']['delta']['epsilon'][':alpha_setting'] == 2


def test_extract_settings_subspec():
    source = {
        ':alpha': {
            '=': 1,
            'one': (),
        },
        ':beta': {
            'two': 2,
        },
        'hello': {
            ':alpha': (),
            ':beta': (),
        },
    }
    spec = test_domain.compile_spec(source)
    settings = spec.extract_settings()
    assert settings[':alpha'] == 1
    assert settings['hello'][':alpha'] == 1
    assert settings[':beta'] == ANY
    assert settings['hello'][':beta'] == ANY


def test_getpath():
    source = {
        'one': {
            'two': 2,
            'three': (),
        },
    }
    spec = test_domain.compile_spec(source)
    assert spec.getpath(('one',))[('two',)] == 2
    assert spec.getpath(('one',))[('three',)] is ANY
    assert spec.getpath(('one', 'two')) == 2
    assert spec.getpath(('one', 'three')) == ANY
    assert spec.getpath(('one', 'alpha')) is NULL
    assert spec.getpath(('one', 'two', 'alpha')) is NULL
    assert spec.getpath(('one', 'three', 'alpha')) is NULL


def test_spec_as_mapping():
    source = {
        'one': {
            'two': 2,
            'three': (),
        },
    }
    spec = test_domain.compile_spec(source)
    assert len(spec) == 1
    assert ('one', 'four') not in spec
    assert ('one', 'two') in spec
    assert ('one', 'three') in spec
    assert spec.keys() == [(), ('one',), ('one', 'three'), ('one', 'two')]
    assert zip(spec.keys(), spec.values()) == spec.items()
    assert list(spec) == spec.keys()


def test_getval():
    source = {
        'one': {
            '=': 1,
            'two': {
                '=': 2,
                'three': 3,
            },
        },
        'alpha': {
            'beta': (),
        },
    }
    spec = test_domain.compile_spec(source)
    assert spec[()] == ANY
    assert spec[('one',)] == 1
    assert spec[('one', 'two')] == 2
    assert spec[('one', 'two', 'three')] == 3
    assert spec[('alpha',)] == ANY
    assert spec[('alpha', 'beta')] == ANY
    assert spec[('alpha', 'gamma')] == NULL

    assert getval(spec, ('alpha', 'beta'), default=7) == 7
    assert getval(spec, ('alpha', 'gamma'), missing=9) == 9
    assert getval(spec, (), default=7, missing=9) == 7
    assert getval(spec, ('one', 'alpha'), default=7, missing=9) == 9
    assert getval(spec, ('one', 'two'), default=7, missing=9) == 2


def test_setval():
    spec = Spec()
    spec['one/two/three'] = 1
    spec['one?alpha?beta'] = 2
    spec.setval('one.a.b', 3)
    assert spec['one/two/three'] == 1
    assert spec['one?alpha?beta'] == 2
    assert spec['one.a.b'] == 3


def test_iter_level_values():
    source = {
        'alpha': 1,
        'beta': (),
        'camma': {
            '=': 3,
            'one': 1,
        },
        'delta': {
            'two': 2,
        },
    }
    spec = test_domain.compile_spec(source)
    assert tuple(spec.iter_level_values()) == (
        ('alpha', 1),
        ('beta', ANY),
        ('camma', 3),
        ('delta', ANY),
    )


def test_iterall():
    source = {
        'a': {
            'b': {
                '=': 2,
                'c': 3,
            },
        },
        '?': {
            'b': {
                '=': 'beta',
                'c': 'gamma',
            },
            'c': 9,
        },
        '.': {
            'a': {
                '=': 1,
            },
            'b': (),
            'c': {
                'd': (),
                'e': 5,
            },
        },
    }

    spec = test_domain.compile_spec(source)

    assert all(
        a == b
        for a, b in
        zip(
            spec.iterall(what='/'),
            spec.iterall(what='/', preorder=False, postorder=True),
        )
    )

    assert tuple(spec.iterall(what='/', preorder=False, postorder=True)) == (
        (('a', 'b', 'c'), 3),
        (('a', 'b'), spec.nodes['a'].nodes['b']),
        (('a',), spec.nodes['a']),
        ((), spec),
    )

    assert tuple(spec.iterall(what='/', preorder=True, postorder=False)) == (
        ((), spec),
        (('a',), spec.nodes['a']),
        (('a', 'b'), spec.nodes['a'].nodes['b']),
        (('a', 'b', 'c'), 3),
    )

    expected = (
        ((), spec),
        (('a',), spec.nodes['a']),
        (('a', 'b'), spec.nodes['a'].nodes['b']),
        (('a', 'b', 'c'), 3),
        (('a', 'b'), spec.nodes['a'].nodes['b']),
        (('a',), spec.nodes['a']),
        ((), spec),
    )
    reported = tuple(spec.iterall(what='/', preorder=True, postorder=True))
    assert reported == expected

    assert tuple(spec.iterall(what='.?=', preorder=1, postorder=0)) == (
        ((), ANY),
        (('.',), ANY),
        (('.', 'a'), 1),
        (('.', 'b'), ANY),
        (('.', 'c'), ANY),
        (('.', 'c', 'd'), ANY),
        (('.', 'c', 'e'), 5),
        (('a',), ANY),
        (('a', 'b'), 2),
        (('a', 'b', 'c'), 3),
        (('?',), ANY),
        (('?', 'b'), 'beta'),
        (('?', 'b', 'c'), 'gamma'),
        (('?', 'c'), 9),
    )

    assert tuple(spec.iterall(what='.=', preorder=1, postorder=0)) == (
        ((), ANY),
        (('.',), ANY),
        (('.', 'a'), 1),
        (('.', 'b'), ANY),
        (('.', 'c'), ANY),
        (('.', 'c', 'd'), ANY),
        (('.', 'c', 'e'), 5),
        (('a',), ANY),
        (('a', 'b'), 2),
        (('a', 'b', 'c'), 3),
    )

    assert tuple(spec.iterall(what='?=', preorder=1, postorder=0)) == (
        ((), ANY),
        (('a',), ANY),
        (('a', 'b'), 2),
        (('a', 'b', 'c'), 3),
        (('?',), ANY),
        (('?', 'b'), 'beta'),
        (('?', 'b', 'c'), 'gamma'),
        (('?', 'c'), 9),
    )

    assert tuple(ANY.iterall(what='/')) == (((), ANY),)


def test_make_constructor_callable():

    class CustomConstructor(object):
        def __call__(self,
                     spec,
                     top_spec,
                     constructions,
                     construction,
                     constructors,
                     value,
                     output,
                     artifacts,
                     settings,
                     dependencies,
                     schemata,
                     constructed,
                     skipped,
                     round,
                     errs,
                     predicate,
                     args,
                     context):
            return 99

    custom_source = [
        (
            '.custom',
            {
                '.custom': (),
            },
        ),
    ]
    domain = Spec()
    domain.compile_schemata(custom_source)

    cc = make_constructor(CustomConstructor())
    assert cc.func_name == 'CustomConstructor'

    domain.constructions['base'] = {
        '.custom': cc,
    }

    source = {
        'alpha': {
            '.custom': (),
        },
    }
    spec = domain.compile_spec(source)
    artifacts = spec.construct()
    assert artifacts['base'][('alpha',)] == 99


def test_make_constructor_context():
    def custom_constructor(context):
        return 1

    cc = make_constructor(custom_constructor)
    assert cc is custom_constructor
    assert custom_constructor(None) == 1


def test_make_constructor_unknown_args():
    def custom_constructor(unknown_arg):
        return 1
    try:
        make_constructor(custom_constructor)
    except Exception as e:
        assert type(e) is Error
        assert e.what == 'invalid'
        assert 'unknown' in e.message
    else:
        m = "Error not raised"
        raise AssertionError(m)

    assert custom_constructor({}) == 1


def test_make_constructor_invalid():
    try:
        make_constructor(5)
    except Exception as e:
        assert type(e) is Error
        assert e.what == 'invalid'
        assert '5' in e.message
    else:
        raise AssertionError("Error not raised")


def test_spec_init():
    try:
        Spec(loc=('alphatron', 'betatron'))
    except Exception as e:
        assert type(e) is TypeError
        assert 'alphatron' in e.message
        assert 'betatron' in e.message
    else:
        raise AssertionError("TypeError not raised")

    try:
        Spec(top=9, loc=('gammatron', 'deltatron'))
    except Exception as e:
        assert type(e) is TypeError
        assert 'gammatron' in e.message
        assert 'deltatron' in e.message
    else:
        raise AssertionError("TypeError not raised")

    try:
        Spec(top='boo', loc=())
    except Exception as e:
        assert type(e) is TypeError
        assert 'root' in e.message
    else:
        raise AssertionError("TypeError not raised")

    topspec = Spec()
    spec = Spec(top=topspec, loc=())
    assert spec.top is topspec.top


def test_spec_basic():

    predicate_sources = [
        (
            '.integer',
            {
                '.integer': (),
                'min': (),
                'max': (),
            },
        ),
        (
            '.text',
            {
                '.text': (),
                'minlen': (),
                'maxlen': (),
            },
        ),
        (
            '.error',
            {
                '.error': (),
            },
        ),
    ]

    domain = Spec()
    domain.compile_schemata(predicate_sources)

    error_source = {
        '.error': (),
        'code': (),
        'message': {
            '.text': (),
        },
        'codeloc': {
            'file': {
                '.text': (),
            },
            'function': {
                '.text': (),
            },
            'lineno': {
                '.integer': (),
                'min': 0,
            },
        },
        'data': (),
        '?': 1,
    }
    domain.compile_schema('.error', error_source)

    errors_source = {
        'errors': {
            '?': {
                '.error': (),
            },
        },
    }
    errors_spec = domain.compile_spec(errors_source)

    source = {
        'errors': {
            'conflicterror': {
                'message': 'action requested conflicts with current state',
                'codeloc': {
                    'lineno': '42',
                    'file': 'boo',
                    'function': 'do_it()',
                },
                'data': {
                    'newstate': 9,
                },
            },
        },
    }

    errors_spec.config(source)
    errors_spec.construct()


def test_fields():
    flag_spec = {
        '.flag': ()
    }

    field_spec = {
        '.field': (),
        'source': {'.string': ()},
        'default': (),
        '.flag': (),
    }

    field_string_spec = {
        '.field': {
            'string': ()
        },
        'default': {'.string': ()},
    }

    domain = Spec()
    domain.compile_schema('.flag', flag_spec)
    domain.compile_schema('.field', field_spec)
    domain.compile_schema('.field.string', field_string_spec)
    assert 'source' in domain.getpath('$/.field.string').nodes


def test_spec_test():

    source = {
        '.hello': {
            'friend': 6,
        },
        'hello.there': {
            '.nine': (),
            'ten': (),
        },
        'one': {
            '2two': 2,
            '@three': 3,
            '?': {'foo': 5},
        },
        'four': 4,
        'five': {
            '=': 5,
            'someting': (),
        },
        'six': Data({'one': 1}),
    }

    spec = test_domain.compile_spec(source)
    import ast
    spec_repr = repr(spec).replace('ANY', '()')
    uncompiled_source = normalize_source(ast.literal_eval(spec_repr))
    assert normalize_source(source) == uncompiled_source

    spec.config({'?': {'foo': {'bar': 4}}})
    spec.config({'zoo': {'moo': {'=': 1}}})
    spec.config({'?': {'=': 9}})
    try:
        spec.config({'goo': {'daz': 11}})
    except Error as e:
        assert e.what == 'config-failed'
    spec.config({'zoo': {'foo': ()}})
    spec.config({'zoo': {'foo': {'a': 1}}})
    spec.config({'zoo': 0})
    try:
        spec.config({'zoo': {'foo': {'b': 2}}})
    except Error as e:
        assert e.what == 'config-failed'
        assert e.errs and e.errs[0].what == 'immutable-key'
    try:
        spec.config({'zoo': {'foo': 3}})
    except Error as e:
        assert e.what == 'config-failed'
        assert e.errs and e.errs[0].what == 'immutable-value'

    spec.config({'six': {'=': {'one': 1}}})


def test_spec_properties():
    source = {
        '.': {
            'one': (),
            'two': (),
        },
        '?': {
            'alpha': (),
            'beta': (),
        },
    }
    spec = test_domain.compile_spec(source)
    assert spec.predicates is spec.nodes[b'.']
    assert spec.template is spec.nodes[b'?']
    pp = spec.nodes.pop(b'.')
    assert spec.predicates is NULL
    tt = spec.nodes.pop(b'?')
    assert spec.template is NULL
    spec.predicates = pp
    assert spec.predicates is pp
    del spec.nodes[b'.']
    spec.template = tt
    assert spec.template is tt
    spec.nodes = ()
    assert spec.template is NULL
    assert spec.predicates is NULL


def test_data():
    data = Data(True)
    assert data.value is True
    assert repr(data) == 'Data(True)'


def test_construct_integer():

    source = {
        'alpha': {
            '.integer': {
                'min': 3,
                'max': 4,
            },
        },
    }
    domain = global_domain.clone()
    spec = domain.compile_spec(source)

    randomized_spec = spec.clone()
    randomized_spec.config({'alpha.integer.randomize': 1})
    for _ in range(10):
        artifacts = randomized_spec.construct()
        output = artifacts['base'][('alpha',)] 
        assert 3 <= output <= 4

    for val in (2, 5, '10', 'ab', None):
        invalid_spec = spec.clone()
        invalid_spec.config({'alpha': val})
        try:
            invalid_spec.construct()
        except Exception as e:
            assert type(e) is Error
            assert e.what == 'construction-failed'
            assert len(e.errs) == 1
            assert e.errs[0].what == 'invalid'
        else:
            m = "Error not raised"
            raise AssertionError(m)

    valid_spec = spec.clone()
    valid_spec.config({'alpha': 3})
    artifacts = valid_spec.construct()
    assert artifacts['base'][('alpha',)] == 3

    skip_spec = domain.compile_spec({'.integer': ()})
    skip_spec.construct()
    

def test_construct_text():

    source = {
        'alpha': {
            '.text': {
                'minlen': 33,
                'maxlen': 34,
            },
        },
    }

    domain = global_domain.clone()
    spec = domain.compile_spec(source)

    randomized_spec = spec.clone()
    randomized_spec.config({'alpha.text.randomize': 1})
    artifacts = randomized_spec.construct()
    output = artifacts['base'][('alpha',)]
    assert 33 <= len(output) <= 34

    randomized_spec.config({'alpha.text.alphabet': 'xyz'})
    artifacts = randomized_spec.construct()
    output = artifacts['base'][('alpha',)]
    assert not output.replace('x', '').replace('y', '').replace('z', '')

    randomized_spec.config({'alpha.text.excluded': 'yz'})
    artifacts = randomized_spec.construct()
    output = artifacts['base'][('alpha',)]
    assert not output.replace('x', '')

    randomized_spec.config({'alpha.text.regex': '[abc]'})
    try:
        randomized_spec.construct()
    except Exception as e:
        assert type(e) is Error
        assert e.what == 'construction-failed'
        assert len(e.errs) == 1
        assert e.errs[0].what == 'unsupported'
    else:
        m = "Error not raised"
        raise AssertionError(m)

    utf_source = {
        'alpha': {
            '=': u'Καλημέρα'.encode('utf-8'),
            '.text.encoding': 'utf-8',
        },
    }
    utf_spec = domain.compile_spec(utf_source)
    artifacts = utf_spec.construct()
    output = artifacts['base'][('alpha',)]
    assert type(output) == unicode
    assert output == u'Καλημέρα'

    base_source = {
        'alpha': {
            '.text': (),
        },
    }
    base_spec = domain.compile_spec(base_source)
    for invalid_config in [
        {
            'alpha': 1,
        },
        {
            'alpha': 'abcd',
            'alpha.text.minlen': 5,
        },
        {
            'alpha': 'abcd',
            'alpha.text.maxlen': 3,
        },
        {
            'alpha': 'abcd',
            'alpha.text.regex': '^[abc]*$',
        },
        {
            'alpha': 'abcd',
            'alpha.text.alphabet': 'abc',
        },
        {
            'alpha': 'abcd',
            'alpha.text.excluded': 'bd',
        },
    ]:
        invalid_spec = base_spec.clone()
        invalid_spec.config(invalid_config)
        try:
            invalid_spec.construct()
        except Exception as e:
            assert type(e) is Error
            assert e.what == 'construction-failed'
            assert len(e.errs) == 1
            assert e.errs[0].what == 'invalid'
        else:
            m = "Error not raised"
            raise AssertionError(m)

    valid_source = {
            'alpha': 'abcd',
            'alpha.text.minlen': 3,
            'alpha.text.maxlen': 4,
            'alpha.text.regex': '^[abcde]*$',
            'alpha.text.alphabet': 'abcde',
            'alpha.text.excluded': 'xyz',
    }
    valid_spec = domain.compile_spec(valid_source)
    output = valid_spec.construct()['base'][('alpha',)]
    assert output == 'abcd'

    skip_spec = domain.compile_spec({'.text': ()})
    skip_spec.construct()


def test_construct_object():
    domain = global_domain.clone()
    for invalid_source in [
        {
            'alpha': {
                '.object': (),
                'class': 'this_path_must.not:exist',
            },
        },
        {
            'alpha': {
                '.object': (),
                'class': 'collections:this_collection_must_exist',
            },
        },
        {
            'alpha': {
                '=': 1,
                '.object': (),
                'class': 'types:BooleanType',
            },
        },
        {
            'alpha': {
                '.object': (),
                'class': 'types:IntType',
                'args': {
                    'x': 'abc',
                },
            },
        },
    ]:
        invalid_spec = domain.compile_spec(invalid_source)
        try:
            invalid_spec.construct()
        except Exception as e:
            assert type(e) is Error
            assert e.what == 'construction-failed'
            assert len(e.errs) == 1
            assert e.errs[0].what == 'invalid'
        else:
            m = "Error not raised"
            raise AssertionError(m)

    valid_source = {
        'alpha': {
            '.object': (),
            'class': 'types:IntType',
            'args': {
                'x': '99',
            },
        },
    }
    valid_spec = domain.compile_spec(valid_source)
    artifacts = valid_spec.construct()
    output = artifacts['base'][('alpha',)]
    assert output == 99


def test_recursion():
    tree_source = {
        '.tree': (),
        'value': (),
        'nodes': {
            '?': {
                '.tree': (),
            },
        },
    }
    tree_domain = Spec()
    tree_domain.compile_schema('.tree', tree_source)
    tree_spec = tree_domain.compile_spec({'.tree': ()})
    tree_spec.config({'nodes/alpha': ()})
    tree_spec.config({'nodes/alpha/nodes/beta': ()})
    tree_spec.config({'nodes/gamma': ()})
    tree_spec.config({'nodes/gamma/nodes/delta': ()})

    assert tree_spec[('nodes', 'alpha', '.', 'tree')] == ANY
    assert tree_spec[('nodes', 'alpha', 'nodes', 'beta', '.', 'tree')] == ANY
    assert tree_spec[('nodes', 'gamma', '.', 'tree')] == ANY
    assert tree_spec[('nodes', 'gamma', 'nodes', 'delta', '.', 'tree')] == ANY
    assert tree_spec[('nodes', 'delta', '.', 'tree')] == NULL


def test_specular_demo():

    demo_domain = global_domain.clone()

    expression_source = {
        '.expression': (),
        'operator': (),
        'terms': {
            '?': {
                '.expression': (),
            },
        },
    }

    # register .expression predicate schema
    demo_domain.compile_schema('.expression', expression_source)

    demo_source = {
        'demo': {
            '.expression': (),
            'operator': {
                '.text': {
                    'minlen': 1,
                    'maxlen': 1,
                    'alphabet': '+*',
                },
            },
        },
    }

    base_constructions = demo_domain.constructions['base']
    demo_domain.constructions['eval'] = dict(base_constructions)
    demo_domain.constructions['repr'] = dict(base_constructions)

    @make_constructor
    def construct_eval_expression(spec, loc, value, artifacts):
        if spec.value is not ANY:
            raise SkipConstructor()

        termspec = spec.nodes['terms']
        termloc = loc + ('terms',)
        values = []
        for key, val in termspec.iter_level_values():
            if val is ANY:
                subloc = termloc + (key,)
                if subloc in artifacts:
                    val = artifacts[subloc]
            values.append(val)

        op = spec['operator']
        if op == '+':
            output = sum(values)
        elif op == '*':
            output = reduce(lambda a, b: a * b, values, 1)
        else:
            raise Error(what='invalid', loc=loc)

        return output


    demo_domain.constructions['eval'].update({
        '.expression': construct_eval_expression,
    })

    @make_constructor
    def construct_repr_expression(spec, value, artifacts):
        if spec.value is not ANY:
            return str(spec.value)

        op = spec['operator']
        termspec = spec.getpath('terms')
        output = '('
        output += op.join(
            v for p, v in termspec.iter_level_outputs(artifacts)
        )
        output += ')'
        return output

    demo_domain.constructions['repr'].update({
        '.expression': construct_repr_expression,
    })

    demo_spec = demo_domain.compile_spec(demo_source)

    demo_config = {
        'demo': {
            'operator': '+',
            'terms': [
                1,
                2,
                3,
                {
                    'operator': '*',
                    'terms': [3, 5, 7],
                },
                {
                    'operator': '*',
                    'terms': [
                        {
                            'operator': '+',
                            'terms': [1, 5, 9],
                        },
                        6,
                        8,
                    ],
                    'foo': 9,
                },
            ],
        },
    }
    demo_spec.config(demo_config)

    artifacts = demo_spec.construct()
    eval_result = 1 + 2 + 3 + (3 * 5 * 7) + ((1 + 5 + 9) * 6 * 8)
    assert artifacts['eval'][('demo',)] == eval_result
    repr_result = artifacts['repr'][('demo',)]
    import re
    assert re.match('^[(0-9)+*]*$', repr_result)
    assert eval(repr_result) == eval_result


def test_schema_extension():

    domain = Spec()

    style_sources = [
        (
            '.style',
            {
                'background': (),
                'text': (),
                'border': (),
            },
        ),
        (
            '.style.bar',
            {
                'menu': (),
            },
        ),
        (
            '.style.frame',
            {
                'content': (),
            },
        ),
    ]

    domain.compile_schemata(style_sources)

    page_source = {
        '?': {
            'header': (),
            'body': (),
            'footer': (),
        },
    }

    page_spec = domain.compile_spec(page_source)

    page_config = {
        '?': {
            'header': {
                '.style.bar': (),
            },
            'body': {
                '.style.frame': (),
                'dialog': {
                    '.style.frame': (),
                },
            },
            'footer': {
                '.style.bar': (),
            },
        },
    }

    page_spec.config(page_config)

    test_page_config = {
        'test_page': {
            'body': {
                'content': 'test',
            },
        },
    }

    page_spec.config(test_page_config)

    style_bar_spec = domain.get_schema('.style.bar')

    bar_spec_extension = {
        'background': 'deepblue',
        'text': 'white',
    }

    style_bar_spec.config(bar_spec_extension)

    style_frame_spec = domain.get_schema('.style.frame')

    frame_spec_extension = {
        'background': 'darkgray',
        'text': 'white',
    }

    style_frame_spec.config(frame_spec_extension)

    landing_page_config = {
        'landing': {
            'header': {
                'menu': ['account', 'navigate'],
            },
            'body': {
                'content': 'Welcome',
            },
            'footer': {
                'menu': ['contact', 'settings'],
            },
        },
    }

    page_spec.config(landing_page_config)

    assert page_spec['landing/body/background'] == 'darkgray'
    assert page_spec['landing/body/background'] == 'darkgray'
    assert page_spec['landing/header/background'] == 'deepblue'
    assert page_spec['landing/footer/background'] == 'deepblue'


def test_runtime():
    try:
        Runtime(1)
    except Exception as e:
        assert type(e) is TypeError
    else:
        m = "TypeError not raised"
        raise AssertionError(m)


    source = {
        'alpha': {
            '.alpha': (),
            'one': (),
            'two': {
                '.two': (),
                'x': (),
                'y': 1,
                'z': {
                    'foo': 9,
                },
            },
            'three': (),
        },
    }

    domain = Spec()
    spec = domain.compile_spec(source)

    runtime = Runtime(spec)

    assert 'alpha/two/y' in runtime
    assert runtime['alpha/two/y'] == 1
    assert 'alpha/two/z' in runtime
    assert runtime['alpha/two/z'] is ANY
    assert runtime['alpha/two/z/foo'] == 9
    assert runtime['alpha/two/w'] is NULL
    assert 'alpha/two/w' not in runtime
    assert runtime['alpha/./alpha'] is NULL
    runtime['alpha/three'] = 3
    assert runtime['alpha/three'] == 3
    assert len(runtime) == len(runtime.values())
    assert runtime.keys() == list(runtime) == list(runtime.iterkeys())
    assert runtime.items() == zip(runtime.iterkeys(), runtime.itervalues())

    try:
        runtime['non/existent'] = 1
    except Exception as e:
        assert type(e) is Error
        assert e.what == 'not-found'
    else:
        raise AssertionError("Error not raised")

    @Processor.make()
    def example_proc1():
        return 1

    assert type(example_proc1) is Processor

    proc_name = 'foo_proc'
    proc_reads = ('alpha/one', 'alpha/two')
    proc_writes = ('alpha/two', 'alpha/three')
    @Processor.make(name=proc_name, reads=proc_reads, writes=proc_writes)
    def example_proc2():
        return 2

    assert type(example_proc2) is Processor
    assert example_proc2.name == proc_name
    assert example_proc2.reads == frozenset(proc_reads)
    assert example_proc2.writes == frozenset(proc_writes)

    runtime.add_processor(example_proc2)
    assert proc_name in runtime.reader_index['alpha/one']
    assert proc_name in runtime.reader_index['alpha/two']
    assert proc_name in runtime.writer_index['alpha/two']
    assert proc_name in runtime.writer_index['alpha/three']

    assert runtime.getlevel('alpha/two') == {
        'x': ANY,
        'y': 1,
        'z': ANY,
    }
    assert runtime.getlevel('alpha/two/x') == {}
    assert runtime.getlevel('alpha/two/y') == {'': 1}

    try:
        runtime.getlevel('non/existent')
    except Exception as e:
        assert type(e) is Error
        assert e.what == 'not-found'
    else:
        raise AssertionError("Error not raised")

    assert runtime.getpath('alpha/two') == {
        '': ANY,
        'x': ANY,
        'y': 1,
        'z': ANY,
        'z/foo': 9,
    }
    assert runtime.getpath('alpha/two/x') == {}
    assert runtime.getpath('alpha/two/y') == {'': 1}
    try:
        runtime.getpath('non/existent')
    except Exception as e:
        assert type(e) is Error
        assert e.what == 'not-found'
    else:
        raise AssertionError("Error not raised")


def test_runtime_insert():

    spec = Spec()
    source = {
        'hello': {
            'there': (),
            'world': (),
            'and': {
                'jolly': (),
                'holy': (),
                'people': (),
            },
        },
    }
    spec.compile(source)
    runtime = Runtime(spec)
    data = {
        'there': Data({'one': 1}),
        'world': 2,
        'and': {
            '=': 3,
            'people': 4,
        },
    }
    runtime.insert(data, path='hello', writer='hello')
    assert runtime['hello'] == ANY
    assert runtime['hello/there'] == {'one': 1}
    assert runtime['hello/world'] == 2
    assert runtime['hello/and'] == 3
    assert runtime['hello/and/jolly'] == ANY
    assert runtime['hello/and/holy'] == ANY
    assert runtime['hello/and/people'] == 4
    assert runtime['hello/foo'] == NULL


def test_runtime_schedule():

    domain = Spec()
    source = {
        'alpha': {
            'one': (),
            'two': (),
            'three': (),
        },
        'beta': {
            'four': (),
            'five': (),
        },
        'gamma/six': {
            'hello': (),
            'there': (),
        },
    }
    spec = domain.compile_spec(source)
    runtime = Runtime(spec)

    results_one = {
        'alpha/one': 1,
        'beta/four': 2,
    }

    @Processor.make(
        name='one',
        reads=('alpha/one', 'beta/five', 'gamma/six'),
        writes=('alpha/one', 'beta/four'),
    )
    def proc_one(data):
        return results_one

    results_two = {
        'alpha': 3,
        'beta': 4,
        'gamma': 5,
    }

    @Processor.make(
        name='two',
        reads=('alpha/three', 'beta', 'gamma/six/hello'),
        writes=('alpha', 'beta', 'gamma/six/there'),
    )
    def proc_two(data):
        assert 'alpha/three' in data
        assert 'beta' in data
        assert 'gamma/six/hello' in data
        return results_two

    @Processor.make(
        name='three',
        reads=(),
        writes=(
            'alpha/one', 'alpha/two', 'alpha/three',
            'beta', 'beta/five',
            'gamma/six', 'gamma/six/hello'
        ),
    )
    def proc_three(data):
        return {}

    @Processor.make(
        name='four',
        reads=('gamma/six/there', 'beta/four'),
        writes=('gamma', 'alpha'),
    )
    def proc_four(data):
        return {}

    runtime.add_processor(proc_one)
    runtime.add_processor(proc_two)
    runtime.add_processor(proc_three)
    runtime.add_processor(proc_four)

    schedule, pending = runtime.get_schedule()
    expected_schedule = ['three', 'one', 'two', 'four']
    assert schedule == expected_schedule
    assert not pending

    results, pending, errs = runtime.process({})
    expected_results = [
        ('three', {}),
        ('one', {}),
        ('two', {'gamma': 5}),
        ('four', {}),
    ]
    assert results == expected_results
    assert not errs
    assert not pending

    runtime.reset()
    try:
        runtime.process_all({})
    except Exception as e:
        assert type(e) is Error
        assert e.what == 'process-unknown-keys'
    else:
        raise AssertionError("Error not raised")

    runtime.reset()
    from cStringIO import StringIO
    io = StringIO()
    runtime.print_out_dot_graph(io)
    expected_dot_output = \
"""digraph {
    node [fontname="Courier"];
    edge [fontname="Courier"];

    "four" [shape=oval]
    "beta/four" [shape=box]
    "beta/four" -> "four"
    "gamma/six/there" [shape=box]
    "gamma/six/there" -> "four"
    "alpha" [shape=box]
    "four" -> "alpha"
    "gamma" [shape=box]
    "four" -> "gamma"
    "one" [shape=oval]
    "alpha/one" [shape=box]
    "alpha/one" -> "one"
    "beta/five" [shape=box]
    "beta/five" -> "one"
    "gamma/six" [shape=box]
    "gamma/six" -> "one"
    "one" -> "alpha/one"
    "one" -> "beta/four"
    "three" [shape=oval]
    "three" -> "gamma/six"
    "gamma/six/hello" [shape=box]
    "three" -> "gamma/six/hello"
    "alpha/two" [shape=box]
    "three" -> "alpha/two"
    "three" -> "alpha/one"
    "beta" [shape=box]
    "three" -> "beta"
    "three" -> "beta/five"
    "alpha/three" [shape=box]
    "three" -> "alpha/three"
    "two" [shape=oval]
    "gamma/six/hello" -> "two"
    "beta" -> "two"
    "alpha/three" -> "two"
    "two" -> "alpha"
    "two" -> "beta"
    "two" -> "gamma/six/there"
}
"""
    assert io.getvalue() == expected_dot_output


def test_runtime_errors():
    @Processor.make(
        reads=(),
        writes=('one', 'two'),
    )
    def alpha(data):
        return {}

    @Processor.make(
        reads=('one', 'five'),
        writes=('three', 'four'),
    )
    def beta(data):
        return {}

    @Processor.make(
        reads=('two', 'three'),
        writes=('five', 'six'),
    )
    def gamma(data):
        return {}

    @Processor.make(
        reads=('seven', 'eight')
    )
    def delta(data):
        pass

    @Processor.make(
        writes=('seven', 'eight')
    )
    def epsilon(data):
        pass

    source = {
        'one': (),
        'two': (),
        'three': (),
        'four': (),
        'five': (),
        'six': (),
    }
    spec = Spec()
    spec.compile(source)

    runtime = Runtime(spec)
    runtime.add_processor(alpha)
    runtime.add_processor(beta)
    runtime.add_processor(gamma)

    try:
        runtime.add_processor(gamma)
    except Exception as e:
        assert type(e) is Error
        assert e.what == 'already'
    else:
        raise AssertionError("Error not raised")

    try:
        runtime.add_processor(delta)
    except Exception as e:
        assert type(e) is Error
        assert e.what == 'no-read-key'
    else:
        raise AssertionError("Error not raised")

    try:
        runtime.add_processor(epsilon)
    except Exception as e:
        assert type(e) is Error
        assert e.what == 'no-write-key'
    else:
        raise AssertionError("Error not raised")

    try:
        runtime.add_processor(1)
    except Exception as e:
        assert type(e) is Error
        assert e.what == 'invalid'
    else:
        raise AssertionError("Error not raised")

    schedule, pending = runtime.get_schedule()
    assert pending

    runtime.reset()
    try:
        runtime.process_all({})
    except Exception as e:
        assert type(e) is Error
        assert e.what == 'process-error'
    else:
        raise AssertionError("Error not raised")


def test_processor_deps():
    source = {
        'one': (),
        'two': (),
        'three': (),
        'four': (),
        'five': (),
        'six': (),
    }
    spec = Spec()
    spec.compile(source)

    runtime = Runtime(spec)

    @Processor.make(
        name='alpha',
        reads=['one'],
        writes=['two'],
    )
    def alpha(data):
        return {'two': 0}

    @Processor.make(
        name='beta',
        reads=['two'],
        writes=['two', 'three'],
    )
    def beta(data):
        return {'two': data['two'] + 1 , 'three': 3}

    @Processor.make(
        name='cee',
        reads=['two'],
        writes=['two', 'four'],
    )
    def cee(data):
        return {'two': data['two'] + 1, 'four': 4}

    @Processor.make(
        name='delta',
        reads=['two', 'three'],
        writes=['five'],
    )
    def delta(data):
        return {'five': 5}

    @Processor.make(
        name='epsilon',
        reads=['three'],
        writes=['six']
    )
    def epsilon(data):
        return {'six': 6}

    runtime.add_processor(delta)
    runtime.add_processor(epsilon)
    runtime.add_processor(beta)
    runtime.add_processor(cee)
    runtime.add_processor(alpha)

    schedule = runtime.process_all({'one': 1})
    expected_schedule = ['alpha', 'beta', 'cee', 'epsilon', 'delta']

    assert schedule == expected_schedule

    schedule, pending = runtime.get_schedule()
    assert not pending
    assert schedule == ['alpha', 'beta', 'cee', 'epsilon', 'delta']

    runtime.reset()
    schedule = runtime.process_all(docdata={'one': 1})
    assert schedule == expected_schedule


def test_processor_exceptions():
    try:
        Processor.make()(1)
    except Exception as e:
        assert type(e) is Error
        assert e.what == 'invalid'
    else:
        raise AssertionError("Error not raised")

    class Callable(object):
        def __call__(self, data):
            return {}

    c = Callable()
    proc = Processor.make()(c)
    assert proc.name == 'Callable'

    try:
        Processor(1, 'hello')
    except Exception as e:
        assert type(e) is Error
        assert e.what == 'invalid'
    else:
        raise AssertionError("Error not raised")

    def foo(data):
        return {}

    for kwargs in [
        {'name': b'hello', 'reads': u'καλημέρα'},
        {'name': b'hello', 'writes': u'καλημέρα'},
        {'name': u'καλημέρα'},
    ]:

        try:
            Processor(process=foo, **kwargs)
        except Exception as e:
            assert type(e) is Error
            assert e.what == 'invalid'
        else:
            raise AssertionError("Error not raised")


    class Cleaner(Processor):

        def __init__(self, name):
            Processor.__init__(self, name=name,
                               reads=['counter'], writes=['counter'])

        def process(self, data):
            data['counter'] += 1
            if data['counter'] >= 12 :
                data['$runtime'].processed.append('nonexistent')
                raise Error(what='cleanup', data=data)
            return data

        def cleanup(self, name, exc, data):
            data['counter'] -= 2
            if data['counter'] <= 6:
                raise Error(what='cleanup-fail')
            return data

    spec = Spec()
    spec.compile({'counter': ()})
    runtime = Runtime(spec)
    runtime.add_processor(Cleaner(name='one'))
    runtime.add_processor(Cleaner(name='two'))
    runtime.add_processor(Cleaner(name='three'))
    results, pending, errs = runtime.process({'counter': 9})

    assert not pending
    assert runtime['counter'] == 7
    assert len(errs) == 2
    assert type(errs[0]) is Error
    assert errs[0].what == 'cleanup'
    assert type(errs[1]) is Error
    assert errs[1].what == 'cleanup-fail'

    runtime.reset()
    try:
        runtime.process_all({'counter': 9})
    except Exception as e:
        assert type(e) is Error
        assert e.what == 'process-error'
    else:
        raise AssertionError("Error not raised")


def test_incomplete_schemata():
    source_predicates = [
        (
            '.incomplete',
            {
                '.incomplete': (),
            },
        ),
        (
            '.incomplete.zero',
            {
                '.incomplete.zero': (),
                'zero': 0,
            },
        ),
        (
            '.incomplete.one',
            {
                '.incomplete.one': (),
                'one': 1,
            },
        ),
    ]
    domain = Spec()
    domain.compile_schemata(source_predicates)

    source = {
        'hello': {
            '?': {
                '.incomplete': (),
            },
        },
    }
    spec = domain.compile_spec(source)

    spec.config({'hello/alpha': ()})
    assert spec['hello/alpha/zero'] == NULL
    assert spec['hello/alpha/one'] == NULL

    domain.compile_schema('.incomplete', {'.incomplete.zero': ()})
    spec.config({'hello/beta': ()})
    assert spec['hello/beta/zero'] == 0
    assert spec['hello/beta/one'] == NULL

    domain.compile_schema('.incomplete', {'=': None})

    try:
        domain.compile_schema('.incomplete', {'.incomplete.one': ()})
    except Exception as e:
        assert type(e) is Error
        assert e.what == 'compile-failed'
        assert all(x.what == 'immutable-key' for x in e.errs)
    else:
        raise AssertionError("Error not raised")


def test_negotiate():
    source = {
        'party': {
            'members': {
                '?': {
                    'willing_host': (),
                    'address': (),
                    'capacity': (),
                },
            },
            'theme': {
                'proposals': {
                    '?': {
                        '?': None,
                    },
                },
            },
            'host': {
                '?': None,
            },
        },
    }

    spec0 = Spec()
    spec0.compile(source)

    alice_contrib_0 = {
        'party': {
            'members': {
                'alice': {
                    'willing_host': 'yes',
                    'address': 'aliceplace',
                    'food': 'good',
                    'music': 'best',
                },
            },
            'theme': {
                'proposals': {
                    'alice': 'cyberpunk',
                },
            },
            'host': 'alice',
        },
    }

    bob_contrib_0 = {
        'party': {
            'members': {
                'bob': {
                    'willing_host': 'yes',
                    'address': 'bobplace',
                    'food': 'best',
                    'music': 'good',
                },
                'alice': {
                    'food': 'bad',
                },
            },
            'theme': {
                'proposals': {
                    'bob': 'forest',
                },
            },
            'host': 'bob',
        },
    }

    eve_contrib_0 = {
        'party': {
            'members': {
                'eve': {
                    'willing_host': 'no',
                    'music': 'worst',
                    'food': 'worst',
                },
            },
            'theme': {
                'proposals': {
                    'eve': 'murder',
                },
            },
            'host': 'alice',
        },
    }

    contributions0 = [
        ('alice', alice_contrib_0),
        ('bob', bob_contrib_0),
    ]

    analysis0 = negotiate(spec0, contributions0, 'eve', eve_contrib_0)
    node_statuses = analysis0['node_statuses']

    assert all(
        node_statuses[p][1] == 'CONFLICT'
        for p in (
            '',
            'party',
            'party/host',
            'party/members',
            'party/members/alice',
            'party/members/alice/food',
        )
    )
