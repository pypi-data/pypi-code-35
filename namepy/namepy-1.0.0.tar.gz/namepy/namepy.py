from random import choice

from lexicon import adjectives
from lexicon import nouns


def name():
    """
    This method returns a name separated by hyphens if longer than one word.

    :return: (String) Generated name
    """
    return '-'.join([choice(adjectives), choice(nouns)])
