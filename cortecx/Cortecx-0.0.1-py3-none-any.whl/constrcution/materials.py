import os
import numpy as np
import pandas as pd
import tensorflow as tf
import itertools
from cortecx.constrcution.foundation import TextObj
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn import preprocessing as sklpp
from keras.preprocessing.image import array_to_img, img_to_array


class Tokenize:

    """Splits text into word tokens"""

    def __init__(self):
        self.text = None
        self.tokens = None
        self.args = None

    def process(self, text: str):
        self.text = text
        self.tokens = list(self.text.split(' '))
        self.tokens = [token for token in self.tokens if token is not '']
        return self.tokens


class Cleanse:

    """Cleans text of special characters and extra spaces"""

    def __init__(self, filters=None, include_punctuation=True, include_numbers=True, custom_filter=None):
        self.text = None
        self.filters = filters
        self.include_punctuation = include_punctuation
        self.include_numbers = include_numbers
        self.custom_filter = custom_filter

    def process(self, text: str):
        self.text = text
        deconstructed_text = []
        standard_filter = '`~@#$%^&*()_-+=}{][|\\/><'
        num_filter = '1234567890'
        punc_filter = ',.?":;!'
        apostraphe_filter = "'"
        punc_filter = punc_filter + apostraphe_filter
        reconstructed_text = ''
        final_filter = standard_filter

        if self.include_punctuation is True:
            final_filter = final_filter + punc_filter
        if self.include_numbers is True:
            final_filter = final_filter + num_filter
        if self.filters is not None:
            final_filter = final_filter + self.filters
        if self.custom_filter is not None:
            final_filter = self.custom_filter

        for element in self.text:
            if ord(element) < 128:
                if element not in final_filter:
                    deconstructed_text.append(element)

        for element in deconstructed_text:
            reconstructed_text = reconstructed_text + str(element)

        alphabet = 'abscdefghijklmnopqrstuvwxyz'

        for element in alphabet:
            reconstructed_text = reconstructed_text.replace('.' + element, '.' + ' ' + element)

        i = 0

        while i < 6:
            spaces = ['  ', '   ', '     ', '       ', '         ', '           ']
            for element in spaces:
                reconstructed_text = reconstructed_text.replace(element, ' ')
            i += 1

        return reconstructed_text


class Vectorize:

    """Converts text into it's word embeddings"""

    def __init__(self, vector_model, word_dimension_size, padding_length):
        self.text = None
        self.vector_model = vector_model
        self.word_dimension_size = word_dimension_size
        self.padding_length = padding_length

    def process(self, text):
        self.text = text

        words = None

        if type(self.text) is str:
            sentence = TextObj(self.text)
            sentence.apply(Cleanse(include_numbers=True, include_punctuation=True))
            sentence.apply(Tokenize())
            words = list(sentence.text)

        if type(self.text) is list:
            words = self.text

        while len(words) < int(self.padding_length):
            words.append(' ')
        sentence_as_vector = []
        for element in words:
            try:
                sentence_as_vector.append(self.vector_model[element])
            except KeyError:
                sentence_as_vector.append(np.zeros(int(self.word_dimension_size)))

        return sentence_as_vector


class Padding:

    """Pads sentence"""

    def __init__(self, padding_length, pad_char=None, clean=False):
        self.text = None
        self.padding_length = padding_length
        self.pad_char = pad_char
        self.clean = clean

    def process(self, text):
        self.text = text

        if type(self.text) is list:
            if self.pad_char is None:
                self.pad_char = ' '
            else:
                self.pad_char = self.pad_char

            while len(self.text) <= int(self.padding_length):
                self.text.append(self.pad_char)

            return self.text

        if self.clean is not False:
            self.text = TextObj(self.text).apply(Cleanse()).text
        else:
            self.text = str(self.text)

        if self.pad_char is None:
            self.pad_char = ' '
        else:
            self.pad_char = self.pad_char
        tokens = TextObj(self.text)
        tokens.apply(Tokenize())
        tokens = list(tokens.text)

        while len(tokens) <= int(self.padding_length):
            tokens.append(self.pad_char)

        return tokens


class Chop:

    """Cuts text into specified word chunks"""

    def __init__(self, chop_size, pad_char=None, clean=False):
        self.text = None
        self.chop_size = chop_size
        self.pad_char = pad_char
        self.clean = clean

    def process(self, text):
        self.text = text
        tokens = None

        if self.pad_char is None:
            self.pad_char = ' '
        if self.clean is not False:
            self.text = TextObj(self.text)
            self.text.apply(Cleanse())
            self.text = self.text.text
        if type(self.text) == str:
            tokens = TextObj(self.text)
            tokens.apply(Tokenize())
            tokens = list(tokens.text)
        elif type(self.text) == list:
            tokens = self.text

        chopped_text = []
        i = 0
        x = 0
        y = self.chop_size
        chopps = TextObj(None)
        while i <= (len(tokens) / self.chop_size):
            chopps.text = tokens[x:y]
            chopps.apply(Padding(padding_length=(self.chop_size - 1), pad_char=self.pad_char))
            chopped_text.append(list(chopps.text))
            x += self.chop_size
            y += self.chop_size
            i += 1

        for element in chopped_text:
            if element == [self.pad_char for num in range(self.chop_size)]:
                chopped_text.remove(element)
            else:
                continue
        return chopped_text


class Reconstruct:

    """Reconstructs word tokens back into string"""

    def __init__(self):
        self.text = None
        self.tokens = self.text

    def process(self, text):
        self.text = text

        if type(self.text) is not list:
            raise TypeError('Reconstruct reconstructs word tokens therefore input must be a list')

        self.tokens = list(self.text)
        new_string = ''

        for element in self.tokens:
            new_string = new_string + str(element) + ' '

        return new_string


