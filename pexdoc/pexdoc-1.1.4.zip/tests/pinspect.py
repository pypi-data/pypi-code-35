# pinspect.py
# Copyright (c) 2013-2019 Pablo Acosta-Serafini
# See LICENSE for details
# pylint: disable=C0103,C0111,C0413,E0611,F0401
# pylint: disable=R0201,R0205,R0903,R0913,R0914,R0915
# pylint: disable=W0104,W0212,W0232,W0611,W0612,W0613,W0621

# Standard library imports
from __future__ import print_function
from functools import partial
import copy
import os
import sys
import time
import types

# PyPI imports
import pmisc
from pmisc import AE, AI, CS, GET_EXMSG, RE
import pytest

if sys.hexversion == 0x03000000:
    from pexdoc.compat3 import _readlines
# Intra-package imports
import pexdoc.pinspect


###
# Helper functions
###
modfile = lambda x: sys.modules[x].__file__


###
# Tests for module functions
###
def test_private_props():
    """Test private_props function behavior."""
    obj = pexdoc.pinspect.Callables()
    assert sorted(list(pexdoc.pinspect.private_props(obj))) == [
        "_callables_db",
        "_class_names",
        "_fnames",
        "_module_names",
        "_modules_dict",
        "_reverse_callables_db",
    ]


if sys.hexversion == 0x03000000:

    def test_readlines():  # noqa: D202
        """Test _readlines function behavior."""

        def mopen1(fname, mode):
            raise RuntimeError("Mock mopen1 function")

        def mopen2(fname, mode):
            text = chr(40960) + "abcd" + chr(1972)
            # Next line raises UnicodeDecodeError
            b"\x80abc".decode("utf-8", "strict")

        class MockOpenCls(object):
            def __init__(self, fname, mode, encoding):
                pass

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_value, exc_tb):
                if exc_type is not None:
                    return False
                return True

            def readlines(self):
                return "MockOpenCls"

        pkg_dir = os.path.abspath(os.path.dirname(__file__))
        fname = os.path.join(pkg_dir, "test_misc.py")
        # This should not trigger an exception (functionality checked
        # by other unit tests)
        _readlines(fname)
        # Trigger unrelated exception exception
        obj = _readlines
        with pytest.raises(RuntimeError) as excinfo:
            _readlines(fname, mopen1)
        assert GET_EXMSG(excinfo) == "Mock mopen1 function"
        # Trigger UnicodeDecodeError exception
        assert _readlines(fname, mopen2, MockOpenCls) == "MockOpenCls"


def test_object_is_module():
    """Test object_is_module() function."""
    assert not pexdoc.pinspect.is_object_module(5)
    assert pexdoc.pinspect.is_object_module(sys.modules["pexdoc.pinspect"])


def test_get_module_name():
    """Test get_module_name() function."""
    obj = pexdoc.pinspect.get_module_name
    AI(obj, "module_obj", module_obj=5)
    mock_module_obj = types.ModuleType("mock_module_obj", "Mock module")
    exmsg = "Module object `mock_module_obj` could not be found in loaded modules"
    AE(obj, RE, exmsg, module_obj=mock_module_obj)
    ref = "pexdoc.pinspect"
    assert pexdoc.pinspect.get_module_name(sys.modules[ref]) == ref
    assert pexdoc.pinspect.get_module_name(sys.modules["pexdoc"]) == "pexdoc"


def test_get_module_name_from_fname():
    """Test _get_module_name_from_fname() function."""
    obj = pexdoc.pinspect._get_module_name_from_fname
    AE(obj, RE, "Module could not be found", fname="_not_a_module")
    assert obj(modfile("pexdoc.pinspect")) == "pexdoc.pinspect"


def test_is_special_method():
    """Test is_special_method() function."""
    assert not pexdoc.pinspect.is_special_method("func_name")
    assert not pexdoc.pinspect.is_special_method("_func_name_")
    assert pexdoc.pinspect.is_special_method("__func_name__")


