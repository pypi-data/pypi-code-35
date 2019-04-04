#!/usr/bin/env python3

__accents_translation_table = str.maketrans(
    "áéíóúýàèìòùỳâêîôûŷäëïöüÿÁÉÍÓÚÝÀÈÌÒÙỲÂÊÎÔÛŶÄËÏÖÜŸ",
    "aeiouyaeiouyaeiouyaeiouyAEIOUYAEIOUYAEIOUYAEIOUY"
    )


def remove_accents(text: str) -> str:
    """
    Replace tildes with letters without them.

    :param text: str: Text which tildes needs to be replaced..

    """
    return text.translate(__accents_translation_table)
