# -*- coding: utf-8 -*-
"""
This class aligns natural language phrases into their most default forms and matches them
with niceStr parameters located in templates_dic.yaml. Returns an dict with selected template and
filled as many fields from the dic as possible.
"""
import re
from gherkan.utils.word_morpho import Finetuner
from pattern.en import parse, parsetree, lemma
import majka
import pkg_resources, json



class NLTempMatcher():
    def __init__(self, lang):
        self.finetune = Finetuner()
        self.NLPhrase = None
        self.lang = lang
        self.program_dic = self.load_program_dic()

    def get_NLPhrase(self, phrase):
        negative = self.get_negative(phrase)
        force = self.get_force(phrase)
        clean_phrase = self.get_cleanphr(phrase, negative, force)
        clean_phrase = self.lemmatize(clean_phrase)
        pn = self.get_pn(clean_phrase)
        if pn:
            clean_phrase = pn
        clean_phrase = self.finetune.strip_extra_spaces(clean_phrase)
        self.NLPhrase = {"tempToNL": clean_phrase,
                         "negate": negative,
                         "force": force
                         }
        return self.NLPhrase

    def get_pn(self, phrase):
        tree = parsetree(phrase, tokenize=True,
                         tags=True, chunks=True, relations=True)
        for sentence in tree:
            try:
             actor = str(sentence.subjects[0]).lower()
            except:
                return False
        action_lemma = self.lemmatize("".join(phrase.rsplit(actor)))
        if actor in self.program_dic.keys():
            for key in self.program_dic[actor]:
                if self.finetune.strip_extra_spaces(action_lemma) in self.program_dic[actor][key]:
                    phrase = " ".join([actor, "program number be", key])
                    return phrase
        return False

    def get_force(self, phrase):
        if self.lang == 'en':
           force = re.findall(r'\b(force)\b', phrase, re.IGNORECASE)
        elif self.lang == 'cs':
            no_diacritics = self.finetune.remove_diacritics(phrase)
            force = re.findall(r'\b(vynut)\b', no_diacritics, re.IGNORECASE)
        if not self.empty_tree(force):
            force = True
        else:
            force = False
        return force

    def get_negative(self, phrase):
        verbs = self.finetune.find_verb(self.lang, phrase)
        if self.lang == "en":
            if verbs:
                for verb in verbs:
                    negative = re.findall(r'\b(not)\b\s+\b({})\b|(\b({})\b)\s\b(not)\b'.format(verb, verb), phrase)
                    if not self.empty_tree(negative):
                        negative = True
                    else:
                        negative = False
            else:
                negative = False
        elif self.lang == "cs":
            if verbs:
                for verb in verbs:
                    pass

        return negative

    def get_cleanphr(self, phrase, negative=None, force=None):
        # clean the phrase from negatives and force
        if self.lang == "en":
            if negative == True:
              phrase = re.sub(r'\b(not)\b', '', phrase)
            if force == True:
              phrase = re.sub(r'\b(force)\b', '', phrase)

            # remove excess verb words
            for sent in parsetree(phrase, tags=True, chunks=True, relations=True, lemmas=True):
                del_words = ["do", "will", "can", "must", "have to"]
                if sent.verbs:
                    for i in sent.verbs[0].string.split():
                        if lemma(i) in del_words:
                            action_cl = re.sub(r'^\b({})\b\s'.format(i), "", sent.verbs[0].string)
                            phrase = self.finetune.strip_extra_spaces(phrase)
                            phrase = re.sub(sent.verbs[0].string, action_cl, phrase)
        elif self.lang == "cs":
          pass

        phrase = self.finetune.strip_extra_spaces(phrase)
        # print(parse(clean_phrase, relations=True, lemmata=True))
        return phrase

    def empty_tree(self, input_list):
        """Recursively iterate through values in nested lists."""
        for item in input_list:
            if not isinstance(item, list) or not self.empty_tree(item):
                return False
        return True

    def lemmatize(self, text):
        lemmas = ""
        skip_list = [",", ".", ";"]
        if self.lang == "cs":
            self.morph_wlt.flags |= majka.ADD_DIACRITICS  # find word forms with diacritics
            self.morph_wlt.tags = False  # return just the lemma, do not process the tags
            self.morph_wlt.first_only = True  # return only the first entry
            for word in text.split():
               if word in skip_list:
                   pass
               else:
                   output = self.morph_wlt.find(word)
                   lemma_det = output[0]['lemma']
                   lemmas += " "
                   lemmas += lemma_det

        elif self.lang == "en":
            # this version keeps capitals
            tree = parsetree(text, tokenize=True)

            for sentence in tree:
                for word in sentence:
                    if word.string in skip_list:
                        pass
                    else:
                        lemmas += " "
                    lemmas += lemma(word.string)

        return lemmas

    def load_program_dic(self):
        # load program json
        if self.lang == "en":
            file = "utils/RobotPrograms_en.json"
        elif self.lang == "cs":
            file = "utils/RobotPrograms_cz.json"
        with pkg_resources.resource_stream("gherkan", file) as stream:
            try:
                program_dic = json.load(stream)
            except:
                print("Could not load {}".format(file))
        return program_dic


if __name__ == "__main__":
   match_temp = NLTempMatcher()
