from fastai.text import *
import sentencepiece as spm


class LanguageTokenizer(BaseTokenizer):
    def __init__(self, lang: str):
        self.lang = lang
        self.sp = spm.SentencePieceProcessor()
        self.sp.Load(f'inltk/models/{lang}/tokenizer.model')

    def tokenizer(self, t: str) -> List[str]:
        return self.sp.EncodeAsPieces(t)


class SanskritTokenizer(LanguageTokenizer):
    def __init__(self, lang: str):
        LanguageTokenizer.__init__(self, lang)
