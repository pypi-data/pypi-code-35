# coding: utf-8
from googletrans import Translator
import majka

class AdjustWords():

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

        # for x in cases:
        #     if x < final_list:
        #         pass
        #     else:
        #         final_list.append(x)

        return cases

    def translate(self, phrase, lang = "cz-en"):
        translator = Translator()
        if lang == "cz-en":
          result = translator.translate(phrase, src="cs", dest='en')
        elif lang == "en-cz":
          result = translator.translate(phrase, src="en", dest='cs')

        translation = result.text
        return translation



if __name__ == "__main__":

 entry = "put on the line"
 adjust = AdjustWords()
 word = adjust.translate(entry, "en-cz")
print(word)
