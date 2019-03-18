import re
import copy
import random as rn

__all__ = ['Markold']

class Markold:
    def __init__(self):
        self.sentences = []
        self.saved_matrixes = {}

    def import_sentences(self, file):
        self.sentences = []
        self.saved_matrixes = {}
        if isinstance(file, list):
            self.sentences = file
        else:
            with open(file, 'r', encoding='utf-8') as input_file:
                self.sentences = input_file.read().split('\n')

    def beautify(self, sentences):
        """ Reformats sentences by adding a space before and after punctuation
            (to treat them as regular sentence parts). """

        translator = str.maketrans({key: " {0} ".format(key) for key in ','})

        if isinstance(sentences, str):
            return re.sub(r'\s+', ' ', sentences.translate(translator)).strip()

        elif isinstance(sentences, list):
            new_lst = []
            for sentence in sentences:
                new_lst.append(re.sub(r'\s+', ' ', sentence.translate(translator)).strip())
            return new_lst

        return sentences

    def reformate_sentence(self, sentence):
        """ Reformat the sentence correctly, such as punctuation have the correct spacing. """

        sentence = sentence.replace(' , ', ', ')
        sentence = sentence.replace(' \' ', '\'')
        return sentence

    def get_key(self, words, i, n):
        """ Returns a key consisting of n words. """
        new_key = []
        for j in range(n):
            new_key.append(words[i+j])
        return tuple(new_key)

    def compute_words(self, sentences, nb):
        """ Returns a set of unique pair of words across all the sentences. """

        n_words_set = set()

        for sentence in sentences:
            words = sentence.split(' ')
            if len(words) > (nb - 1):
                for i, _ in enumerate(words):
                    if i < len(words) - nb + 1:
                        n_words_set.add(self.get_key(words, i, nb))

        return n_words_set

    def compute_word_occurence(self, sentences, word_order, n):
        """ Computes the number of occurences of each words following each pair of words. """

        matrix = {}

        for word in word_order:
            matrix[word] = {}

        for sentence in sentences:
            splitted = sentence.split(' ')
            if len(splitted) > n - 1:
                for i, word in enumerate(splitted):

                    if i < len(splitted) - n + 1:
                        key = self.get_key(splitted, i, n)
                    else:
                        break

                    if i == 0:
                        if 'BEGIN' in matrix[key]:
                            matrix[key]['BEGIN'] += 1
                        else:
                            matrix[key]['BEGIN'] = 1

                    if i == len(splitted) - n:
                        if 'END' in matrix[key]:
                            matrix[key]['END'] += 1
                        else:
                            matrix[key]['END'] = 1

                    if i < len(splitted) - n:
                        if splitted[i+n] in matrix[key]:
                            matrix[key][splitted[i+n]] += 1
                        else:
                            matrix[key][splitted[i+n]] = 1

        return matrix

    def cumulative_probs(self, lst):
        """ Orders the a list of probabilities and transforms them into cumulative probabilities. """

        total_sum = sum([x[1] for x in lst])

        # Normalising (-> probs)
        lst = [[x[0], x[1] / total_sum] for x in lst]

        # Ordering probs
        lst = sorted(lst, key=lambda x: x[1], reverse=False)

        # Cumulative probs
        for i, _ in enumerate(lst):
            if i != 0:
                lst[i][1] += lst[i-1][1]

        return lst

    def return_selected(self, random_choice, lst):
        """ Chose a random word from a probabilities list. """

        for i, word in enumerate(lst):
            if i == 0:
                if random_choice < word[1]:
                    return word[0]

            if i == len(lst) - 1:
                return word[0]

            else:
                if lst[i-1][1] <= random_choice < lst[i][1]:
                    return word[0]

        # Sometimes, lst is empty
        return lst[0][0]


    def normalise_word_matrix(self, word_matrix):
        """ Normalises the number of occurences of each word (from occurences to probabilities). """

        new_matrix = copy.deepcopy(word_matrix)

        for word, probs in new_matrix.items():
            total_sum = sum(probs.values())

            for next_word_prob in probs.keys():
                new_matrix[word][next_word_prob] = new_matrix[word][next_word_prob] / total_sum

        return new_matrix

    def compute_word_matrix(self, markov):
         # Add spaces before and after quotes and commas
        trimmed = self.beautify(self.sentences)

        # Get all unique words across all sentences
        word_set = self.compute_words(trimmed, markov)

        # Compute the number of occurence of each words
        word_prob_matrix = self.compute_word_occurence(trimmed, word_set, markov)

        # Transforms occurences into cumulative probabilities
        word_prob_matrix_normalised = self.normalise_word_matrix(word_prob_matrix)

        self.saved_matrixes[markov] = {'wpm': word_prob_matrix, 'wpmn': word_prob_matrix_normalised}



    def generate_sentence(self, markov, min_word_length=0, max_word_length=50):
        """ Generates a sentence from a list of word probabilities. """

        new_sentence = ''
        first_word = []
        last_word = ''

        if not markov in self.saved_matrixes.keys():
            self.compute_word_matrix(markov)

        wpm = self.saved_matrixes[markov]['wpm']
        wpmn = self.saved_matrixes[markov]['wpmn']

        # Get every couple of words that can start a sentence
        for word, next_word_proba in wpm.items():
            if 'BEGIN' in next_word_proba:
                first_word.append([word,  wpm[word]['BEGIN']])

        first_word = self.cumulative_probs(first_word)

        # Choose a random one
        random_choice = rn.random()
        first_choice = self.return_selected(random_choice, first_word)

        # We got our first couple of words. Yay!
        new_sentence += ' '.join(first_choice) + ' '
        last_word = first_choice

        iteration = 0

        while iteration <= max_word_length or 'END' not in next_word_proba.keys():

            #BUG: Sometimes, the algorithm get stuck in an infinite loop between 2 words
            if iteration > max_word_length * 2:
                print(f'WARNING: endless loop between two words, invalid sentence (ditched)')
                return ''


            # BUG: shouldn't happen (but it did)
            try:
                # Get the probable words following the last one
                next_word_proba = wpmn[last_word]
            except KeyError:
                break

            next_word_proba_lst = [[k, v] for k, v in next_word_proba.items() if k != 'BEGIN']
            next_word_proba_lst = self.cumulative_probs(next_word_proba_lst)

            # If we have reached the maximum number of words allowed and we can end here, do it
            if iteration > max_word_length and any(x[0] == 'END' for x in next_word_proba_lst):
                break

            # Else, pick a random one
            else:
                random_choice = rn.random()

                choice = self.return_selected(random_choice, next_word_proba_lst)

            # If we chose that this is the end of the sentence
            if choice == 'END':
                # If we reached the minimal number of words in the sentence, we're done
                if iteration >= min_word_length:
                    break

                else:
                    # Else, check if there are other possibilities than END
                    removed_end_cumulative = [x for x in next_word_proba_lst if x[0] != 'END']
                    if removed_end_cumulative:
                        random_choice = rn.random()
                        choice = tuple([self.return_selected(random_choice, removed_end_cumulative)])
                    # Else, we have no other choice than finishing the sentence
                    else:
                        break


            # Else, take a random couple of words beginning with the choosen word
            else:
                lst = [k for k in wpm.keys() if k[0] == choice]
                if lst:
                    choice = lst[rn.randint(0, len(lst) - 1)]
                else:
                    break

            # Continue until we have reached the maximum number of words allowed
            new_sentence += ' '.join(choice) + ' '
            last_word = choice

            iteration += 1

        return new_sentence

    def generate_multiple_sentences(self, markov, n, min_word_length=0, max_word_length=50, to_output=None, to_print=None):
        generated_sentences = []

        for x in range(n):
            print(f'Generating sentence {x}...', end=' ')
            generated_sentences.append(self.reformate_sentence(self.generate_sentence(markov, min_word_length=min_word_length,
                                                                                      max_word_length=max_word_length)))
            print(f'sentence generated.')

        if to_output:
            output_file = open(to_output, 'a', encoding='utf-8')

        if to_output or to_print:
            for sentence in generated_sentences:
                if to_print:
                    print(sentence)
                if to_output:
                    output_file.write(sentence + '\n')

        if to_output:
            output_file.close()

        return generated_sentences
