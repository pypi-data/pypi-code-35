from devconfig.attrs import YamlAttributedObject
import attr


@attr.s
class DummyObject(YamlAttributedObject):
    value = attr.ib()

@attr.s
class DefaultDummyObject(YamlAttributedObject):
    value = attr.ib()