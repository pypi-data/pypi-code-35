# coding: utf-8
# from googletrans import Translator
import majka, re, os, imp
from pattern.en import conjugate, parsetree, lemma
from termcolor import colored
import spacy, unicodedata

class Finetuner():
    def __init__(self):
        self.morph_lwt = majka.Majka(os.path.join(imp.find_module("gherkan")[1], "utils/majka.l-wt"))
        self.morph_wlt = majka.Majka(os.path.join(imp.find_module("gherkan")[1], "utils/majka.w-lt"))

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
            self.morph_lwt.flags |= majka.ADD_DIACRITICS
            analysis = self.morph_lwt.find(word)
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
        if word == "nebýt" and person == 3:   # majka does not work for this case
            if number == "singular":
                declenation = "není"
            else:
                declenation = "nejsou"
        return declenation

    def start_sentence_upper(self, text):
        """Changes the letters at the beginning of sentences into upper"""
        return re.sub("(^|[.?!])\s*([a-zA-Z])", lambda p: p.group(0).upper(), text.lower())

    def strip_extra_spaces(self, text):
        stripped_spaces = re.sub(' +', ' ', text)
        stripped_text = stripped_spaces.strip()
        return stripped_text

    def lemmatize(self, lang, word):
        """  Returns lemma of given word form / Vrátí základní podobu slova (např. infinitiv)"""
        if lang == "cs":
            self.morph_wlt.flags |= majka.ADD_DIACRITICS  # find word forms with diacritics
            self.morph_wlt.tags = False  # return just the lemma, do not process the tags
            self.morph_wlt.first_only = True  # return only the first entry
            output = self.morph_wlt.find(word)
            lemma = output[0]['lemma']
        else:
            # this version keeps capitals
            nlp = spacy.load('en_core_web_sm', disable=['tagger', 'parser', 'ner'])
            doc = nlp(word)
            for token in doc:
                    lemma = str(token.lemma_)

        return lemma

    def lemmatize_sentence(self, lang, text):
        self.lang = lang
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

    def change_case(self, word, case, plural = False):
        """  Returns provided noun in given grammatical case / Vrátí podstatné jméno vyskloňované v daném pádu """
        self.morph_lwt.flags |= majka.ADD_DIACRITICS
        word_form = []
        analysis = self.morph_lwt.find(word)

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

    def make_negative(self, lang, word):
        if lang == "cs":
            self.morph_wlt.flags |= majka.ADD_DIACRITICS
            self.morph_wlt.tags = False
            self.morph_wlt.first_only = False
            analysis = self.morph_wlt.find(word)
        elif lang == "en":
            neg = conjugate(word, negated=True)

    def get_cases(self, word):
        """ Returns all possible cases of the word, in case of verb returns all info / Vrátí možné pády daného slova, u sloves vrátí všechno info"""
        self.morph_wlt.flags |= majka.ADD_DIACRITICS  # find word forms with diacritics
        output = self.morph_wlt.find(word)

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
        self.morph_wlt.flags |= majka.ADD_DIACRITICS
        if lang =="cs":
            for word in word_list:
                analysis = self.morph_wlt.find(word)
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
                   analysis = self.morph_wlt.find(verb[0])
                   config["singular"] = analysis[0]["tags"]["singular"]
                except:
                    pass
                for word in word_list:
                    analysis = self.morph_lwt.find(word)
                    if analysis:
                        if analysis[0]["tags"]["pos"] == "adjective":
                            for dict in analysis:
                                if all(item in dict["tags"].items() for item in config.items()):
                                    aligned_adj = dict["lemma"]
                                    sentence = re.sub(word, aligned_adj, sentence)
        else:
            pass
        return sentence

    def remove_diacritics(self, text):
        """
        Returns a string with all diacritics (aka non-spacing marks) removed.
        For example "Héllô" will become "Hello".
        Useful for comparing strings in an accent-insensitive fashion.
        """
        normalized = unicodedata.normalize("NFKD", text)
        return "".join(c for c in normalized if unicodedata.category(c) != "Mn")

    def find_verb(self, lang, sentence, head_only=True):
        verb = []
        word_list = sentence.split()
        if lang =="cs":
            for word in word_list:
                analysis = self.morph_wlt.find(word)
                if analysis == []:
                   continue
                else:
                    if analysis[0]["tags"]["pos"] == "verb":
                        verb.append(word)
                    else:
                        continue
        elif lang == "en":
            t = parsetree(self.lemmatize_sentence(lang, sentence), tokenize=True,  tags=True)
            excepts = ["start", "stop", "end", "finish"]
            for sent in t:
              # try:
                  chunk = sent.verbs
                  check = False
                  if chunk:
                      for x in excepts:
                              if x in chunk[0].string:
                                word = re.findall(r'\w*{}\w*'.format(x), chunk[0].string)
                                if word:
                                  verb.append(word[0])
                                  check = True
                      if not check:
                             if head_only:
                               verb.append(chunk[0].head.string)
                             else:
                               verb.append(chunk[0].string)
                  else:
                    for x in t.string.split():
                      if x in excepts:
                          word = re.findall(r'\w*{}\w*'.format(x), t.string)
                          if word:
                              verb.append(word[0])
              # except:
              #     print(colored("Warning: No verb detected in {}".format(sentence), "yellow"))

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
