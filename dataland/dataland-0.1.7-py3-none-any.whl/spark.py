import os
import types
from functools import wraps
from typing import List, Optional, Union

import pyspark.sql.functions as F
from pyspark import SparkConf
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StringType

from .base import DataNode


class SparkDFNode(DataNode):
    def _default_spark_config(self, **configs):
        scfg = SparkConf()

        user = os.environ.get("USER", "")
        scfg.set(
            "spark.sql.warehouse.dir", os.path.join(f"/tmp/{user}", "spark-warehouse")
        )

        for k, v in configs.items():
            scfg.set(k, v)

        return scfg

    def load(
        self,
        fullpaths: Union[str, List[str]] = None,
        ss: Optional[SparkSession] = None,
        scfg: Optional[SparkConf] = None,
        **read_options,
    ) -> DataFrame:

        if ss is None:
            cfg = dict(scfg.getAll()) if isinstance(scfg, SparkConf) else {}
            scfg = self._default_spark_config(**cfg)

            ss = SparkSession.builder.config(conf=scfg).getOrCreate()

        if "format" not in read_options:
            read_options["format"] = self.data.format
        if "schema" not in read_options:
            read_options["schema"] = self.data.schema

        return ss.read.load(fullpaths or self.data.source.fullpath, **read_options)

    def dump(self, sdf: DataFrame, destination=None, **write_options) -> None:
        """"""

        if "mode" not in write_options:
            write_options["mode"] = "overwrite"
        if "format" not in write_options:
            write_options["format"] = self.data.format

        sdf.write.save(destination or self.data.source.fullpath, **write_options)


def _copy_func(f, name: str = ""):
    """Copy a function object.

    Args:
        name (str): Give the copied function a new name, or use the original function's name

    Returns:
        Copied function object
    """

    fn = types.FunctionType(
        f.__code__, f.__globals__, name or f.__name__, f.__defaults__, f.__closure__
    )

    # In case f was given attrs (note this dict is a shallow copy):
    fn.__dict__.update(f.__dict__)

    return fn


def udfy(fn=None, return_type=StringType()):
    """A wrapper to provide additional spark udf interface to arbitrary python function.

    In python, invoke function by `my_function(a, b)`,
    then in spark context, invoke udf by `my_function.udf('col-a', 'col-b')`,
    additionally, keyword arguments can be overrided by "dynamic udf interface",
    e.g., invoke `my_function.dudf(some_keyword=other_value)('col-a', 'col-b')`

    Args:
        fn (FunctionType): function to wrap
        return_type (DataType): the spark data type the wrapped function should return

    Examples:

        >>> @udfy(return_type=FloatType())
            def foo(val, offset=2, mult=3):
                return float(val * mult + offset)

        >>> foo(8)
        26.0

        >>> sdf = spark.range(10)
        >>> sdf.show(3)
        +---+
        | id|
        +---+
        |  0|
        |  1|
        |  2|
        +---+
        only showing top 3 rows

        >>> sdf.select(foo.udf('id')).show(3)
        +-------+
        |foo(id)|
        +-------+
        |    2.0|
        |    5.0|
        |    8.0|
        +-------+
        only showing top 3 rows

        >>> sdf.select(foo.dudf(mult=11, offset=-5)('id')).show(3)
        +-------+
        |foo(id)|
        +-------+
        |   -5.0|
        |    6.0|
        |   17.0|
        +-------+
        only showing top 3 rows

    Returns:
        Wrapped function object

    """

    def wrap(f):
        @wraps(f)
        def outer(**kwargs):
            @wraps(f)
            def inner(*args):
                return f(*args, **kwargs)

            return F.udf(inner, returnType=return_type)

        # Use some hacky deepcopy trick to avoid `AssertionError` while pickling
        fcopied = _copy_func(f)

        fcopied.udf = outer()
        fcopied.dudf = outer

        return fcopied

    if fn is None:
        return wrap

    else:
        return wrap(fn)
