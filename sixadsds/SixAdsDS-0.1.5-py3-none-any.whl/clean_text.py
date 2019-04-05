"""
Functions for text preprocesing/summarizing.
A common way to use these functions is to combine them into a pipeline which the input is a list containing strings.    
"""

# Additional packages

import nltk
from nltk.corpus import stopwords
import string
import re
import inflection
from nltk.stem import WordNetLemmatizer
from tqdm import tqdm

def lemmatize_word(string_list, engine=WordNetLemmatizer()):
    """
    Lemmatize words using one of the WordNet engines
    
    Parameters
    ----------
    string_list : list
        List which stores strings
    engine : WordNetLemmatizer() (default) 
        An object from the nltk.stem.wodnet library

    Returns
    -------
    list
        List with the same length as *string_list* where each word in each 
        string is lemmatized

    """
    lemma_engine = engine
    cleaned_string = []
    
    for text in string_list:
        text = [lemma_engine.lemmatize(word) for word in text.split()]
        text = ' '.join(text)
        cleaned_string.append(text)     
        
    return cleaned_string    

def to_str(string_list):
    """
    Lemmatize words using one of the WordNet engines
    
    Parameters
    ----------
    string_list : list
        List which stores strings

    Returns
    -------
    list
        List with the same length as *string_list* where every list element 
        is converted to a str type object

    """
    cleaned_string = [str(x) for x in string_list]
    return cleaned_string

def rm_short_words(string_list, lower_bound=1, upper_bound=2):
    """
    Removes characters that are in the range of *lower_bound* and *upper_bound*
    
    Parameters
    ----------
    string_list : list
        List which stores strings

    lower_bound: int 
        Integer indicating the lower bound of a character length
    
    upper_bound: int
        Integer indicating the upper bound of a character length
        
    Returns
    -------
    list
        List with the same length as *string_list* where every character that is 
        split by whitespace is removed if it has a length in the range 
        [lower_bound, upper_bound]
        
    Examples
    --------
    >>> string_list = ['python is awesome', 'R is good as well']
    >>> rm_short_words(string_list)
    >>> rm_short_words(string_list, 4, 5)

    """
    
    # Constructing the regex
    regex = '\w{'
    regex += str(lower_bound)
    regex += ','
    regex += str(upper_bound)
    regex += '}'
    regex = r'\b' + regex + r'\b'
    
    # Iterating through all the string
    cleaned_string = [re.sub(regex, '', x) for x in string_list]
    return cleaned_string
    
def to_single(string_list):
    """
    Converts every word in string_list to it's singular form.
    
    Parameters
    ----------
     string_list : list
        List which stores strings
        
    Returns
    -------
     list
        List with the same length as *string_list* where every word is converted
        to singular form
    """
    cleaned_string = []
    for text in string_list:
        text = [inflection.singularize(word) for word in text.split()]
        text = ' '.join(text)
        cleaned_string.append(text)
    return cleaned_string 

def to_lower(string_list):
    """
    Makes every word in the string_list lowercase
    
    Parameters
    ----------
     string_list : list
        List which stores strings
        
    Returns
    -------
     list
        List with the same length as *string_list* where every word is converted
        to lowercase
    """
    cleaned_string = [string.lower() for string in string_list]
    return cleaned_string
    
def rm_stop_words(string_list):
    """
    Removes stop words using the nltk stopwords module.
    
    Parameters
    ----------
     string_list : list
        List which stores strings
        
    Returns
    -------
     list
        List with the same length as *string_list* where every string is without
        stopwords
    """
    cleaned_string = []
    stop_words = stopwords.words("english")   
    for text in string_list:
        text = [word for word in text.split() if word not in stop_words]
        text = ' '.join(text)
        cleaned_string.append(text)
    return cleaned_string    

def rm_punctuations(string_list):
    """
    Removes punctuations and other special characters from a string list
    
    Parameters
    ----------
     string_list : list
        List which stores strings
        
    Returns
    -------
     list
        List with the same length as *string_list* where every string is without
        punctuations and other special characters
    """
    cleaned_string = [re.sub(r"[^a-zA-Z0-9 ]"," ",s) for s in string_list]
    return cleaned_string

def rm_digits(string_list):
    """
    Removes digits from a string list
    
    Parameters
    ----------
     string_list : list
        List which stores strings
        
    Returns
    -------
     list
        List with the same length as *string_list* where every string is without
        digits
    """
    regex = re.compile('[%s]' % re.escape(string.digits))
    cleaned_string = [regex.sub('', s) for s in string_list]
    return cleaned_string

def stem_words(string_list, stemmer=nltk.stem.SnowballStemmer('english')):
    """
    A function to stemm the words in a given string vector
    
    Parameters
    ----------
     string_list : list
        List which stores strings
        
     stemmer : word stemmer from nltk.stem library;
         nltk.stem.SnowballStemmer('english') default
     
    Returns
    -------
     list
        List with the same length as *string_list* where every character is stemmed
    """
    cleaned_string = []
    for text in string_list:
        text = [stemmer.stem(word) for word in text.split()]
        text = ' '.join(text)
        cleaned_string.append(text)
    return cleaned_string  

def clean_ws(string_list):
    """
    Cleans one or more whitespaces
     
    Parameters
    ----------
     string_list : list
        List which stores strings
        
   Returns
    -------
     list
        List with the same length as *string_list* where every string has only 
        one or less whitespace
    
    """
    cleaned_string = [re.sub('\s+', ' ', s).strip() for s in string_list]
    return cleaned_string

def build_vocab(string_list, verbose = True):
    """
    A function that creates a term frequency vocabulary from the text
    
    Parameters
    ----------
     string_list : list
        List which stores strings
     verbose : boolean; default=True 
         Whether to show the timing of the for loop
         
    Returns
    -------
    vocabulary
        vocabulary that each key is a unique term in the string_list and 
        the key value is the number of times a certain term appeared in the 
        string
    
    Example
    -------
    >>> string_list = string_list = ['python is awesome', 'R is awesome as well']
    >>> build_vocab(string_list)    
        
    """
    vocab = {}
    for sentence in tqdm(string_list, disable = (not verbose)):
        for word in sentence.split():
            try:
                vocab[word] += 1
            except KeyError:
                vocab[word] = 1
    return vocab
