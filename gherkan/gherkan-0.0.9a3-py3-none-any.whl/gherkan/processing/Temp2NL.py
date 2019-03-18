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

CZ_PROGRAM_DICT_DIR = os.path.join(c.PROJECT_ROOT_DIR, "gherkan/utils", "RobotPrograms_cz.json")
EN_PROGRAM_DICT_DIR= os.path.join(c.PROJECT_ROOT_DIR, "gherkan/utils", "RobotPrograms_en.json")
GENERAL_YAML_DIR = os.path.join(c.PROJECT_ROOT_DIR, "gherkan/utils", "en-cz_phrases.yaml")

class FillActions:
    def __init__(self):
        self.finetune = Finetuner()

    def ParseMainAction(self, data):
        """ Construct basic NL phrase from given template
            Input format of data:
            data = [Name, VarsVals, Type, Values, TempStr]
            Name = string; name of the template
            VarsVals = list of strings; specific values to fill into template
            Type = "edge"/"bool"/"force"/"equality"
            Values = list of integers; values for given Types
            TempStr = string; specific details for given template
        """
        actor = ""
        self.data = self.convert_to_dic(data)
        lang = self.data["language"]
        values = self.data["vars"]
        inclinations = self.data["inclinations"]

        ## We suppose that templates with robot actions have PN in their name
        if "PN" in self.data["tempName"]:
                phrase = self.data["tempToNL"]
                string = str(self.data['vars']['subject'][1:])  # we leave out the first letter in case it is upper
                subject = (re.findall('([A-Z0-9].*)', string)) # separate actor specification (if exists), i.e. XY
                if subject:
                    subject = subject[0]
                action = self.MatchAction(lang, subject, self.data['vars']['value'])
                verb = self.finetune.find_verb(lang, action)
                if verb:
                    conj_verb = " " + self.finetune.conjugate(lang, verb[0], 3) + " "  # conjugate verb to third person
                    action = re.sub(verb[0], conj_verb, action)
                if subject:
                    subject = self.data['vars']['subject'].replace(subject[0], " " + subject[0])  # separate actor general name, i.e. shuttle
                    self.data["vars"]["subject"] = subject
                self.data["vars"]["value"] = action
                for key, value in values.items():
                      to_replace = re.compile(r"\(\?P\<{}\>[^\)]+\)".format(key))
                      phrase = re.sub(to_replace, value, phrase)
                phrase = self.finetune.strip_extra_spaces(phrase)
        else:
                phrase = self.data["tempToNL"]
                subject = values["subject"]
                if not subject.isupper():
                    string = str(subject[1:]) # we leave out the first letter in case it is upper
                    actor = (re.findall('([A-Z0-9].*)', string))   # separate actor specification (if exists), i.e. XY
                if actor:
                   actor = actor[0]
                   actor_name = subject.replace(actor, "")  # separate actor general name, i.e. shuttle
                else:
                      actor_name = subject
                      actor = ""
                values["subject"] = " ".join([actor_name,actor])
                for key, value in values.items():
                      idx = list(values).index(key)
                      value = self.MatchGeneral(lang, value)
                      if inclinations[idx] != 0:
                       value = self.finetune.conjugate(lang, value, inclinations[idx])
                      to_replace = re.compile(r"\(\?P\<{}\>[^\)]+\)".format(key))
                      phrase = re.sub(to_replace, value, phrase)
                for word in phrase.split():
                    word_new = self.MatchGeneral(lang, word)  # translate words to czech
                    phrase = re.sub(word, word_new, phrase)
                verb = self.finetune.find_verb(lang, phrase)
                if verb:
                  verb_conj = " " + self.finetune.conjugate(lang, verb[0], 3) + " "  # conjugate verb to third person
                  phrase = re.sub(verb[0], verb_conj, phrase)
                phrase = self.finetune.strip_extra_spaces(phrase)
                phrase = self.finetune.align_adjectives(lang, phrase)


        #TODO equality check and so on put to constants
        if phrase:
            data.__dict__["niceStr"] = phrase
        else:
            data.__dict__["niceStr"] = self.data["niceStr"]
            print(colored("Failed to create NL description for following actions: {}".format(self.data["niceStr"]), "yellow"))


    def ParseBool_Robot(self, lang, data, phrase=None):
        """ Return start or end for given bool value """
        if not phrase:
          phrase = ""
        phrase_spec = ""
        if lang == "en":
            if "start" in data[4].lower():
                if data[3] == "1":
                    phrase_spec = ' '.join(["starts the program", phrase])
                elif data[3] == "0":
                    phrase_spec = ' '.join(["does not start the program", phrase])
            elif "end" in data[4].lower():
                if data[3] == "1":
                    phrase_spec = ' '.join(["finishes program", phrase])
                elif data[3] == "0":
                    phrase_spec = ' '.join(["does not finish the program", phrase])
        elif lang =="cz":
            if "start" in data[4].lower():
                if data[3] == "1":
                    phrase_spec = ' '.join(["začne program", phrase])
                elif data[3] == "0":
                    phrase_spec = ' '.join(["nezačne program", phrase])
            elif "end" in data[4].lower():
                if data[3] == "1":
                    phrase_spec = ' '.join(["skončí program", phrase])
                elif data[3] == "0":
                    phrase_spec = ' '.join(["neskončí program", phrase])

        return phrase_spec

    def convert_to_dic(self, lists):
        data = lists.__dict__
        # return [str(el) if not isinstance(el, list) else self.convert_to_str(el) for el in lists]
        return data

    def strip_extra_spaces(self, text):
        stripped_spaces = re.sub(' +', ' ', text)
        stripped_text = stripped_spaces.strip()
        return stripped_text

    def ParseNegative(self, phrase):
        eng_phrase = phrase[0]
        czech_phrase = phrase[1]

        czech_phrase.replace("skončí", "neskončí")
        czech_phrase.replace("začne", "nezačne")
        eng_phrase.replace("finishes", "does not finish")
        eng_phrase.replace("starts", "does not start")

        return self.eng_phrase, self. czech_phrase

    def MatchAction(self, lang, actor, prog):
        """ Load robot actions and return sring for given program number """
        if lang == "en":
            with open(EN_PROGRAM_DICT_DIR, 'r') as stream:
                action_list = json.load(stream)
                try:
                  action = action_list[actor.lower()][str(prog)]
                except:
                  action = "execute program {}".format(prog)
                  print(colored("Warning: Did not find program {} for robot {} in English".format(prog, actor), "yellow"))

        elif lang == "cs":
            with open(CZ_PROGRAM_DICT_DIR, 'r') as stream:
                action_list = json.load(stream)
                try:
                   action = action_list[actor.lower()][str(prog)]
                except:
                  action = "vykonat program {}".format(prog)
                  print(colored("Warning: Did not find program {} for robot {} in Czech".format(prog, actor), "yellow"))

        return action

    def MatchGeneral(self, lang, word):
        """ Return nice string for basic form of a word """
        with open(GENERAL_YAML_DIR, 'r') as stream:
            phrase_list = yaml.load(stream)
            try:
              phrase = phrase_list[lang][word.lower()]
            except:
                phrase = word
        return phrase



if __name__=="__main__":
    fill_action = FillActions()