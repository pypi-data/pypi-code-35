import os
import json
import string
from termcolor import colored
import en_coref_md
from pattern.en import parsetree, conjugate, lemma
import re
import spacy
import gherkan.utils.constants as c
import gherkan.utils.gherkin_keywords as g
from gherkan.encoder.NL2Temp import NLTempMatcher
from gherkan.utils.word_morpho import Finetuner


# TODO: pass language from Raw Text
LANG = "en"


class RawNLParser:
    def __init__(self, feature=None, language="en", splitter="scenario"):
        """
        This class takes the raw text input and outputs the filled gherkin template in NL. It also updates
        the RobotPrograms.json with detected actions of selected subject
        :param feature: the actor we are talking about in the scenarios, i.e. robot R3
                (is filled when there is only "robot" without specification)
        :param language: language of the NL text (en/cs)
        :param subj_of_interest: subject of whom we collect actions and save them to RobotPrograms.json
        :param splitter: word which separates scenarios in NL text
        """
        self.lang = language
        self.split_word = splitter
        self.subj_of_interest = c.SUBJ_OF_INTEREST
        self.nlp = spacy.load('en_core_web_sm')
        self.actor_uni = feature
        self.cleaner = NLTempMatcher(self.lang)
        self.finetune = Finetuner()
        self.text_raw = None
        self.robot_actions = []
        self.text_lines_normalized = []
        self.sentences = []
        self.keywords = [g.GIVEN, g.WHEN, g.THEN]

    def parse(self, text_raw: str):
        """The main parser outputting the Given. When, Then template"""
        self.text_raw = text_raw
        scenarios = self.separate_scenarios(text_raw, self.split_word)

        for scenario in scenarios:
            print("Scenario: " + scenario)
            self.text_lines_normalized.append("Scenario: {}".format(scenario))
            text = self.replace_synonyms(scenario)
            text = self.substitute_feature(text)
            self.separate_sentences(text)
            phrases = self.prune_keywords(self.sentences)
            for phrase in phrases:
                self.collect_subject_actions(phrase)
            for sentence in self.sentences:
                clean = self.strip_extra_spaces(sentence)
                self.text_lines_normalized.append(clean)

        print("Actions connected with {}s: ".format(
            self.subj_of_interest), self.robot_actions)

    def prune_keywords(self, text):
        separators = [g.OR, g.AND]
        pruned = []
        for phrase in text:
            sent = re.sub(r'\b({}|{}|{})\b'.format(
                *self.keywords), "", phrase, re.IGNORECASE)
            for x in separators:
                if isinstance(sent, list):
                    for y in sent:
                        sent_y = re.split(x, y)
                        sent_y = list(filter(None, sent_y))
                        sent_y = [x for x in sent_y if x.lower() != []]
                        pruned.extend(sent_y)
                else:
                    sent = re.split(x, sent)
                    sent = list(filter(None, sent))
                    sent = [x for x in sent if x.lower() != []]
        return pruned

    def process_sentence(self, sentence):
        """ Aimed for processing of Background. Will not sort into template"""
        text = self.replace_synonyms(sentence)
        if self.lang == "en":
            splitter = re.compile(r'(^\s*{})'.format(g.GIVEN), re.IGNORECASE)
            given = list(filter(None, re.split(splitter, text)))
            given = [x for x in given if x.lower() != g.GIVEN.lower()]
            self.collect_subject_actions(given[0])
            lemmatized = self.strip_extra_spaces(
                g.GIVEN + self.finetune.lemmatize_sentence(self.lang, given[0]))
        elif self.lang == "cs":
            splitter = re.compile(
                r'(^\s*{})'.format(g.GIVEN_CS), re.IGNORECASE)
            given = list(filter(None, re.split(splitter, text)))
            given = [x for x in given if x.lower() != g.GIVEN_CS.lower()]
            self.collect_subject_actions(given[0])
            lemmatized = self.strip_extra_spaces(
                g.GIVEN + self.finetune.lemmatize_sentence(self.lang, given[0]))
        return lemmatized

    def get_text_lines(self):
        print(self.text_lines_normalized)
        return self.text_lines_normalized

    def substitute_feature(self, phrase):
        """If there is no specification of the subject, we take it from the feature (e.g. robot > robot R1)"""
        tree = parsetree(phrase, tokenize=True,
                         tags=True, chunks=True, relations=True)
        for sentence in tree:
            actors = sentence.subjects
        for actor in actors:
            if actor.string.lower() == self.subj_of_interest:
                actor_new = self.actor_uni.lower()
                phrase = re.sub(actor.string, actor_new, phrase)
        return phrase

    def replace_synonyms(self, command):
        """place words in command with synonyms defined in synonym_file"""
        synonyms_filename = os.path.join(
            c.PROJECT_ROOT_DIR, "gherkan", "utils", "synonyms.json")
        with open(synonyms_filename) as f:
            synonyms = json.load(f)
        for key in synonyms[self.lang]:
            for phrase in synonyms[self.lang][key]:
                if phrase in command.lower():
                    src_str = re.compile(
                        r'\b{}\b'.format(phrase), re.IGNORECASE)
                    command = src_str.sub(key, command)
        command_ready = self.strip_extra_spaces(
            re.sub(r"\stodelete", "", command))
        return command_ready

    def separate_sentences(self, text):
        """ Separate the sentences according to given keywords Given, When, Then """
        temps_cz = [g.GIVEN_CS, g.WHEN_CS, g.THEN_CS]
        if self.lang == "cs":
            for idx, key in enumerate(temps_cz):
                text = re.compile(r'\b{}\b'.format(key), re.IGNORECASE).sub(
                    self.keywords[idx], text)
        separated = self.find_patterns(text, self.keywords)
        return separated

    def find_patterns(self, text, t):
        """ Detects sentences framed with template keywords. Sentences without any keyword are detected as Then"""
        split = re.findall(
            r'\b(?:{0}|{1}|{2})\b.+?(?={0}|{1}|{2}|$)'.format(*t), text, re.IGNORECASE | re.MULTILINE)
        rest = list(filter(None, re.split(r',', split[-1], re.IGNORECASE)))
        try:
            for idx, x in enumerate(rest):
                keyword = re.findall(
                    r'{0}|{1}|{2}'.format(*t), x, re.IGNORECASE)
                if not keyword:
                    rest[idx] = " ".join([g.THEN, x])
        except:
            rest = []
        split = split[:-1] + rest
        for x in split:
            phrase = x.translate(str.maketrans('', '', string.punctuation))
            phrase = self.strip_extra_spaces(phrase)
            phrase = phrase.replace(" and ", "".join([" ", g.AND, " "]))
            phrase = phrase.replace(" or ", " OR ")
            if self.lang == "cs":
                phrase = phrase.replace(" a ",  "".join([" ", g.AND_CS, " "]))
                phrase = phrase.replace(" nebo ", " OR ")
            self.sentences.append(phrase)
        self.sentences = list(set(self.sentences))
        corr_order = [[], [], []]
        for idx, x in enumerate(t):
            for i in self.sentences:
                if x.lower() in i.lower():
                    i = re.sub(x.lower(), x, i)
                    corr_order[idx] = i
        self.sentences = list(filter(None, corr_order))
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
                    actor = str(sentence.subjects[0]).lower()
                if actor.lower() == self.subj_of_interest:   # if no specification, use the one defined in Feature
                    actor = self.actor_uni.lower()
                elif len(actor.split()) > 2:
                    actor_new = re.findall(
                        r'({}\s+([a-z]+)*([0-9])*([a-z]+)*)'.format(self.subj_of_interest), actor, re.IGNORECASE)
                    try:
                        actor = actor_new[0][0]
                    except:
                        pass
                action_lemma = self.finetune.lemmatize_sentence(
                    self.lang, "".join(action.lower().rsplit(actor)))
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
            print(colored("WARNING: No {} actions found. Have you parsed the text?".format(
                self.subj_of_interest), "red"))

    def strip_extra_spaces(self, text):
        stripped_spaces = re.sub(' +', ' ', text)
        stripped_text = stripped_spaces.strip()
        return stripped_text

    def collect_subject_actions(self, text):
        """ Detect any actions performed by a robot """
        tree = parsetree(text, tokenize=True, tags=True,
                         chunks=True, relations=True)
        for x in tree:  # now we select sentences with robot subjects or passive form
            for chunk in x.chunks:
                if chunk.string in x.subjects[0].string:
                    if self.subj_of_interest in chunk.string:  # active verb form
                        bool = self.cleaner.get_negative(x.string)
                        force = self.cleaner.get_force(x.string)
                        state, phrase = self.cleaner.get_state(x.string)
                        sentence_new = self.cleaner.get_cleanphr(
                            phrase, bool, force)
                        self.robot_actions.append(sentence_new)
            # handle passive verb form
            if " ".join(["by", self.subj_of_interest]) in x.string.lower():
                verbs, nouns = ([] for i in range(2))
                verb_object = (x.string).split(" by ")[0]
                subject = (x.string).split(" by ")[1]
                for chunk in x.chunks:
                    if chunk.type == "VP":
                        for word in chunk.words:
                            verbs.append(
                                (lemma(word.string)))
                        if "be" in verbs:
                            verbs.remove("be")
                        rest = verb_object.replace(chunk.string, "")
                sent = subject + " " + ' '.join(verbs) + " " + rest
                sent = x.translate(
                    str.maketrans('', '', string.punctuation))
                bool = self.cleaner.get_negative(sent)
                force = self.cleaner.get_force(sent)
                sentence_new = self.cleaner.get_cleanphr(sent, bool, force)
                self.robot_actions.append(sentence_new)
        # now remove duplicit actions:
        self.robot_actions = list(set(self.robot_actions))

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

    def solve_corefs(self, text):
        print("Loading Neuralcoref module...")
        nlc = en_coref_md.load()
        dok = nlc(text)
        if dok._.has_coref == 1:
            replaced_corefs = dok._.coref_resolved
        else:
            replaced_corefs = text
        print("Done")
        # print("Corref: " + replaced_corefs)

        return replaced_corefs

    def separate_scenarios(self, text, split_word):
        """Returns a list of scenarios separated by self.split_word. Upper case does not matter"""
        splitter = re.compile(r'\s*({})\s*'.format(split_word), re.IGNORECASE)
        split = re.split(splitter, text)
        split = list(filter(None, split))
        split_cl = [x for x in split if x.lower() != split_word]
        return split_cl

    def replace(self, string, substitutions):
        substrings = sorted(substitutions, key=len, reverse=True)
        regex = re.compile('|'.join(map(re.escape, substrings)))

        return regex.sub(lambda match: substitutions[match.group(0)], string)
