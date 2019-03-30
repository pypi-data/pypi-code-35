
from . import pos
import pandas as pd
import re
from konlpy.tag import Okt




class LatinHangulSpliter:

    def __init__(self, text):
        self.text = text
        self.latin_pat = '[a-zA-Z]+'
        self.parse_latin()
        self.parse_hangul()

    def parse_latin(self):
        strings = re.findall(pattern=self.latin_pat, string=self.text)
        self.latin = " ".join(strings)

    def parse_hangul(self):
        new_string, number_of_subs_made = re.subn(pattern=self.latin_pat, repl='', string=self.text)
        self.number_of_subs_made = number_of_subs_made
        new_string = new_string.strip().lstrip()
        self.hangul = self.remove_trace(new_string)

    def remove_trace(self, text):
        new_string, number_of_subs_made = re.subn(pattern='\(\s+\)', repl='', string=text)
        return new_string

class LatinHangulSpliter_v1(pos.PosTag):

    def __init__(self, text):
        super().__init__()
        self.text = text
        okt = Okt()
        self.postags = okt.pos(self.text)
        self.split_postags()
        df = self.postagdf
        self.latin = df.query('pos == "Alpha"')
        self.hangul = df.query('pos == "Foreign"')
