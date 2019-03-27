import sys
import os

from gherkan.utils import constants as c

TAGGER_PATH = os.path.join(c.PROJECT_ROOT_DIR, "gherkan", "morphodita", "czech-morfflex-pdt-161115", "czech-morfflex-pdt-161115.tagger")

from ufal.morphodita import *


class CZMorph():
    def __init__(self):
        self.load_tagger()

    def get_pos_info(self, text):
        analysed = []
        forms = Forms()
        lemmas = TaggedLemmas()
        tokens = TokenRanges()
        # Tag - tags explanations at http://ufal.mff.cuni.cz/pdt2.0/doc/manuals/en/m-layer/html/ch02s02s01.html
        self.tokenizer.setText(text)
        while self.tokenizer.nextSentence(forms, tokens):
          self.tagger.tag(forms, lemmas)
          for i in range(len(lemmas)):
            lemma = lemmas[i]
            token = tokens[i]
            pos = self.encode_entities(lemma.tag[0])
            pos_det = self.encode_entities(lemma.tag[1])
            gender = self.encode_entities(lemma.tag[2])
            num = self.encode_entities(lemma.tag[3])
            case = self.encode_entities(lemma.tag[4])
            # poss_gender = self.encode_entities(lemma.tag[5])
            # poss_num = self.encode_entities(lemma.tag[6])
            person = self.encode_entities(lemma.tag[7])
            # tense = self.encode_entities(lemma.tag[8])
            negation = self.encode_entities(lemma.tag[10])

            analysed.append({"word":self.encode_entities(text[token.start : token.start + token.length]),"pos": pos,
                             "pos_det":pos_det, "case":case, "num":num, "person":person, "gender":gender, "negate":negation})
        return analysed

    def encode_entities(self,text):
      return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

    def load_tagger(self):
        self.tagger = Tagger.load(TAGGER_PATH)
        self.tokenizer = self.tagger.newTokenizer()
        if self.tokenizer is None:
          sys.stderr.write("No tokenizer is defined for the supplied model!")
          sys.exit(1)

