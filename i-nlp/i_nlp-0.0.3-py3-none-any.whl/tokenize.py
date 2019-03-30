
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk import word_tokenize, pos_tag, DefaultTagger
# 강제 태거.
default_tagger = DefaultTagger('NN')
import string
import re
from collections import Counter
import pandas as pd
import inspect


PYTHON_REGEX_METACHARS = ['.', '^', '$', '*', '+', '?', '{', '}', '[', ']', '\\', '|', '(', ')']
SPECIAL_CHARS = [
    '.', '…', '¿', '？', '¡', '！', '–', '·',#기본
    '（', '）', '《', '》', '】', '【',#괄호
    '′', '“', '”', "‘", "’",#따옴표
    '»','—', '―', '•',
    '｜', '|', ':', ':]',#구분자
]
SHAPE_CHARS = ['▶', '❤', '🏾',]
ADDI_STOPWORDS = ['vs','rt','via']

class Tokenizer:
    """토큰화 함수 자체는 영향을 미치지 못한다."""
    def __init__(self, text):
        self.text = text.replace('__', ', ')

    def word_tokenize(self):
        self.tokens = word_tokenize(self.text)
        return self.tokens

    def tweet_tokenize(self):
        self.tokens = TweetTokenizer().tokenize(self.text)
        return self.tokens

    # 최악의 결과
    def split_tokenize(self):
        self.tokens = self.text.split()
        return self.tokens

class PatternRemover:

    def __init__(self):
        text_removal_regexs = [
            '\.\.+|\.\s(\.\s)+',# 목차에서 페이지 번호 표시를 위한 연결된 점들.
            '\d+\.\d+|\d+\.\d+(\.\d+)+',# 목차에서 문서구조를 나타내는 번호트리.
        ]
        self.text_removal_regex = "|".join(text_removal_regexs)
        #self.ToC_numbering_regex = '\d+\.\d+'

        self.tokens = None
        self.token_removal_regexs = []
        self.specialchars = SPECIAL_CHARS.copy()
        self.metachars = PYTHON_REGEX_METACHARS.copy()
        self.produce_specialchars_regexs()

    def produce_specialchars_regexs(self):
        for sc in self.specialchars:
            if sc in self.metachars: sc = "\\" + sc
            else: sc += '+'
            self.token_removal_regexs.append(sc)

    def add_text_removal_regex(self, regex):
        self.text_removal_regex += ('|' + regex)

    def add_token_removal_regex(self, regex):
        self.token_removal_regexs.append(regex)

    def remove_matched_text(self):
        new_string, number_of_subs_made = re.subn(pattern=self.text_removal_regex, repl='', string=text)
        #print(f"\n\n new_string : {new_string}")
        return new_string

    def remove_matched_tokens(self):
        if self.tokens is not None:
            refined_tokens = []
            for regex in self.token_removal_regexs:
                p = re.compile(pattern=regex)
                for tok in self.tokens:
                    if p.match(string=tok) is None:
                        refined_tokens.append(tok)
            self.tokens = refined_tokens

class TokenRemover:
    """정확한 값에 의해서 제거"""
    def __init__(self, lang):
        self.lang = lang
        self.tokens = []
        self.stopwords = get_stopwords(self.lang)
        self.addi_stopwords = ['vs','rt','via']
        self.metachars = PYTHON_REGEX_METACHARS
        self.specialchars = SPECIAL_CHARS
        self.allwords = self.stopwords + self.addi_stopwords + self.metachars + self.specialchars
        self.TF = True
        self.leaving_single_chars = ['R']

    def remove_in_li(self, tokens):
        tokens = self.remove_digits(tokens)
        tokens = self.remove_allwords(tokens)
        tokens = self.remove_non_alphabets(tokens)
        tokens = self.remove_single_chars(tokens)
        return tokens

    def remove_in_df(self, df):
        df = self.remove_digits_in_df(df)
        df = self.remove_allwords_in_df(df)
        df = self.remove_non_alphabets_in_df(df)
        df = self.remove_single_chars_in_df(df)
        return df

    def remove_stopwords(self, tokens):
        return [tok for tok in tokens if tok not in self.stopwords]

    def remove_digits(self, tokens):
        return [tok for tok in tokens if tok.isdigit() is False]

    def remove_digits_in_df(self, df):
        if len(df) is 0: return df
        else: return df[ ~df.word.str.isdigit() ]

    def remove_non_alphabets(self, tokens):
        return [tok for tok in tokens if tok.isalpha() is True]

    def remove_non_alphabets_in_df(self, df):
        if len(df) is 0: return df
        else: return df[ df.word.str.isalpha() ]

    def remove_addi_stopwords(self, tokens):
        return [tok for tok in tokens if tok not in self.addi_stopwords]

    def remove_metachars(self, tokens):
        return [tok for tok in tokens if tokc not in self.metachars]

    def remove_specialchars(self, tokens):
        return [tok for tok in tokens if tok not in self.specialchars]

    def remove_allwords(self, tokens):
        return [tok for tok in tokens if tok not in self.allwords]

    def remove_allwords_in_df(self, df):
        if len(df) is 0: return df
        else: return df[ ~df.word.isin(self.allwords) ]

    def remove_single_chars(self, tokens):
        new_tokens = []
        for tok in tokens:
            if (len(tok) is 1) and (tok not in self.leaving_single_chars):
                pass
            else:
                new_tokens.append(tok)
        return new_tokens

    def remove_single_chars_in_df(self, df):
        if len(df) is 0: return df
        else:
            df['TF'] = df.word.apply(lambda x: True if len(x) is 1 else False)
            return df.query('TF == False')

def get_stopwords(lang='english'):
    if lang is 'korean':
        words = [
            '은','는','이','가',
            '을','를',
            '이','그','저',
            '에','에서','으로','으로부터','로부터',
        ]
    elif lang is 'latin':
        words = stopwords.words('english') + stopwords.words('spanish')
    else:
        words = stopwords.words(lang)
    return list(string.punctuation) + words

class TermFrequency:

    def report(text, lang='english'):
        t = Tokenizer(text)
        tokens = t.tweet_tokenize()
        tr = TokenRemover(lang)
        tokens = tr.process(tokens)
        c = Counter()
        c.update(tokens)
        # term-frequencies
        tfs = []
        for tag, count in c.most_common(len(c)):
            tfs.append({'word':tag, 'freq':count})

        df = pd.DataFrame(tfs).sort_values(by='freq', ascending=False)
        print(f"\n\n{'*'*60}\n\n {__class__.__name__} : {inspect.stack()[0][3]} \n\n{'*'*60}\n\n")
        print(f"\n df :\n\n{df}")
        return df
