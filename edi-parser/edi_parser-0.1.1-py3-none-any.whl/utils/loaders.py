import json
from typing import TextIO


def load_template(file: str) -> dict:
    with open('../templates/' + file + '.json', encoding='utf-8') as file:
        return json.load(file)


def load_file(file: TextIO) -> dict:
        return json.load(file)
