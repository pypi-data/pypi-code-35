from random import choice
import logging

from .dictionaries import words, languages

logger = logging.getLogger(__name__)


def get_random_words(lang: str = "en") -> str:
    """Function returns a string with random set of three words form selected language (default is english).
    Words are chosen from built in dictionary and capitalized.
    The first one is an adverb, the second is an adjective and the third is a noun.

    Raises ValueError if chosen language is not supported.
    """
    if lang in languages:
        adv = str.rstrip(choice(words.get(lang).get("adverbs"))).capitalize()
        adj = str.rstrip(choice(words.get(lang).get("adjectives"))).capitalize()
        nou = str.rstrip(choice(words.get(lang).get("nouns"))).capitalize()

        if lang == "pl" and nou[-1] == "a":
            return_string = adv + adj[:-1] + "a" + nou
        else:
            return_string = adv + adj + nou

        return return_string
    else:
        logger.error(f"Value: '{lang}' is not a supported language.")
        raise ValueError

