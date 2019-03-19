import os
import json
import string
import en_coref_md
from pattern.en import parsetree, conjugate
from pattern.search import Pattern
import itertools
import spacy
import re
import gherkan.utils.constants as c
import gherkan.utils.gherkin_keywords as g


class RawNLParser:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.text_raw = ""
        self.robot_actions = []
        self.text_lines_normalized = []
        self.sentences = []

    def parse(self, text_raw: str):
        self.text_raw = text_raw
        scenarios = self.separate_scenarios(text_raw)

        for scenario in scenarios:
            print("Scenario: " + scenario)
            self.text_lines_normalized.append("Scenario: {}".format(scenario))
            text = self.replace_synonyms(scenario)
            self.collect_robot_actions(text)
            separated_text = self.separate_sentences(text)
            for phrase in separated_text:
                lemmatized = self.lemmatize(phrase)
                clean = self.strip_extra_spaces(lemmatized)
                self.text_lines_normalized.append(clean)

        print("Things that robots do: ", self.robot_actions)

    def process_sentence(self, sentence):
        """ Aimed for processing of Background. Will not sort into template"""
        text = self.replace_synonyms(sentence)
        self.collect_robot_actions(text)
        if (text[0:5]).lower() == "given":
            lemmatized = "given" + self.lemmatize(text[6:])
        else:
            lemmatized = self.lemmatize(text)
        return lemmatized

    def get_text_lines(self):
        return self.text_lines_normalized

    def replace_synonyms(self, command):
        """place words in command with synonyms defined in synonym_file"""
        synonyms_filename = os.path.join(
            c.PROJECT_ROOT_DIR, "gherkan", "utils", "synonyms.json")
        with open(synonyms_filename) as f:
            synonyms = json.load(f)
        for key in synonyms:
            for phrase in synonyms[key]:
                if phrase in command.lower():
                    src_str = re.compile(phrase, re.IGNORECASE)
                    command = src_str.sub(key, command)
        command_ready = command.replace(" todelete", "")
        # print("Replaced: " + self.command_ready)
        return command_ready

    def separate_sentences(self, text):
        """ Separate the sentences according to given keywords Given, When, Then """
        separated = []
        self.sentences = []
        templates = ["Given ", "When ", "Then "]
        for word in templates:
            separated = self.find_patterns(text, word)

        return separated

    def find_patterns(self, text, temp_word):
        """ Detects sentences starting with temp_word and end with "," or "."
            Sentences without any keyword are detected as Then"""
        detected_temp = re.findall(
            r'(?<=(?i)' + re.escape(temp_word) + r')+([^,]+)', text)
        rest = []
        for x in detected_temp:
            rest = re.split(x, text)[1]
            text = rest
            rest = rest.translate(str.maketrans('', '', string.punctuation))
            rest = self.strip_extra_spaces(rest)
        for x in detected_temp:
            new_match = temp_word + x
            new_match = new_match.replace(" and ", " AND ")
            new_match = new_match.translate(
                str.maketrans('', '', string.punctuation))
            new_match = self.strip_extra_spaces(new_match)
            self.sentences.append(new_match)
        if rest:
            rest = "Then " + re.compile("then ", re.IGNORECASE).sub("", rest)
            self.sentences.append(rest)

        for a, b in itertools.combinations(self.sentences, 2):
            if a in b:
                self.sentences.remove(a)
            elif b in a:
                self.sentences.remove(b)

        return self.sentences

    def generate_program_dict(self, make_new=True):
        """ make_new - creates a new dict and replaces old one. If False, programs are appended to current dict """
        program_dict = {}
        dict_path = os.path.join(
            c.PROJECT_ROOT_DIR, "gherkan", "utils", "RobotPrograms_en.json")
        if self.robot_actions:
            if not make_new:
                with open(dict_path, 'r') as f:
                    program_dict = json.load(f)
                    f.close()
            for action in self.robot_actions:
                tree = parsetree(action, tokenize=True,
                                 tags=True, chunks=True, relations=True)
                for sentence in tree:
                    actor_type = str(sentence.subjects[0])
                    actor = "".join(actor_type.rsplit("robot "))
                action_lemma = self.lemmatize(
                    "".join(action.rsplit(actor_type)))
                if actor in program_dict.keys():
                    is_unique = True
                    # find if the action is already in list
                    for key in program_dict[actor]:
                        if self.strip_extra_spaces(action_lemma) in program_dict[actor][key]:
                            is_unique = False
                    if is_unique:
                        new_key = len(program_dict[actor]) + 1
                        program_dict[actor].update(
                            {new_key: self.strip_extra_spaces(action_lemma)})
                else:
                    program_dict[actor] = {
                        1: self.strip_extra_spaces(action_lemma)}
            with open(dict_path, 'w') as f:
                json.dump(program_dict, f)
            print("Program list: {}".format(program_dict))
            print("Programs saved to {}".format(dict_path))
        else:
            raise Exception(
                "No robot actions found. Have you parsed the text first?")

    def strip_extra_spaces(self, text):
        stripped_spaces = re.sub(' +', ' ', text)
        stripped_text = stripped_spaces.strip()
        return stripped_text

    def collect_robot_actions(self, text):
        """ Detect any actions performed by a robot """
        tree = parsetree(text, tokenize=True, tags=True,
                         chunks=True, relations=True)
        sentences = self.separate_compound(tree)
        for x in sentences:  # now we select sentences with robot subjects or passive form
            sent_parsed = parsetree(x, chunks=True, relations=True)
            for sentence in sent_parsed:
                for chunk in sentence.chunks:
                    if chunk in sentence.subjects:
                        if "robot" in chunk.string:  # active verb form
                            sentence = sentence.slice(
                                chunk.start, sentence.stop)
                            sent = (sentence.string).translate(
                                str.maketrans('', '', string.punctuation))
                            sentence_new = self.strip_extra_spaces(sent)
                            self.robot_actions.append(sentence_new)
                if "by robot" in sentence.string.lower():  # handle passive form
                    verbs, nouns = ([] for i in range(2))
                    verb_object = (sentence.string).split(" by ")[0]
                    tree = parsetree(verb_object, lemmata=True)
                    subject = (sentence.string).split(" by ")[1]
                    for part in tree:
                        for chunk in part.chunks:
                            if chunk.type == "VP":
                                for word in chunk.words:
                                    verbs.append(
                                        (conjugate(word.string, tense="INFINITIVE")))
                                if "be" in verbs:
                                    verbs.remove("be")
                                rest = verb_object.replace(chunk.string, "")
                    sent = subject + " " + ' '.join(verbs) + " " + rest
                    sent = sent.translate(
                        str.maketrans('', '', string.punctuation))
                    sentence_new = self.strip_extra_spaces(sent)
                    self.robot_actions.append(sentence_new)
        # now remove duplicit actions:
        for a, b in itertools.combinations(self.robot_actions, 2):
            if a in b:
                self.robot_actions.remove(a)
            elif b in a:
                self.robot_actions.remove(b)

    def separate_compound(self, tree):
        """ Separate individual sentences in a compound sentence"""
        sentence_num = 1  # we always have at least one sentence
        sentence_start = 0
        sentences = []
        for sentence in tree:
            for chunk in sentence.chunks:  # first we split compound sentences according to chunk relations
                if chunk.relation is not None and chunk.relation is not sentence_num:
                    new_sentence = sentence.slice(sentence_start, chunk.start)
                    sentences.append(new_sentence.string)
                    sentence_start = chunk.start
                    sentence_num = chunk.relation
            sentence_new = sentence.slice(sentence_start, sentence.stop)
            sentences.append(sentence_new.string)
        return sentences

    def lemmatize(self, text):
        lemmas = ""
        # this version keeps capitals
        nlp = spacy.load('en_core_web_sm', disable=['tagger', 'parser', 'ner'])
        doc = nlp(text)
        skip_list = [",", ".", ";"]
        temp_words = [g.GIVEN, g.WHEN, g.THEN]

        for token in doc:
            if token.text in temp_words:
                lemmas += token.text
            else:
                if token.lemma_ in skip_list:
                    pass
                else:
                    lemmas += " "
                lemmas += token.lemma_

        lemmatised = lemmas
        # print(lemmatised)

        return lemmatised

    def solve_corefs(self, text):
        print("Loading Neuralcoref module...")
        nlc = en_coref_lg.load()
        dok = nlc(text)
        if dok._.has_coref == 1:
            replaced_corefs = dok._.coref_resolved
        else:
            replaced_corefs = text
        print("Done")
        # print("Corref: " + replaced_corefs)

        return replaced_corefs

    def separate_scenarios(self, text):
        text = text
        split = text.split("scenario ")
        split = list(filter(None, split))
        # print("Scenarios: ", split)

        return split

    def replace(self, string, substitutions):
        substrings = sorted(substitutions, key=len, reverse=True)
        regex = re.compile('|'.join(map(re.escape, substrings)))

        return regex.sub(lambda match: substitutions[match.group(0)], string)
