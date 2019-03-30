
import unittest
from inlp.pos import *
from inlp import tokenize
import copy






@unittest.skip("showing class skipping")
class KonlpyTestCase(unittest.TestCase):

    #@unittest.skip("demonstrating skipping")
    def test_postag(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        text = "[나꼼수 레전드편] 나꼼수 나와서 털리는 홍준표 (김어준,주진우,정봉주,김용민)__[이명박]"
        k = Konlpy(text, lang='korean')
        k.postag()
        print(f"\n\n k.postags :\n\n{k.postags}")

    #@unittest.skip("demonstrating skipping")
    def test_remove_useless_words_and_get_nouns(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        text = "[나꼼수 레전드편] 나꼼수 나와서 털리는 홍준표 (김어준,주진우,정봉주,김용민)__[이명박]"
        k = Konlpy(text, lang='korean')
        nouns = k.postag().remove_useless_words_and_get_nouns()
        print(f"\n\n k.postagdf :\n\n{k.postagdf}")
        print(f"\n\n nouns :\n\n{nouns}")

@unittest.skip("showing class skipping")
class NLTKTestCase(unittest.TestCase):

    text = "An A-Z Index of the Apple macOS (OSX) command line - SS64 Command line reference"

    @unittest.skip("demonstrating skipping")
    def test_remove_useless_words_and_get_nouns(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        n = NLTK(self.text, lang='latin')
        nouns = n.postag().remove_useless_words_and_get_nouns()
        print(f"\n\n n.postagdf :\n\n{n.postagdf}")
        print(f"\n\n nouns :\n\n{nouns}")

    #@unittest.skip("demonstrating skipping")
    def test_deduplicate(self):
        print(f"\n{'='*60}\n {__class__.__name__} : {inspect.stack()[0][3]}\n")
        n = NLTK(self.text, lang='latin')
        nouns = n.postag()
        n.convert_to_postagdf()
        print(f"\n\n n.postagdf :\n\n{n.postagdf}")
        t = tokenize.TokenRemover(n.lang)
        n.postagdf = t.process_in_df(n.postagdf)
        print(f"\n\n n.postagdf :\n\n{n.postagdf}")
        df = n.deduplicate(n.postagdf)
        print(f"\n df :\n\n{df}\n")







def main():
    unittest.main()
