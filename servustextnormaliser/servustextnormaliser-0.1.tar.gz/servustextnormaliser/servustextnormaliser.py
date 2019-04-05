#!/usr/bin/env python3

from removeurl import remove_url
from removeaccents import remove_accents

from servussimplifytext import simplify_text, simplify_text_no_symbols

from contractions import fix


class TextNormaliser:
    def __init__(
        self,
        remove_accents: bool = True,
        remove_links: bool = True,
        remove_contractions: bool = True,
        no_symbols: bool = True,
        remove_non_ascii_characters: bool = True
            ) -> None:
        self.remove_accents = remove_accents
        self.remove_links = remove_links
        self.remove_contractions = remove_contractions
        self.no_symbols = no_symbols
        self.remove_non_ascii_characters = remove_non_ascii_characters

    def normalise(self, text: str) -> str:
        # We remove tildes before strange symbols.
        if self.remove_accents:
            text = remove_accents(text)

        if self.remove_links:
            text = remove_url(text)

        if self.remove_contractions:
            text = fix(text)

        if self.remove_non_ascii_characters:
            if self.no_symbols:
                text = simplify_text_no_symbols(text)
            else:
                text = simplify_text(text)

        return text
