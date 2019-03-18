import os
from typing import Any, Union

import attr


@attr.s(frozen=True, auto_attribs=True)
class DataUri:
    basename: str = attr.ib(converter=str)
    prefix: str = attr.ib(converter=str)

    @property
    def fullpath(self):
        return os.path.join(self.prefix, self.basename)


@attr.s(frozen=True, auto_attribs=True)
class DataPath(DataUri):
    pass


@attr.s(frozen=True, auto_attribs=True)
class DataTable:
    dataset: str
    tablename: str
    query: str = ""


class DataFormat:
    TEXT = "txt"
    JSON = "json"
    PARQUET = "parquet"
    CSV = "csv"


@attr.s(frozen=True, auto_attribs=True)
class Data:
    name: str
    source: Union[DataUri, DataTable]
    schema: Any = None
    format: str = DataFormat.JSON  # noqa
    description: str = ""

    def to_dict(self):
        return attr.asdict(self)


class DataNode:
    def __init__(
        self,
        name: str,
        source: Union[DataUri, DataTable],
        schema: Any = None,
        format: str = DataFormat.JSON,
        description: str = "",
    ):
        self._data = Data(
            name=name,
            source=source,
            schema=schema,
            format=format,
            description=description,
        )

    @property
    def data(self) -> Data:
        return self._data

    def load(self):
        raise NotImplementedError()

    def dump(self):
        raise NotImplementedError()

    def __repr__(self):
        return f"DataNode.{repr(self._data)}"

    def __eq__(self, other: "DataNode"):
        return self.data == other.data and self.__class__ == other.__class__


class DataLink:
    def __init__(
        self,
        delegate_cls: DataNode,
        name: str,
        source: Union[DataUri, DataTable],
        link: Union[DataUri, DataTable],
        schema: Any = None,
        format: str = DataFormat.JSON,
        description: str = "",
    ):
        self._node = delegate_cls(
            name=name,
            source=source,
            schema=schema,
            format=format,
            description=description,
        )

        self._link = delegate_cls(
            name=name,
            source=link,
            schema=schema,
            format=format,
            description=description,
        )

    @property
    def node(self) -> DataNode:
        return self._node

    @property
    def link(self) -> DataNode:
        return self._link