###
# Test for classes
###
class TestCallables(object):
    """Test for Callables."""

    def test_check_intersection(self):
        """Test _check_intersection method behavior."""
        obj1 = pexdoc.pinspect.Callables()
        obj1._callables_db = {"call1": 1, "call2": 2}
        obj2 = pexdoc.pinspect.Callables()
        obj2._callables_db = {"call1": 1, "call2": "a"}
        exmsg = "Conflicting information between objects"
        obj = obj1._check_intersection
        AE(obj, RE, exmsg, other=obj2)
        obj1._callables_db = {"call1": 1, "call2": ["a", "c"]}
        obj2._callables_db = {"call1": 1, "call2": ["a", "b"]}
        AE(obj, RE, exmsg, other=obj2)
        obj1._callables_db = {"call1": 1, "call2": {"a": "b"}}
        obj2._callables_db = {"call1": 1, "call2": {"a": "c"}}
        AE(obj, RE, exmsg, other=obj2)
        obj1._callables_db = {"call1": 1, "call2": "a"}
        obj2._callables_db = {"call1": 1, "call2": "c"}
        AE(obj, RE, exmsg, other=obj2)
        obj1._callables_db = {"call1": 1, "call2": "a"}
        obj2._callables_db = {"call1": 1, "call2": "a"}
        assert obj1._check_intersection(obj2) is None

    def test_init_exceptions(self):
        """Test constructor exceptions."""
        obj = pexdoc.pinspect.Callables
        for item in [5, [5]]:
            AI(obj, "fnames", fnames=item)
        exmsg = "File _not_a_file_ could not be found"
        AE(obj, OSError, exmsg, fnames=["_not_a_file_"])

    def test_add(self):
        """Test __add__ __radd__ method behavior."""
        obj1 = pexdoc.pinspect.Callables()
        obj1._callables_db = {"call1": {"a": 5, "b": 6}, "call2": {"a": 7, "b": 8}}
        obj1._reverse_callables_db = {"rc1": "5", "rc2": "7"}
        obj1._modules_dict = {"key1": {"entry": "alpha"}, "key2": {"entry": "beta"}}
        obj1._fnames = {"hello": 0}
        obj1._module_names = ["this", "is"]
        obj1._class_names = ["once", "upon"]
        #
        obj2 = pexdoc.pinspect.Callables()
        obj2._callables_db = {
            "call3": {"a": 10, "b": 100},
            "call4": {"a": 200, "b": 300},
        }
        obj2._reverse_callables_db = {"rc3": "0", "rc4": "1"}
        obj2._modules_dict = {"key3": {"entry": "pi"}, "key4": {"entry": "gamma"}}
        obj2._fnames = {"world": 1}
        obj2._module_names = ["a", "test"]
        obj2._class_names = ["a", "time"]
        #
        obj1._callables_db = {"call3": {"a": 5, "b": 6}, "call2": {"a": 7, "b": 8}}
        with pytest.raises(RuntimeError) as excinfo:
            obj1 + obj2
        assert GET_EXMSG(excinfo) == "Conflicting information between objects"
        obj1._callables_db = {"call1": {"a": 5, "b": 6}, "call2": {"a": 7, "b": 8}}
        #
        obj2._reverse_callables_db = {"rc3": "5", "rc2": "-1"}
        with pytest.raises(RuntimeError) as excinfo:
            obj1 + obj2
        assert GET_EXMSG(excinfo) == "Conflicting information between objects"
        obj2._reverse_callables_db = {"rc3": "0", "rc4": "-1"}
        #
        obj2._modules_dict = {"key1": {"entry": "pi"}, "key4": {"entry": "gamma"}}
        with pytest.raises(RuntimeError) as excinfo:
            obj1 + obj2
        assert GET_EXMSG(excinfo) == "Conflicting information between objects"
        obj2._modules_dict = {"key3": {"entry": "pi"}, "key4": {"entry": "gamma"}}
        # Test when intersection is the same
        obj2._modules_dict = {"key1": {"entry": "alpha"}, "key4": {"entry": "gamma"}}
        obj1 + obj2
        obj2._modules_dict = {"key3": {"entry": "pi"}, "key4": {"entry": "gamma"}}
        #
        sobj = obj1 + obj2
        scomp = lambda x, y: sorted(x) == sorted(y)
        ref = {
            "call1": {"a": 5, "b": 6},
            "call2": {"a": 7, "b": 8},
            "call3": {"a": 10, "b": 100},
            "call4": {"a": 200, "b": 300},
        }
        assert scomp(sobj._callables_db, ref)
        ref = {"rc1": "5", "rc2": "7", "rc3": "0", "rc4": "-1"}
        assert scomp(sobj._reverse_callables_db, ref)
        ref = {
            "key1": {"entry": "alpha"},
            "key2": {"entry": "beta"},
            "key3": {"entry": "pi"},
            "key4": {"entry": "gamma"},
        }
        assert scomp(sobj._modules_dict, ref)
        assert scomp(sobj._fnames, {"hello": 0, "world": 1})
        assert scomp(sobj._module_names, ["this", "is", "a", "test"])
        assert scomp(sobj._class_names, ["once", "upon", "a", "time"])
        #
        obj1 += obj2
        ref = {
            "call1": {"a": 5, "b": 6},
            "call2": {"a": 7, "b": 8},
            "call3": {"a": 10, "b": 100},
            "call4": {"a": 200, "b": 300},
        }
        assert scomp(obj1._callables_db, ref)
        ref = {"rc1": "5", "rc2": "7", "rc3": "0", "rc4": "-1"}
        assert scomp(obj1._reverse_callables_db, ref)
        ref = {
            "key1": {"entry": "alpha"},
            "key2": {"entry": "beta"},
            "key3": {"entry": "pi"},
            "key4": {"entry": "gamma"},
        }
        assert scomp(obj1._modules_dict, ref)
        assert scomp(obj1._fnames, {"hello": 0, "world": 1})
        assert scomp(obj1._module_names, ["this", "is", "a", "test"])
        assert scomp(obj1._class_names, ["once", "upon", "a", "time"])

    def test_copy(self):
        """Test __copy__ method behavior."""
        sobj = pexdoc.pinspect.Callables()
        import tests.support.pinspect_support_module_1

        sobj.trace([modfile("tests.support.pinspect_support_module_1")])
        dobj = copy.copy(sobj)
        assert sobj._module_names == dobj._module_names
        assert id(sobj._module_names) != id(dobj._module_names)
        assert sobj._class_names == dobj._class_names
        assert id(sobj._class_names) != id(dobj._class_names)
        assert sobj._callables_db == dobj._callables_db
        assert id(sobj._callables_db) != id(dobj._callables_db)
        assert sobj._reverse_callables_db == dobj._reverse_callables_db
        assert id(sobj._reverse_callables_db) != id(dobj._reverse_callables_db)

    def test_eq(self):
        """Test __eq__ method behavior."""
        obj1 = pexdoc.pinspect.Callables()
        obj2 = pexdoc.pinspect.Callables()
        obj3 = pexdoc.pinspect.Callables()
        import tests.support.pinspect_support_module_1
        import tests.support.pinspect_support_module_2

        mname = "tests.support.pinspect_support_module_1"
        obj1.trace([modfile(mname)])
        obj2.trace([modfile(mname)])
        obj3.trace([modfile("pmisc")])
        assert (obj1 == obj2) and (obj1 != obj3)
        assert obj1 != 5

    def test_repr(self):
        """Test __repr__ method behavior."""
        get_name = lambda x: modfile(x).replace(".pyc", ".py")
        import tests.support.exdoc_support_module_1

        file1 = get_name("tests.support.exdoc_support_module_1")
        file2 = get_name("tests.support.exdoc_support_module_2")
        xobj = pexdoc.pinspect.Callables([file2])
        xobj.trace([file1])
        ref = "pexdoc.pinspect.Callables([{0}, {1}])".format(repr(file1), repr(file2))
        assert repr(xobj) == ref

    def test_str_empty(self):
        """Test __str__ magic method when object is empty."""
        obj = pexdoc.pinspect.Callables()
        assert str(obj) == ""

    def test_refresh(self):
        """Test refresh method behavior."""
        ref = modfile("pexdoc.pinspect")
        src = os.path.join(os.path.dirname(ref), "pit.py")
        with open(src, "w") as fobj:
            fobj.write(
                "class MyClass(object):\n" "    pass\n" "def func1():\n" "    pass\n"
            )
        import pexdoc.pit

        obj = pexdoc.pinspect.Callables([ref, src])
        tmod = obj._fnames[src]
        obj.trace([src])
        assert obj._fnames[src] == tmod
        cname1 = "pexdoc.pinspect.Callables"
        cname2 = "pexdoc.pinspect._AstTreeScanner"
        rtext = (
            "Modules:\n",
            "   pexdoc.pinspect\n",
            "   pexdoc.pit\n",
            "Classes:\n",
            "   pexdoc.pinspect.Callables\n",
            "   pexdoc.pinspect._AstTreeScanner\n",
            "   pexdoc.pit.MyClass\n",
            "pexdoc.pinspect._get_module_name_from_fname: func (40-53)\n",
            "pexdoc.pinspect._validate_fname: func (54-65)\n",
            "pexdoc.pinspect.get_function_args: func (66-128)\n",
            "pexdoc.pinspect.get_module_name: func (129-158)\n",
            "pexdoc.pinspect.is_object_module: func (159-170)\n",
            "pexdoc.pinspect.is_special_method: func (171-182)\n",
            "pexdoc.pinspect.private_props: func (183-206)\n",
            cname1 + ": class (207-772)\n",
            cname1 + ".__init__: meth (234-243)\n",
            cname1 + ".__add__: meth (244-283)\n",
            cname1 + ".__bool__: meth (284-306)\n",
            cname1 + ".__copy__: meth (307-325)\n",
            cname1 + ".__eq__: meth (326-355)\n",
            cname1 + ".__iadd__: meth (356-391)\n",
            cname1 + ".__nonzero__: meth (392-414)\n",
            cname1 + ".__repr__: meth (415-433)\n",
            cname1 + ".__str__: meth (434-483)\n",
            cname1 + "._check_intersection: meth (484-507)\n",
            cname1 + "._get_callables_db: meth (508-511)\n",
            cname1 + ".get_callable_from_line: meth (512-526)\n",
            cname1 + "._get_reverse_callables_db: meth (527-530)\n",
            cname1 + ".load: meth (531-577)\n",
            cname1 + ".refresh: meth (578-581)\n",
            cname1 + ".save: meth (582-610)\n",
            cname1 + ".trace: meth (611-697)\n",
            cname1 + ".callables_db: prop (698-730)\n",
            cname1 + ".reverse_callables_db: prop (731-772)\n",
            cname2 + ": class (773-1119)\n",
            cname2 + ".__init__: meth (777-790)\n",
            cname2 + "._close_callable: meth (791-904)\n",
            cname2 + "._get_indent: meth (905-912)\n",
            cname2 + "._in_class: meth (913-920)\n",
            cname2 + "._pop_indent_stack: meth (921-966)\n",
            cname2 + ".generic_visit: meth (967-980)\n",
            cname2 + ".visit_arguments: meth (981-988)\n",
            cname2 + ".visit_Assign: meth (989-1030)\n",
            cname2 + ".visit_ClassDef: meth (1031-1065)\n",
            cname2 + ".visit_FunctionDef: meth (1066-1119)\n",
            "pexdoc.pit.MyClass: class (1-2)\n",
            "pexdoc.pit.func1: func (3-4)",
        )
        CS(str(obj), "".join(rtext))
        ftime = int(os.path.getmtime(src))
        while int(time.time()) <= ftime:
            time.sleep(0.1)
        os.remove(src)
        content = "def my_func():\n    pass"
        with open(src, "w") as fobj:
            fobj.write(content)
        obj.refresh()
        assert obj._fnames[src] != tmod
        rtext = (
            "Modules:\n",
            "   pexdoc.pinspect\n",
            "   pexdoc.pit\n",
            "Classes:\n",
            "   pexdoc.pinspect.Callables\n",
            "   pexdoc.pinspect._AstTreeScanner\n",
            "pexdoc.pinspect._get_module_name_from_fname: func (40-53)\n",
            "pexdoc.pinspect._validate_fname: func (54-65)\n",
            "pexdoc.pinspect.get_function_args: func (66-128)\n",
            "pexdoc.pinspect.get_module_name: func (129-158)\n",
            "pexdoc.pinspect.is_object_module: func (159-170)\n",
            "pexdoc.pinspect.is_special_method: func (171-182)\n",
            "pexdoc.pinspect.private_props: func (183-206)\n",
            cname1 + ": class (207-772)\n",
            cname1 + ".__init__: meth (234-243)\n",
            cname1 + ".__add__: meth (244-283)\n",
            cname1 + ".__bool__: meth (284-306)\n",
            cname1 + ".__copy__: meth (307-325)\n",
            cname1 + ".__eq__: meth (326-355)\n",
            cname1 + ".__iadd__: meth (356-391)\n",
            cname1 + ".__nonzero__: meth (392-414)\n",
            cname1 + ".__repr__: meth (415-433)\n",
            cname1 + ".__str__: meth (434-483)\n",
            cname1 + "._check_intersection: meth (484-507)\n",
            cname1 + "._get_callables_db: meth (508-511)\n",
            cname1 + ".get_callable_from_line: meth (512-526)\n",
            cname1 + "._get_reverse_callables_db: meth (527-530)\n",
            cname1 + ".load: meth (531-577)\n",
            cname1 + ".refresh: meth (578-581)\n",
            cname1 + ".save: meth (582-610)\n",
            cname1 + ".trace: meth (611-697)\n",
            cname1 + ".callables_db: prop (698-730)\n",
            cname1 + ".reverse_callables_db: prop (731-772)\n",
            cname2 + ": class (773-1119)\n",
            cname2 + ".__init__: meth (777-790)\n",
            cname2 + "._close_callable: meth (791-904)\n",
            cname2 + "._get_indent: meth (905-912)\n",
            cname2 + "._in_class: meth (913-920)\n",
            cname2 + "._pop_indent_stack: meth (921-966)\n",
            cname2 + ".generic_visit: meth (967-980)\n",
            cname2 + ".visit_arguments: meth (981-988)\n",
            cname2 + ".visit_Assign: meth (989-1030)\n",
            cname2 + ".visit_ClassDef: meth (1031-1065)\n",
            cname2 + ".visit_FunctionDef: meth (1066-1119)\n",
            "pexdoc.pit.my_func: func (1-2)",
        )
        CS(str(obj), "".join(rtext))
        ## Test malformed JSON file
        obj = pexdoc.pinspect.Callables()
        json_src = os.path.join(os.path.dirname(ref), "pit.json")
        json_txt = (
            "{{\n"
            '    "_callables_db": {{\n'
            '        "pexdoc.pit.my_func": {{\n'
            '            "code_id": [\n'
            '                "{pyfile}",\n'
            "                1\n"
            "            ],\n"
            '            "last_lineno": 2,\n'
            '            "name": "pexdoc.pit.my_func",\n'
            '            "type": "func"\n'
            "        }}\n"
            "    }},\n"
            '    "_class_names": [],\n'
            '    "_fnames": {{\n'
            '        "{pyfile}": {{\n'
            '            "classes": [],\n'
            '            "date": 1,\n'
            '            "name": "pexdoc.pit"\n'
            "        }}\n"
            "    }},\n"
            '    "_module_names": [\n'
            '        "pexdoc.pit"\n'
            "    ],\n"
            '    "_modules_dict": {{\n'
            '        "pexdoc.pit": [\n'
            "            {{\n"
            '                "code_id": [\n'
            '                    "{pyfile}",\n'
            "                    1\n"
            "                ],\n"
            '                "last_lineno": 2,\n'
            '                "name": "pexdoc.pit.my_func",\n'
            '                "type": "func"\n'
            "            }}\n"
            "        ]\n"
            "    }},\n"
            '    "_reverse_callables_db": {{\n'
            '        "(\'{pyfile}\', 1)": "pexdoc.pit.my_func",\n'
            '        "(\'{pyfile}\', 10)": "pexdoc.pit.my_func"\n'
            "    }}\n"
            "}}\n"
        )
        with open(json_src, "w") as fobj:
            fobj.write(json_txt.format(pyfile=src.replace("\\", "/")))
        obj.load(json_src)
        obj.refresh()
        os.remove(json_src)
        os.remove(src)

    def test_load_save(self):
        """Test load and save methods behavior."""
        import tests.support.csv_file
        import tests.support.exdoc_support_module_1

        # Empty object
        obj1 = pexdoc.pinspect.Callables()
        with pmisc.TmpFile() as fname:
            obj1.save(fname)
            obj2 = pexdoc.pinspect.Callables()
            obj2.load(fname)
        assert obj1 == obj2
        # 1 module trace
        mname = "tests.support.csv_file"
        cname = "{0}.CsvFile".format(mname)
        obj1 = pexdoc.pinspect.Callables([modfile(mname)])
        with pmisc.TmpFile() as fname:
            obj1.save(fname)
            obj2 = pexdoc.pinspect.Callables()
            assert not bool(obj2)
            obj2.load(fname)
        assert obj1 == obj2
        # Test merging of traced and file-based module information
        mname1 = "tests.support.csv_file"
        obj1 = pexdoc.pinspect.Callables([modfile(mname1)])
        mname2 = "tests.support.exdoc_support_module_1"
        obj2 = pexdoc.pinspect.Callables([modfile(mname2)])
        with pmisc.TmpFile() as fname1:
            with pmisc.TmpFile() as fname2:
                obj1.save(fname1)
                obj2.save(fname2)
                obj3 = pexdoc.pinspect.Callables([modfile(mname1), modfile(mname2)])
                obj4 = pexdoc.pinspect.Callables()
                obj4.load(fname2)
                obj4.load(fname1)
        assert obj3 == obj4

    def test_load_exceptions(self):
        """Test load method exceptions."""
        obj = pexdoc.pinspect.Callables()
        for item in [True, 5]:
            AI(obj.load, "callables_fname", callables_fname=item)
        exmsg = "File _not_a_file_ could not be found"
        AE(obj.load, OSError, exmsg, callables_fname="_not_a_file_")

    def test_save_exceptions(self):
        """Test save method exceptions."""
        obj = pexdoc.pinspect.Callables()
        for item in [True, 5]:
            AI(obj.save, "callables_fname", callables_fname=item)

    def test_trace(self):
        """Test trace method behavior."""
        import tests.support.csv_file

        mname = "tests.support.csv_file"
        cname = "{0}.CsvFile".format(mname)
        xobj = pexdoc.pinspect.Callables([modfile(mname)])
        ref = []
        ref.append("Modules:")
        ref.append("   {0}".format(mname))
        ref.append("Classes:")
        ref.append("   {0}".format(cname))
        ref.append("{0}._homogenize_data_filter: func (52-77)".format(mname))

        ref.append("{0}._isnumber: func (78-86)".format(mname))
        ref.append("{0}._tofloat: func (87-99)".format(mname))
        ref.append("{0}._write_int: func (100-123)".format(mname))
        ref.append("{0}: class (124-960)".format(cname))
        ref.append("{0}.__init__: meth (176-242)".format(cname))
        ref.append("{0}.__eq__: meth (243-279)".format(cname))
        ref.append("{0}.__repr__: meth (280-316)".format(cname))
        ref.append("{0}.__str__: meth (317-362)".format(cname))
        ref.append("{0}._format_rfilter: meth (363-383)".format(cname))
        ref.append("{0}._gen_col_index: meth (384-394)".format(cname))
        ref.append("{0}._get_cfilter: meth (395-397)".format(cname))
        ref.append("{0}._get_dfilter: meth (398-400)".format(cname))
        ref.append("{0}._get_rfilter: meth (401-403)".format(cname))
        ref.append("{0}._reset_dfilter_int: meth (404-409)".format(cname))
        ref.append("{0}._in_header: meth (410-437)".format(cname))
        ref.append("{0}._set_cfilter: meth (438-442)".format(cname))
        ref.append("{0}._set_dfilter: meth (443-448)".format(cname))
        ref.append("{0}._set_rfilter: meth (449-453)".format(cname))
        ref.append("{0}._add_dfilter_int: meth (454-493)".format(cname))
        ref.append("{0}._apply_filter: meth (494-522)".format(cname))
        ref.append("{0}._set_has_header: meth (523-526)".format(cname))
        ref.append("{0}._validate_frow: meth (527-532)".format(cname))
        ref.append("{0}._validate_rfilter: meth (533-556)".format(cname))
        ref.append("{0}.add_dfilter: meth (557-581)".format(cname))
        ref.append("{0}.cols: meth (582-601)".format(cname))
        ref.append("{0}.data: meth (602-632)".format(cname))
        ref.append("{0}.dsort: meth (633-682)".format(cname))
        ref.append("{0}.header: meth (683-715)".format(cname))
        ref.append("{0}.replace: meth (716-781)".format(cname))
        ref.append("{0}.reset_dfilter: meth (782-799)".format(cname))
        ref.append("{0}.rows: meth (800-819)".format(cname))
        ref.append("{0}.write: meth (820-889)".format(cname))
        ref.append("{0}.cfilter: prop (890-912)".format(cname))
        ref.append("{0}.dfilter: prop (913-936)".format(cname))
        ref.append("{0}.rfilter: prop (937-960)".format(cname))
        ref_txt = "\n".join(ref)
        actual_txt = str(xobj)
        CS(actual_txt, ref_txt)
        #
        import tests.support.exdoc_support_module_1

        mname = "tests.support.exdoc_support_module_1"
        xobj = pexdoc.pinspect.Callables([modfile(mname)])
        ref = []
        cname = "{0}.ExceptionAutoDocClass".format(mname)
        ref.append("Modules:")
        ref.append("   {0}".format(mname))
        ref.append("Classes:")
        ref.append("   {0}".format(cname))
        ref.append("   {0}.MyClass".format(mname))
        ref.append("{0}._validate_arguments: func (18-31)".format(mname))
        ref.append("{0}._write: func (32-36)".format(mname))
        ref.append("{0}.write: func (37-48)".format(mname))
        ref.append("{0}.read: func (49-58)".format(mname))
        ref.append("{0}.probe: func (59-68)".format(mname))
        ref.append("{0}.dummy_decorator1: func (69-73)".format(mname))
        ref.append("{0}.dummy_decorator2: func (74-88)".format(mname))
        ref.append("{0}.dummy_decorator2.wrapper: func (82-85)".format(mname))
        ref.append("{0}.mlmdfunc: func (89-97)".format(mname))
        ref.append("{0}: class (98-220)".format(cname))
        ref.append("{0}.__init__: meth (102-112)".format(cname))
        ref.append("{0}._del_value3: meth (113-118)".format(cname))
        ref.append("{0}._get_value3: meth (119-125)".format(cname))
        ref.append("{0}._set_value1: meth (126-134)".format(cname))
        ref.append("{0}._set_value2: meth (135-148)".format(cname))
        ref.append("{0}._set_value3: meth (149-157)".format(cname))
        ref.append("{0}.add: meth (158-165)".format(cname))
        ref.append("{0}.subtract: meth (166-173)".format(cname))
        ref.append("{0}.multiply: meth (174-181)".format(cname))
        ref.append("{0}.divide: meth (182-186)".format(cname))
        ref.append("{0}.temp(getter): meth (187-191)".format(cname))
        ref.append("{0}.temp(setter): meth (192-197)".format(cname))
        ref.append("{0}.temp(deleter): meth (198-203)".format(cname))
        ref.append("{0}.value1: prop (204-211)".format(cname))
        ref.append("{0}.value2: prop (212-214)".format(cname))
        ref.append("{0}.value3: prop (215-216)".format(cname))
        ref.append("{0}.value4: prop (217-220)".format(cname))
        ref.append("{0}.my_func: func (221-224)".format(mname))
        ref.append("{0}.MyClass: class (225-228)".format(mname))
        ref.append("{0}.MyClass.value: prop (228)".format(mname))
        ref_txt = "\n".join(ref)
        actual_txt = str(xobj)
        CS(actual_txt, ref_txt)
        #
        import tests.exdoc

        mname = "tests.exdoc"
        froot = "{0}.exdocobj".format(mname)
        xobj = pexdoc.pinspect.Callables([modfile(mname)])
        cname1 = "{0}.TestExDocCxt".format(mname)
        cname2 = "{0}.TestExDoc".format(mname)
        mename1 = "{0}.test_multiple".format(cname1)
        mename2 = "{0}.test_build_ex_tree".format(cname2)
        meroot = "{0}.test_get_sphinx".format(cname2)
        ref = []
        ref.append("Modules:")
        ref.append("   {0}".format(mname))
        ref.append("Classes:")
        ref.append("   {0}.MockFCode".format(mname))
        ref.append("   {0}.MockGetFrame".format(mname))
        ref.append("   {0}.TestExDoc".format(mname))
        ref.append("   {0}.TestExDocCxt".format(mname))
        ref.append("{0}: func (54-91)".format(froot))
        ref.append("{0}.multi_level_write: func (60-68)".format(froot))
        ref.append("{0}_raised: func (92-105)".format(froot))
        ref.append("{0}_single: func (106-115)".format(froot))
        ref.append("{0}.simple_exobj: func (116-131)".format(mname))
        ref.append("{0}.simple_exobj.func1: func (122-124)".format(mname))
        ref.append("{0}.mock_getframe: func (132-135)".format(mname))
        ref.append("{0}.trace_error_class: func (136-147)".format(mname))
        ref.append("{0}.MockFCode: class (148-153)".format(mname))
        ref.append("{0}.MockFCode.__init__: meth (149-153)".format(mname))
        ref.append("{0}.MockGetFrame: class (154-161)".format(mname))
        ref.append("{0}.MockGetFrame.__init__: meth (155-161)".format(mname))
        ref.append("{0}: class (162-277)".format(cname1))
        ref.append("{0}.test_init: meth (165-220)".format(cname1))
        ref.append("{0}.test_init.check_ctx1: func (168-174)".format(cname1))
        ref.append("{0}.test_init.check_ctx2: func (175-182)".format(cname1))
        ref.append("{0}.test_init.func0: func (183-190)".format(cname1))
        ref.append("{0}.test_multiple: meth (221-259)".format(cname1))
        ref.append("{0}.func1: func (224-231)".format(mename1))
        ref.append("{0}.test_trace: func (232-247)".format(mename1))
        ref.append("{0}.test_save_callables: meth (260-277)".format(cname1))
        ref.append("{0}: class (278-747)".format(cname2))
        ref.append("{0}.test_init: meth (281-297)".format(cname2))
        ref.append("{0}.test_copy: meth (298-313)".format(cname2))
        ref.append("{0}.test_build_ex_tree: meth (314-425)".format(cname2))
        ref.append("{0}.func1: func (322-326)".format(mename2))
        ref.append("{0}.mock_add_nodes1: func (329-331)".format(mename2))
        ref.append("{0}.mock_add_nodes2: func (332-334)".format(mename2))
        ref.append("{0}.mock_add_nodes3: func (335-337)".format(mename2))
        ref.append("{0}.test_depth: meth (426-433)".format(cname2))
        ref.append("{0}.test_exclude: meth (434-441)".format(cname2))
        ref.append("{0}_autodoc: meth (442-471)".format(meroot))
        ref.append("{0}_doc: meth (472-747)".format(meroot))
        ref_txt = "\n".join(ref)
        actual_txt = str(xobj)
        CS(actual_txt, ref_txt)
        #
        import tests.support.pinspect_support_module_4

        mname = "tests.support.pinspect_support_module_4"
        xobj = pexdoc.pinspect.Callables([modfile(mname)])
        ref = []
        fname = "{0}.another_property_action_enclosing_function".format(mname)
        ref.append("Modules:")
        ref.append("   {0}".format(mname))
        ref.append("{0}: func (17-24)".format(fname))
        ref.append("{0}.fget: func (20-23)".format(fname))
        ref_txt = "\n".join(ref)
        actual_txt = str(xobj)
        CS(actual_txt, ref_txt)
        # Test re-tries, should produce no action and raise no exception
        xobj = pexdoc.pinspect.Callables([modfile(mname)])
        import tests.support.pinspect_support_module_10

        mname = "tests.support.pinspect_support_module_10"
        xobj = pexdoc.pinspect.Callables([modfile(mname)])
        ref = []
        cname = "{0}.AClass".format(mname)
        ref.append("Modules:")
        ref.append("   {0}".format(mname))
        ref.append("Classes:")
        ref.append("   {0}".format(cname))
        ref.append("   {0}.method1.SubClass".format(cname))
        ref.append("{0}: class (7-32)".format(cname))
        ref.append("{0}.method1: meth (11-29)".format(cname))
        ref.append("{0}.method1.func1: func (15-19)".format(cname))
        ref.append("{0}.method1.SubClass: class (22-27)".format(cname))
        ref.append("{0}.method1.SubClass.__init__: meth (25-27)".format(cname))
        ref.append("{0}.method2: meth (30-32)".format(cname))
        ref_txt = "\n".join(ref)
        actual_txt = str(xobj)
        CS(actual_txt, ref_txt)

    def test_callables_db(self):
        """Test callables_db property."""
        import tests.support.pinspect_support_module_4

        mname = "tests.support.pinspect_support_module_4"
        xobj = pexdoc.pinspect.Callables([modfile(mname)])
        pkg_dir = os.path.dirname(__file__)
        ref = {
            "tests.support.pinspect_support_module_4."
            "another_property_action_enclosing_function": {
                "code_id": (
                    os.path.join(pkg_dir, "support", "pinspect_support_module_4.py"),
                    16,
                ),
                "last_lineno": 21,
                "name": "pinspect_support_module_4."
                "another_property_action_enclosing_function",
                "type": "func",
            },
            "tests.support.pinspect_support_module_4."
            "another_property_action_enclosing_function.fget": {
                "code_id": (
                    os.path.join(pkg_dir, "support", "pinspect_support_module_4.py"),
                    18,
                ),
                "last_lineno": 20,
                "name": "pinspect_support_module_4."
                "another_property_action_enclosing_function.fget",
                "type": "func",
            },
        }
        assert sorted(xobj.callables_db) == sorted(ref)
        ref = {
            (os.path.join(pkg_dir, "support", "pinspect_support_module_4.py"), 17): (
                "pinspect_support_module_4."
                "another_property_action_enclosing_function"
            ),
            (os.path.join(pkg_dir, "support", "pinspect_support_module_4.py"), 20): (
                "pinspect_support_module_4."
                "another_property_action_enclosing_function.fget"
            ),
        }
        assert sorted(xobj.reverse_callables_db) == sorted(ref)

    def test_get_callable_from_line(self):
        """Test get_callable_from_line() function."""
        xobj = pexdoc.pinspect.Callables()
        import tests.support.pinspect_support_module_4

        fname = modfile("tests.support.pinspect_support_module_4")
        ref = (
            "tests.support.pinspect_support_module_4."
            "another_property_action_enclosing_function"
        )
        assert xobj.get_callable_from_line(fname, 17) == ref
        xobj = pexdoc.pinspect.Callables([fname])
        ref = (
            "tests.support.pinspect_support_module_4."
            "another_property_action_enclosing_function"
        )
        assert xobj.get_callable_from_line(fname, 17) == ref
        ref = (
            "tests.support.pinspect_support_module_4."
            "another_property_action_enclosing_function"
        )
        assert xobj.get_callable_from_line(fname, 18) == ref
        ref = (
            "tests.support.pinspect_support_module_4."
            "another_property_action_enclosing_function"
        )
        assert xobj.get_callable_from_line(fname, 24) == ref
        ref = (
            "tests.support.pinspect_support_module_4."
            "another_property_action_enclosing_function.fget"
        )
        assert xobj.get_callable_from_line(fname, 20) == ref
        ref = (
            "tests.support.pinspect_support_module_4."
            "another_property_action_enclosing_function.fget"
        )
        assert xobj.get_callable_from_line(fname, 21) == ref
        ref = (
            "tests.support.pinspect_support_module_4."
            "another_property_action_enclosing_function.fget"
        )
        assert xobj.get_callable_from_line(fname, 22) == ref
        ref = "tests.support.pinspect_support_module_4"
        assert xobj.get_callable_from_line(fname, 100) == ref


