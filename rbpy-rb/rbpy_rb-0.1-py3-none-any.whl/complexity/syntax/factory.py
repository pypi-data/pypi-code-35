from typing import List

from rb.complexity.complexity_index import ComplexityIndex
from rb.complexity.syntax.dep import DepIndex
from rb.complexity.syntax.dep_enum import DepEnum
from rb.core.lang import Lang


def create(lang: Lang) -> List[ComplexityIndex]:
    result = [DepIndex(lang, dep) for dep in DepEnum]
    return result
