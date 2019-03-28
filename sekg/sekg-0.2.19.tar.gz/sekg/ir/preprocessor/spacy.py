import spacy

from .base import Preprocessor

nlp = spacy.load('en_core_web_sm')


class SpacyTextPreprocessor(Preprocessor):
    ## todo: improve the text preprocessor and more use-case, more test
    stopWords = {'ourselves', 'first', 'single', 'hers', 'between', 'yourself', 'but', 'again', 'there',
                 'about', 'once', 'one', 'two', 'three', 'second', 'new', 'multiple', 'most', 'mostly',
                 'exact', 'enough', 'entire',
                 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be',
                 'some', ' for', 'do',
                 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am',
                 'or', 'who', 'as', 'from ', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are',
                 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself',
                 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours',
                 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been',
                 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over',
                 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just',
                 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being',
                 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here',
                 'than', "something", "anything",
                 "also", "already", "another", "although", "always", "am", "among",
                 "amongst", "anybody", "any", "anymore", "anyway", "apparently", "both", "better", "best",
                 "by", "but", "considering", "corresponding", "containing", "do", "does", "did", "each",
                 "else", "elsewhere", "enough", "even", "evenly", "ever", "every", "everybody", "everyone",
                 "everything", "everywhere", "f", "except", "e.g", "e", "far", "few", "little", "no", "first",
                 "five", "one", "two", "three", "four", "five", "1th", "six", "seven", "eight", "nine", "ten",
                 "2th", "3th", "4th", "5th", "following", "followed", "former", "furthermore",

                 "her",
                 "here",
                 "hers",
                 "herself",
                 "hes",
                 "hi",
                 "hid",
                 "high",
                 "higher",
                 "highest",
                 "him",
                 "himself",
                 "his",
                 "hither",

                 "how",

                 "however",
                 "hundred",
                 "of",
                 "'s",
                 "if",
                 "im",
                 "immediate",
                 "immediately",
                 "importance",
                 "important",
                 "in",
                 "inner",
                 "insofar",
                 "instead",
                 "interest",
                 "interested",
                 "interesting",
                 "interests",
                 "into",
                 "inward",
                 "is",
                 "isn't",
                 "it",
                 "it'd",
                 "it'll",
                 "it's",
                 "itd",
                 "its",
                 "itself",
                 "latest", "last", "many", "maybe", "merely", "me", "more", "much", "new", "nearly", "never",
                 "must", "next", "nobody", "nor", "none", "now", "one", "ones", "once", "only", "old", "on",
                 "of", "often", "or", "our", "other", "others", "our", "ours", "over", "own", "your", "my",
                 "mine", "yours", "per",
                 "such", "still", "that", "those", "their", "theirs", "then", "there", "them", "themselves",
                 "these", "those", "thereby", "though", "through", "together", "today", "well", "bad", "good",
                 "what", "when", "which", "whatever", "whenever", "when", "whether", "while", "whos", "who",
                 "whom", "whin", "yourself", "yet", "b", "c", "d", "e", "f", "zzz", "zzzz", "yes", "xxx",
                 "quite", "rather", "same", "different", "secondly", "shall", "sometime", "someone",
                 "somewhere", "somehow", "somebody", "some", "so", "aa", "aaa", "bbb", "a1", "a2", "b1", "b2",
                 "-", "a3", "abcd", "non",
                 "change", "current", "currently", "explicitly", "return", "access", "future",
                 "use", "using", "this", "the",
                 }

    def extract_words_for_query(self, query):
        np_v_list = []

        doc = nlp(query)
        for np in doc.noun_chunks:
            np_words = []
            for np_token in np:
                lemma_token = np_token.lemma_

                if np_token.is_stop or np_token.text.lower() in self.stopWords or lemma_token in self.stopWords:
                    continue
                np_words.append(lemma_token)

            clean_np_str = " ".join(np_words)
            if clean_np_str:
                np_v_list.append(clean_np_str)

        for token in doc:
            if token.pos_ == "VERB" and token.is_stop == False:
                verb_lemma = token.lemma_
                if verb_lemma not in self.stopWords:
                    np_v_list.append(verb_lemma)

        # todo: extract CamelName split as keyword from this

        return " ".join(np_v_list).split()

    def clean(self, text):
        """
        return a list of token from the text, only remove stopword and lemma the word
        :param text: the text need to preprocess
        :return: list of str
        """

        result = []
        doc = nlp(text)

        for token in doc:
            if token.pos_ == "PUNCT":
                continue
            if token.is_stop or token.text.lower() in self.stopWords or token.lemma_ in self.stopWords:
                continue

            result.append(token.lemma_.lower())

        return result
