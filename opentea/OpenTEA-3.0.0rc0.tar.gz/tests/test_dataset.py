# pylint: disable=missing-docstring
from os.path import join

import pytest

from .context import opentea, Project


class TestDataset(Project):
    @classmethod
    def setup_class(cls):
        super(TestDataset, cls).setup_class()
        cls.dts = opentea.Dataset(cls.xml_file)

    def test_setup_class_unknown(cls):
        super(TestDataset, cls).setup_class()
        with pytest.raises(IOError):
            cls.dts = opentea.Dataset('False.xml')

    def test_repr(self):
        repr(self.dts)

    def test_addChild_exists(self):
        with pytest.raises(opentea.OTException):
            self.dts.addChild("temperature", "400", "alpha")
#            self.dts.addChild("xor", "", "example_lite")

    def test_addChild(self):
        self.dts.addChild("pressure", "101325", "alpha")
        assert self.dts.nodeExists("pressure", "alpha")
        self.dts.removeNode("pressure", "alpha")

    def test_nodeExists(self):
        assert self.dts.nodeExists("temperature")

    def test_nodeExists_not(self):
        assert not self.dts.nodeExists("pressure")

    def test_getValue(self):
        assert self.dts.getValue("temperature") == "300"

    def test_getValue_unknown(self):
        with pytest.raises(opentea.OTNoNodeException):
            self.dts.getValue("dummy")

    def test_getValue_ambiguous(self):
        with pytest.raises(opentea.OTTooManyNodesException):
            self.dts.getValue("real1")

    def test_tryGetValue(self):
        assert self.dts.tryGetValue("", "codeversion")
#
    def test_tryGetValue_unknown(self):
        assert self.dts.tryGetValue("a", "dummy") == 'a'

    def test_getListValue(self):
        item = self.dts.getListValue("probe")
        assert item == ["x", "0", "y", "0.1", "z", "0.2"]

    def test_getListDict(self):
        item = self.dts.getListDict("probe")
        assert item == {"x": "0", "y": "0.1", "z": "0.2"}

#    def test_addToUniqList(self):
#        self.dts.addToUniqList("theta;1", "probe")
#        item2 = self.dts.getListValue("probe")
#        print item2, type(item2)
#        assert item2 == {"x": "0", "y": "0.1", "z": "0.2", "theta": "1"}

    def test_setValue(self):
        item = self.dts.getValue("phi")
        self.dts.setValue(item + "a", "phi")
        assert self.dts.getValue("phi") == item + "a"

    def test_setValue_list(self):
        item2 = self.dts.getListValue("probe")
        self.dts.setValue(item2 + ["theta", "1"], "probe2")

    #def test_setValue_unknown(self):
    #    with pytest.raises(opentea.OTException):
    #        self.dts.setValue("dummy", "dummy_var")

    def test_getChildrenName(self):
        assert self.dts.getChildrenName("item_1095892") == ["real2",
                                                            "real3"]

# To check
    # def test_getChildrenName_unknown(self):
    #     with pytest.raises(opentea.OTNoNodeException):
    #         self.dts.getChildrenName("dummy")

    def test_removeNode(self):
        self.dts.addChild("pressure", "101325", "alpha")
        self.dts.removeNode("pressure", "alpha")
        assert not self.dts.nodeExists("pressure", "alpha")


class TestMultiple(Project):
    @classmethod
    def setup_class(cls):
        super(TestMultiple, cls).setup_class()
        cls.dts = opentea.Dataset(cls.xml_file)
        cls.mul = cls.dts.get_multiple("mymul")

    def test_ids(self):
        assert self.mul.ids == ["item_1095892", "item_1095893"]

    def test_headers(self):
        assert self.mul.headers == ["label", "real2", "real3"]

    def test_rows(self):
        assert self.mul.rows == [["label2", "1.01", "0.01"],
                                 ["label1", "1.01", "0.02"]]

    def test_columns(self):
        assert self.mul.columns == [["label2", "label1"],
                                    ["1.01", "1.01"],
                                    ["0.01", "0.02"]]

    def test_keys(self):
        assert list(self.mul.keys()) == ["label", "real2", "real3",
                                   "label2", "label1"]

    def test_getitem_label(self):
        assert self.mul["label2"] == ["label2", "1.01", "0.01"]

    def test_getitem_col(self):
        assert self.mul["real2"] == ["1.01", "1.01"]

    def test_order_by(self):
        self.mul.order_by("label")
        assert self.mul["label"] == ["label1", "label2"]
        self.mul.order_by("real3")
