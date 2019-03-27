# -*- coding: utf-8 -*-
"""
This class aligns natural language phrases into their most default forms and matches them
with niceStr parameters located in templates_dic.yaml. Returns an dict with selected template and
filled as many fields from the dic as possible.
"""
import re, os, imp
from gherkan.utils.word_morpho import Finetuner
from pattern.en import parse, parsetree, lemma
import majka, yaml
import pkg_resources, json
import gherkan.utils.constants as c
from termcolor import colored
from gherkan.utils import logging_types
import logging

GENERAL_YAML_DIR = os.path.join(c.PROJECT_ROOT_DIR, "gherkan/utils", "en-cz_phrases.yaml")

class NLTempMatcher():
    def __init__(self, lang):
        self.finetune = Finetuner(lang)
        self.NLPhrase = None
        self.lang = lang
        self.subj_of_interest = c.SUBJ_OF_INTEREST
        self.program_dic = self.load_program_dic()
        self.morph_lwt = majka.Majka(os.path.join(imp.find_module("gherkan")[1], "utils/majka.l-wt"))
        self.morph_wlt = majka.Majka(os.path.join(imp.find_module("gherkan")[1], "utils/majka.w-lt"))

    def get_NLPhrase(self, phrase):
        negative = self.get_negative(phrase)
        force = self.get_force(phrase)
        state, phrase = self.get_state(phrase)
        clean_phrase = self.get_cleanphr(phrase, negative, force)
        if self.lang == "en":
          clean_phrase = self.lemmatize(clean_phrase)
        pn = self.get_pn(clean_phrase)
        if pn:
            clean_phrase = pn
        else:
            clean_phrase = self.lemmatize(clean_phrase)
            clean_phrase = self.translate(self.finetune.strip_extra_spaces(clean_phrase))
        clean_phrase = self.finetune.strip_extra_spaces(clean_phrase)
        self.NLPhrase = {"tempToNL": clean_phrase,
                         "negate": negative,
                         "force": force,
                         "state": state
                         }
        return self.NLPhrase

    def get_pn(self, phrase):
        if self.lang == "en":
            tree = parsetree(phrase, tokenize=True,
                             tags=True, chunks=True, relations=True)
            for sentence in tree:
                try:
                 actor = str(sentence.subjects[0]).lower()
                except:
                   actor = sentence.string
            if len(actor.split()) > 2:
                actor_new = re.findall(r'({}\s+([a-z]+)*([0-9])*([a-z]+)*)'.format(self.subj_of_interest), actor, re.IGNORECASE)
                try:
                    actor = actor_new[0][0]
                except:
                    pass
            action_lemma = self.lemmatize("".join(phrase.lower().rsplit(actor)))
        elif self.lang == "cs":
                actor = re.findall(r'({}\s+(([a-z]+)*([0-9])*|([0-9])*([a-z]+)*))\s'.format(self.subj_of_interest),
                                   phrase, re.IGNORECASE)
                if not actor:
                    actor = self.subj_of_interest
                else:
                    actor = actor[0][0]
                action_lemma = "".join(phrase.lower().rsplit(actor))
                verb = self.finetune.find_verb(self.lang, action_lemma)
                if verb:
                  verb_lemma = self.finetune.lemmatize(self.lang, verb[0])
                  action_lemma = re.sub(verb[0], verb_lemma, action_lemma)
        if actor.lower() == self.subj_of_interest:  # if no specification, use the one defined in Feature
            for key in self.program_dic:
                for value in self.program_dic[key]:
                 if self.finetune.strip_extra_spaces(action_lemma) in self.program_dic[key][value]:
                    phrase = "{} #{}".format(key, value) # internal format for program numbers in NL
                    return phrase
        elif actor in self.program_dic.keys():
            for key in self.program_dic[actor]:
                if self.finetune.strip_extra_spaces(action_lemma) in self.program_dic[actor][key]:
                    phrase = "{} #{}".format(actor, key) # internal format for program numbers in NL
                    return phrase
        return False

    def translate(self, phrase):
        new_phrase = phrase
        with open(GENERAL_YAML_DIR, 'r', encoding="utf-8") as stream:
            try:
                vocab = yaml.load(stream)
            except:
                logging.debug("Could not load en-cz_phrases")
        for word in phrase.split():
            for key in vocab["cs"]:
              if word.lower() == vocab['cs'][key]:
                  word_en = key
                  new_phrase = re.sub(r'\b{}\b'.format(word), word_en, new_phrase, re.IGNORECASE)
        return new_phrase

    def get_state(self, phrase):
        stop_phrases=["end", "ends", "ended", "ending", "finish", "finishes", "stops", "finished", "stopped",
                      "stop", "skončit", "dokončit", "přestat"]
        start_phrases=["start", "starts", "started", "starting", "začít"]
        for word in phrase.split():
            if self.finetune.lemmatize(self.lang, word).lower() in stop_phrases:
               phrase = re.sub(word, '', phrase, re.IGNORECASE)
               state = "End"
               return state, phrase
            elif self.finetune.lemmatize(self.lang, word).lower() in start_phrases:
                phrase = re.sub(word, '', phrase, re.IGNORECASE)
                state = "Start"
                return state, phrase
        state = None
        return state, phrase

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
                    negative = re.findall(
                        r'\b(not)\b\s+\b({})\b|(\b({})\b)\s\b(not)\b'.format(verb, verb), phrase)
                    if not self.empty_tree(negative):
                        negative = True
                    else:
                        negative = False
            else:
                negative = False
        elif self.lang == "cs":
            negative = False
            verbs = self.finetune.find_verb(self.lang, phrase)
            if verbs:
                for verb in verbs:
                    verb_info = self.finetune.get_txt_info(verb)
                    if verb_info[0]["negate"] == "N":
                        negative = True
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
                            action_cl = re.sub(r'^\b({})\b\s'.format(
                                i), "", sent.verbs[0].string)
                            phrase = self.finetune.strip_extra_spaces(phrase)
                            phrase = re.sub(
                                sent.verbs[0].string, action_cl, phrase)
        elif self.lang == "cs":
            if force == True:
              phrase = re.sub(r'\b(vynuť)\b', '', phrase, re.IGNORECASE)
            if negative == True:
                verbs = self.finetune.find_verb(self.lang, phrase)
                if verbs:
                    for verb in verbs:
                        verb_info = self.finetune.get_txt_info(verb)
                        if verb_info[0]["negate"] == "N":
                            verb_new = re.sub(r"^(ne)","", verb, re.IGNORECASE)
                            phrase = re.sub(verb, verb_new, phrase, re.IGNORECASE)

        phrase = self.finetune.strip_extra_spaces(phrase)
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
                   lemmas += " "
                   if output:
                     lemma_det = output[0]['lemma']
                   else:
                         lemma_det = word
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
            file = "utils/RobotPrograms_cs.json"
        with pkg_resources.resource_stream("gherkan", file) as stream:
            try:
                program_dic = json.load(stream)
            except:
                logging.debug("Could not load {}".format(file))
        return program_dic


if __name__ == "__main__":
    match_temp = NLTempMatcher()
