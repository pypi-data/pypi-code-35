"""
This class aligns natural language phrases into their most default forms and matches them
with niceStr parameters located in templates_dic.yaml. Returns an object (like SignalPhrase) with selected template and
filled as many fields from the dic as possible.
"""
import yaml, os, re
import gherkan.utils.constants as c
from gherkan.utils.word_morpho import Finetuner
TEMPLATES_DIC = os.path.join(c.PROJECT_ROOT_DIR, "gherkan/utils", "templates_dic.yaml")

class NLTempMatcher():
    def __init__(self):
        self.temp_dic = self.open_yaml(TEMPLATES_DIC)
        self.finetune = Finetuner()

    def find_temp(self, phrase):
        phrase = self.unify_synonyms(phrase)

        for step in range(len(phrase.split())):
            phrase = self.tag_text(phrase)
            if self.match_with_temps(phrase) == True:
                break
            else:
                continue


    def open_yaml(self, path):
        with open(path, 'r') as stream:
            temp_dic = yaml.load(stream)
        return temp_dic

    def detect_valtype(self, phrase):
        pass

    def detect_negative(self, phrase):

    def tag_text(self, text):
        pass

    def unify_synonyms(self, text):
        pass

    def match_with_temps(self, phrase):
        re.findall(phrase, self.temp_dic)  # generally

        if successful:
            return True

        if fail:
            return False

















if __name__ == "__main__":
   match_temp = NLTempMatcher()