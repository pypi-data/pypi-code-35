import logging


from dataclasses import dataclass
from typing import List
from .extract import Extract

@dataclass
class Config:
    extracts: List[Extract]
    output_path: str
    mailmap_file: str
    logging:int = logging.INFO

