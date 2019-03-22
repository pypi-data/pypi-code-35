# coding: utf-8
"""
Class FillActions turns the filled object SignalPhrase into a natural language phrase, which is then returned
as the filled fields niceStrEN and niceStrCZ in the SignalPhrase.
"""
import yaml, re, json
import os
from termcolor import colored
from gherkan.utils.word_morpho import Finetuner
import gherkan.utils.constants as c
from pattern.en import conjugate, PARTICIPLE

CZ_PROGRAM_DICT_DIR = os.path.join(c.PROJECT_ROOT_DIR, "gherkan/utils", "RobotPrograms_cz.json")
EN_PROGRAM_DICT_DIR= os.path.join(c.PROJECT_ROOT_DIR, "gherkan/utils", "RobotPrograms_en.json")
GENERAL_YAML_DIR = os.path.join(c.PROJECT_ROOT_DIR, "gherkan/utils", "en-cz_phrases.yaml")

class FillActions:
    def __init__(self):
        self.finetune = Finetuner()
        self.lang = None

    def ParseMainAction(self, data):
        """ Construct basic NL phrase from given template
            Input format of data:
            data = [Name, Vars, Values, TempToNL]
            Vars = list of strings; specific values to fill into template
            Values = list of integers; values for given Types
            TempToNL = string; specific details for given template
        """
        self.data = self.convert_to_dic(data)
        self.lang = self.data["language"]
        varz = self.data["vars"]
        values = self.data["values"]
        phrase = self.data["tempToNL"][-1]
        for key in varz:  # separate actor names (shuttleXY > shuttle XY)
              if not varz[key].isupper():
                 string = str(varz[key][1:])  # we leave out the first letter in case it is upper
                 actor = (re.findall('([A-Z0-9].*)', string))
                 if actor:
                     varz[key] = varz[key].replace(actor[0], " {}".format(actor[0]))
                 else:
                     pass
        for key, v in values.items():  # try to match the values with .json
                matched = self.MatchAction(varz['subject'], values[key])
                if matched:
                   values[key] = matched
                   to_replace = re.compile(r"\(\?P\<{}\>[^\)]+\)".format(key))
                   phrase = re.sub(to_replace, values[key], phrase)
                else:
                    phrase = self.ParseBool(phrase, values[key])
        for key, value in varz.items():  # match varz with template
            idx = list(varz).index(key)
            value = self.MatchGeneral(value)
            if self.data["inclinations"][idx] != 0:
                value = self.finetune.conjugate(self.lang, value, self.data["inclinations"][idx])
            to_replace = re.compile(r"\(\?P\<{}\>[^\)]+\)".format(key))
            phrase = re.sub(to_replace, value, phrase)
        verb = self.finetune.find_verb(self.lang, phrase)
        if verb:
          verb_conj = self.finetune.conjugate(self.lang, verb[0], 3) # conjugate verb to third person
          phrase = re.sub(verb[0], verb_conj, phrase)
        for word in phrase.split():
          word_new = self.MatchGeneral(word)  # translate words to czech
          phrase = re.sub(r'\b({})\b'.format(word), word_new, phrase)
        phrase = self.finetune.strip_extra_spaces(phrase)
        phrase = self.finetune.align_adjectives(self.lang, phrase)

        if phrase:
            data.__dict__["niceStr"] = phrase
        else:
            data.__dict__["niceStr"] = self.data["niceStr"]
            print(colored("Failed to create NL description for following actions: {}".format(self.data["niceStr"]), "yellow"))


    def ParseBool(self, phrase, value):
        """ Bool 1 is positive, Bool 0 negative (sth does not happen) """
        exceptions = ["be", "can", "will", "must"]
        if value:
            phrase_bool = phrase
        elif not value:
            verb = self.finetune.find_verb(self.lang, phrase)
            if verb:
                if self.lang == "cs":
                    phrase_bool = re.sub(verb[0], "".join(["ne", verb[0]]), phrase)
                elif self.lang == "en":
                    verb_lemma = self.finetune.lemmatize(self.lang, verb[0])
                    if verb_lemma in exceptions:
                        phrase_bool = re.sub(r'\b{}\b'.format(verb[0]),  " ".join([verb_lemma, "not"]), phrase)
                    else:
                        phrase_bool = re.sub(r'\b{}\b'.format(verb[0]), " ".join(["does not", verb_lemma]), phrase)
            else:
                phrase_bool = phrase
        return phrase_bool

    def ParseForce(self, phrase, value):
        if value:
            if self.lang == "en":
                phrase = " ".join(["force", phrase])
            elif self.lang == "cs":
                phrase = " ".join(["vynuť", phrase])
        elif not value:
            phrase = phrase
        return phrase

    def convert_to_dic(self, lists):
        data = lists.__dict__
        return data

    def strip_extra_spaces(self, text):
        stripped_spaces = re.sub(' +', ' ', text)
        stripped_text = stripped_spaces.strip()
        return stripped_text

    def start_stop(self, phrase, state):
        state = self.finetune.conjugate(self.lang, state.lower(), 3)
        verb = self.finetune.find_verb(self.lang, phrase)
        verb_new = verb[0]
        if verb:
            if self.lang == "cs":
                verb_new = self.finetune.lemmatize(self.lang, verb[0])
                print(verb_new)
            elif self.lang == "en":
                verb_new = conjugate(verb[0], tense=PARTICIPLE, parse=True)
            phrase = re.sub(verb[0], " ".join([state, verb_new]), phrase)
            return phrase
        else:
            return phrase

    def MatchAction(self, actor, prog):
        """ Load robot actions and return sring for given program number """
        if self.lang == "en":
            with open(EN_PROGRAM_DICT_DIR, 'r', encoding="utf-8") as stream:
                action_list = json.load(stream)
                try:
                  action = action_list[actor.lower()][str(prog)]
                except:
                    if actor.lower() in action_list:
                       action = "execute program {}".format(prog)
                       print(colored("Warning: Did not find program {} for robot {} in English".format(prog, actor), "yellow"))
                    else:
                        return False

        elif self.lang == "cs":
            with open(CZ_PROGRAM_DICT_DIR, 'r', encoding="utf-8") as stream:
                action_list = json.load(stream)
                try:
                   action = action_list[actor.lower()][str(prog)]
                except:
                    if actor.lower() in action_list:
                        action = "vykonat program {}".format(prog)
                        print(colored("Warning: Did not find program {} for robot {} in Czech".format(prog, actor), "yellow"))
                    else:
                        return False
        return action

    def MatchGeneral(self, word):
        """ Return nice string for basic form of a word """
        with open(GENERAL_YAML_DIR, 'r', encoding="utf-8") as stream:
            phrase_list = yaml.load(stream)
            try:
              phrase = phrase_list[self.lang][word.lower()]
            except:
                phrase = word
        return phrase



if __name__=="__main__":
    fill_action = FillActions()
