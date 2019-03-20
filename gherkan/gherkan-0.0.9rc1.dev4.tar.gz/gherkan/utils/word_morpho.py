# coding: utf-8
# from googletrans import Translator
import majka, re, os, imp
from pattern.en import conjugate, parsetree
from termcolor import colored

class Finetuner():

    def conjugate(self, lang, word, person, number="singular"):
        """  Returns provided noun in given grammatical case / Vrátí podstatné jméno vyskloňované v daném pádu """
        declenation = ""
        if lang == "en":
           try:
            if number == "singular":
                tag = str(person) + "sg"
                declenation = conjugate(word, tag)
            elif number == "plural":
                tag = str(person) + "pl"
                declenation = conjugate(word, tag)
           except:
               declenation = word
        elif lang == "cs":
           try:
            morph = majka.Majka(os.path.join(imp.find_module("gherkan")[1], "utils/majka.l-wt"))
            morph.flags |= majka.ADD_DIACRITICS
            analysis = morph.find(word)
            if analysis == []:
                declenation = word
            if number == "singular":
                for n in range(len(analysis)):
                    if 'singular' in analysis[n]['tags']:
                        declen = [analysis[n]['lemma'], analysis[n]['tags']]
                        if "person" in declen[1]:
                            if declen[1]["person"] == int(person) and declen[1]["singular"] is True and declen[1]["negation"] is False:
                                declenation = declen[0]
            else:
                for n in range(len(analysis)):
                    if 'singular' in analysis[n]['tags']:
                        declen = [analysis[n]['lemma'], analysis[n]['tags']]
                        if "person" in declen[1]:
                            if declen[1]["person"] == int(person) and declen[1]["singular"] is False and declen[1]["negation"] is False:
                                declenation = declen[0]
           except:
               declenation = word
        if not declenation:
            declenation = word
        return declenation

    def start_sentence_upper(self, text):
        """Changes the letters at the beginning of sentences into upper"""
        return re.sub("(^|[.?!])\s*([a-zA-Z])", lambda p: p.group(0).upper(), text.lower())

    def strip_extra_spaces(self, text):
        stripped_spaces = re.sub(' +', ' ', text)
        stripped_text = stripped_spaces.strip()
        return stripped_text

    def lemmatize(self, word):
        """  Returns lemma of given word form / Vrátí základní podobu slova (např. infinitiv)"""

        morph = majka.Majka('./majka.w-lt')
        morph.flags |= majka.ADD_DIACRITICS  # find word forms with diacritics
        morph.tags = False  # return just the lemma, do not process the tags
        morph.first_only = True  # return only the first entry
        output = morph.find(word)
        lemma = output[0]['lemma']

        return lemma


    def change_case(self, word, case, plural = False):
        """  Returns provided noun in given grammatical case / Vrátí podstatné jméno vyskloňované v daném pádu """
        morph = majka.Majka('./majka.l-wt')
        morph.flags |= majka.ADD_DIACRITICS
        word_form = []
        analysis = morph.find(word)

        if plural == False:
            for n in range(len(analysis)):
                if 'singular' in analysis[n]['tags']:
                    declen = [analysis[n]['lemma'],analysis[n]['tags']['case']]
                    if case in declen:
                       word_form.append(declen[0])
                else:
                    pass
        else:
            for n in range(len(analysis)):
                if 'plural' in analysis[n]['tags']:
                    declen = [analysis[n]['lemma'], analysis[n]['tags']['case']]
                    if case in declen:
                        word_form.append(declen[0])
            else:
                pass

        return word_form[0]

    def get_cases(self, word):
        """ Returns all possible cases of the word, in case of verb returns all info / Vrátí možné pády daného slova, u sloves vrátí všechno info"""
        morph = majka.Majka('./majka.w-lt')
        morph.flags |= majka.ADD_DIACRITICS  # find word forms with diacritics
        output = morph.find(word)

        cases = []
        if "substantive" in output[0]['tags']['pos'] or "adjective" in output[0]['tags']['pos']:
            for n in range(len(output)):
                 case = output[n]['tags']['case']
                 if "singular" in output[n]['tags']:
                  number = "singular"
                 else:
                  number = "plural"
                 cases.append([case, number])

        elif "verb" in output[0]['tags']['pos']:
            cases = output

        return cases


    def align_adjectives(self, lang, sentence):
        word_list = sentence.split()
        morph = majka.Majka(os.path.join(imp.find_module("gherkan")[1], "utils/majka.w-lt"))
        morph.flags |= majka.ADD_DIACRITICS
        if lang =="cs":
            for word in word_list:
                analysis = morph.find(word)
                if analysis == []:
                   continue
                else:
                    if analysis[0]["tags"]["pos"] == "substantive":
                        config = analysis[0]["tags"]
                        config["negation"] = False
                        del config["pos"]
                        if 'plural' in config:
                            del config["plural"]
            if config:
                verb = self.find_verb(lang, sentence)
                try:
                   analysis = morph.find(verb[0])
                   config["singular"] = analysis[0]["tags"]["singular"]
                except:
                    pass
                for word in word_list:
                    morph = majka.Majka(os.path.join(imp.find_module("gherkan")[1], "utils/majka.l-wt"))
                    analysis = morph.find(word)
                    if analysis:
                        if analysis[0]["tags"]["pos"] == "adjective":
                            for dict in analysis:
                                if all(item in dict["tags"].items() for item in config.items()):
                                    aligned_adj = dict["lemma"]
                                    sentence = re.sub(word, aligned_adj, sentence)
        else:
            pass
        return sentence

    def find_verb(self, lang, sentence):
        verb = []
        word_list = sentence.split()
        if lang =="cs":
            for word in word_list:
                morph = majka.Majka(os.path.join(imp.find_module("gherkan")[1], "utils/majka.w-lt"))
                morph.flags |= majka.ADD_DIACRITICS
                analysis = morph.find(word)
                if analysis == []:
                   continue
                else:
                    if analysis[0]["tags"]["pos"] == "verb":
                        verb.append(word)
                    else:
                        continue

        elif lang == "en":
            t = parsetree(sentence, tokenize = True,  tags = True)
            for sentence in t:
              try:
                  chunk = sentence.verbs[0]
                  verb.append(chunk.head.string)
              except:
                  print(colored("Warning: No verb detected in {}".format(sentence), "yellow"))

        return verb

    # def translate(self, phrase, lang = "cz-en"):
    #     """ Translates a word or phrase from czech to english (lang = "cz-en") or from english to czech (lang = "en-cz") """
    #     translator = Translator()
    #     if lang == "cz-en":
    #       result = translator.translate(phrase, src="cs", dest='en')
    #     elif lang == "en-cz":
    #       result = translator.translate(phrase, src="en", dest='cs')
    #
    #     translation = result.text
    #     return translation



if __name__ == "__main__":
 adjust = Finetuner()