##
# Tests for get_function_args()
###
class TestGetFunctionArgs(object):
    """Tests for get_function_args function."""

    def test_all_positional_arguments(self):  # noqa: D202
        """Test function when all arguments are positional arguments."""

        def func(ppar1, ppar2, ppar3):
            pass

        obj = pexdoc.pinspect.get_function_args
        assert obj(func) == ("ppar1", "ppar2", "ppar3")

    def test_all_keyword_arguments(self):  # noqa: D202
        """Test function when all arguments are keywords arguments."""

        def func(kpar1=1, kpar2=2, kpar3=3):
            pass

        obj = pexdoc.pinspect.get_function_args
        assert obj(func) == ("kpar1", "kpar2", "kpar3")

    def test_positional_and_keyword_arguments(self):  # noqa: D202
        """Test function when arguments are mix of positional and keywords arguments."""

        def func(ppar1, ppar2, ppar3, kpar1=1, kpar2=2, kpar3=3, **kwargs):
            pass

        assert pexdoc.pinspect.get_function_args(func) == (
            "ppar1",
            "ppar2",
            "ppar3",
            "kpar1",
            "kpar2",
            "kpar3",
            "**kwargs",
        )
        assert pexdoc.pinspect.get_function_args(func, no_varargs=True) == (
            "ppar1",
            "ppar2",
            "ppar3",
            "kpar1",
            "kpar2",
            "kpar3",
        )

    def test_no_arguments(self):  # noqa: D202
        """Test function when there are no arguments passed."""

        def func():
            pass

        assert pexdoc.pinspect.get_function_args(func) == ()

    def test_no_self(self):  # noqa: D202
        """Test function when there are no arguments passed."""

        class MyClass(object):
            def __init__(self, value, **kwargs):
                pass

        obj = partial(pexdoc.pinspect.get_function_args, MyClass.__init__)
        assert obj() == ("self", "value", "**kwargs")
        assert obj(no_self=True) == ("value", "**kwargs")
        assert obj(no_self=True, no_varargs=True) == ("value",)
        assert obj(no_varargs=True) == ("self", "value")

    def test_nonzero(self):
        """Test __nonzero__() function."""
        obj = pexdoc.pinspect.Callables()
        assert not obj
        obj.trace([modfile("pmisc")])
        assert obj
