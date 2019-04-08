from typing import List

from rb.complexity.complexity_index import ComplexityIndex
from rb.complexity.surface.no_words import NoWordsIndex
from rb.core.lang import Lang


def create(lang: Lang) -> List[ComplexityIndex]:
    return [NoWordsIndex(lang)]
