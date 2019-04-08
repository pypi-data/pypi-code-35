import re

import baconator


def test_genearte():
    name = baconator.generate()
    assert re.fullmatch(r'([a-z]+\-){2,3}\d{4}', name, re.I)


def test_generate_with_custom_delimiter():
    name = baconator.generate(delimiter='@@')
    assert re.fullmatch(r'([a-z]+@@){2,3}\d{4}', name, re.I)


def test_generate_with_custom_token_len():
    name = baconator.generate(token_len=6)
    assert re.fullmatch(r'([a-z]+\-){2,3}\d{6}', name, re.I)


def test_generate_without_token():
    name = baconator.generate(token_len=0)
    assert re.fullmatch(r'[a-z]+\-[a-z]+(\-[a-z])?', name, re.I)