class OneHotEncode:

    """Convert text to lists of word hashes"""

    def __init__(self, highest_num=1000):
        self.text = None
        self.highest_num = highest_num

    def process(self, text):
        self.text = text
        return tf.keras.preprocessing.text.one_hot(self.text, self.highest_num)


class FrequencyEncode:

    """Encode text into its representing number of occurrences of each word in the sentence"""

    def __init__(self):
        self.text = None

    def process(self, text):
        self.text = text
        obj = TextObj(self.text)
        obj.apply(Tokenize())
        tokens = list(obj.text)

        for token in tokens:
            tokens[tokens.index(token)] = tokens.count(token)

        return tokens


class SentTokenize:

    """Tokenizes text by sentence rather than word"""

    def __init__(self):
        self.text = None
        self.tokens = None

    def process(self, text):
        self.text = text
        return self.text.split('. ')


class Binarize:
    def __init__(self):
        self.labels = None
        self.data = None

    def process(self, data):
        self.data = data
        self.labels = LabelBinarizer().fit(self.data)
        return self.labels


class AddFeature:
    def __init__(self, feature, injection_level):
        self.feature = feature
        self.injection_level = int(injection_level)
        self.data = None

        if injection_level > 3:
            raise ValueError('Only an injection level of 3 is supported')

    def process(self, data):
        self.data = data  # Not Finished


class Split:

    """Returns split chunks from data"""

    def __init__(self, steps):
        self.steps = steps

    def process(self):
        pass  # Not Finished


class Shuffle:

    """Shuffles data"""

    def __init__(self):
        self.data = None

    def process(self, data):
        self.data = data
        return np.random.shuffle(self.data)


class Flatten:

    """Converts an N-Dimensional array to 1D Vector"""

    def __init__(self):
        self.data = []
        self.shape = np.shape(np.array(self.data))

    def process(self, data):
        self.data = data
        self.shape = np.shape(np.array(self.data))
        return list(itertools.chain(*self.data))  # Fix


class Repeat:

    """Repeats array n amount of times"""

    def __init__(self, repetition_value):
        self.repval = repetition_value
        self.data = []

    def process(self, data):
        self.data = data
        self.data = [self.data for number in range(self.repval)]
        return self.data


class Reshape:

    """Reshapes array"""

    def __init__(self, new_shape):
        self.shape = new_shape
        self.data = None

    def process(self, data):
        self.data = np.array(data)
        return np.shape(self.data, self.shape)


class Roll:

    """Inverses the position of all elements im data"""

    def __init__(self):
        self.data = None

    def process(self, data):
        self.data = data
        return reversed(self.data)


class Find:

    """Find item in n dimensional array"""

    def __init__(self, coordinates):
        self.data = None
        self.coords = coordinates

    def process(self, data):
        self.data = data



class Sort:

    """Sorts data based on specifications"""

    def __init__(self, sort_by='ltg'):
        self.data = None
        self.sort_by = sort_by
        pass  # Not Finished


class Sum:

    """Sums all values in data"""

    def __init__(self):
        self.data = None
        pass  # Not Finished - Requires Flatten


class EqualizeLength:

    """Equalizes length of two arrays"""

    def __init__(self, length):
        self.data = None
        self.length = length
        pass  # Not Finished


class Scale:

    """Scales all values in data"""

    def __init__(self, scale='scale'):
        self.data = None
        self.scale = scale

    def process(self, data):
        self.data = data
        if self.scale == 'scale':
            return sklpp.scale(self.data)
        elif self.scale == 'standard':
            return sklpp.StandardScaler().fit(self.data)
        elif self.scale == 'minmax':
            return sklpp.MinMaxScaler().fit(self.data)
        elif self.scale not in any(['scale', 'minmax', 'standard']):
            raise ValueError('scale must be one of the three standard scalers')


class Encode:

    """Encodes all values in data"""

    def __init__(self, return_type=list):
        self.data = None
        self.return_type = return_type
        pass  # Not Finished


class Normalize:

    """Performs normalization"""

    def __init__(self):
        self.data = None
        pass  # Not Finished


class Deepen:

    """Deepen DataObj current data depth. Useful for applying vector only functions deep into multi-dim matricies"""

    def __init__(self):
        self.data = None

    def process(self, data):
        self.data = data
        pass  # Not Finished


class Raise:

    """Rise in DataObj current data depth. Useful for applying vector only functions deep into multi-dim matricies or
    to undo results of Deepen"""

    def __init__(self):
        self.data = None

    def process(self, data):
        self.data = data
        pass  # Not Finished


class TrainTestSplit:

    """Splits data into train and testing batches"""

    def __init__(self, test_split):
        self.data = None
        self.split = test_split

    def process(self, data):
        self.data = data
        return train_test_split(self.data, self.split)


"""
class LoadDiseases:

    Loads disease dataset from diseases.json

    def __init__(self):
        self.data = None

    def process(self, data):
        self.data = data
        self.data = list(pd.read_json(str(os.path.abspath('../data/diseases.json')))['graphs'])[0]
        return self.data
"""


class ArrayToImage:

    """Converts array to image"""

    def __init__(self):
        self.data = None

    def process(self, data):
        self.data = data
        return array_to_img(self.data)


class ImageToArray:

    """Converts image to array"""

    def __init__(self):
        self.data = None

    def process(self, data):
        self.data = data
        self.data = img_to_array(self.data)


