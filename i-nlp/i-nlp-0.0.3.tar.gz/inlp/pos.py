
from . import tokenize
import pandas as pd
import re
from nltk import pos_tag
from konlpy.tag import Hannanum


class PosTag():

    def __init__(self, text, lang):
        self.text = text
        self.lang = lang
        self.postags = []

    def convert_to_postagdf(self):
        df = pd.DataFrame({'postags':self.postags})
        df['word'] = df.postags.apply(lambda x: x[0])
        df['pos'] = df.postags.apply(lambda x: x[1])
        del(df['postags'])
        self.postagdf = df

    def deduplicate(self, df):
        df = df.sort_values('word')
        df['lower'] = df.word.apply(lambda x: x.lower())
        return df.drop_duplicates(keep='first', subset=['lower'])

    def get_nouns(self):
        if len(self.postagdf) is 0:
            return []
        else:
            df = self.postagdf
            df1 = df[ df.pos.str.contains(pat=r'^N') ]
            # 중복제거.
            df1 = self.deduplicate(df1)
            return list(df1.word)

    # 명사에서 일반화하자.
    def get_words(self, pos_pat=r'^N'):
        if len(self.postagdf) is 0:
            self.words = []
        else:
            df = self.postagdf
            df1 = df[ df.pos.str.contains(pat=pos_pat) ]
            # 중복제거.
            words = list(df1.word)
            if pos_pat is r'^N':
                words = [w.capitalize() for w in words]
            self.words = list(set(words))

    def remove_useless_words_and_get_nouns(self):
        self.convert_to_postagdf()
        t = tokenize.TokenRemover(self.lang)
        self.postagdf = t.remove_in_df(self.postagdf)
        return self.get_nouns()

class NLTK(PosTag):

    def __init__(self, text, lang='latin'):
        super().__init__(text, lang)

    def postag(self):
        t = tokenize.Tokenizer(self.text)
        t.word_tokenize()
        self.postags = pos_tag(t.tokens)
        return self

class Konlpy(PosTag):

    def __init__(self, text, lang='korean'):
        super().__init__(text, lang)

    def postag(self):
        # 토큰화 + 품사태깅.
        hannanum = Hannanum()
        self.postags = hannanum.pos(self.text)
        return self
