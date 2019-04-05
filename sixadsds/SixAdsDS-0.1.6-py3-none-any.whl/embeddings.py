"""
Class for dealing with word embeddings
"""

import numpy as np

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

def load_from_text(path):
    """
    Reads the word embeddings from a txt documents and saves it as a dictionary
    
    Parameters
    ----------
    
    **path**: string
        path to a txt document containing the word embeddings
    
    Returns
    -------
    
        A dictionary where the key values are individual words and the 
        values are the vectors
    """
    def get_coefs(word,*arr): return word, np.asarray(arr, dtype='float32')
    emb = dict(get_coefs(*o.split(" ")) for o in open(path, 
                                                      encoding = 'utf-8',
                                                      errors='ignore'))
    return emb

def tokenize_text(string_list, max_features, max_len):
    """
    Creates a tokenizer from a given text list
    
    Parameters
    ----------
    
    **string_list**: list
        List containing strings
        
    **max_features**: int
        The maximum number of unique words that the tokenizer saves in memory
        
    **max_len**: int
        The length of the vector into which all elements of *string_list* will
        be converted to.
    
    Returns
    -------
    
        A tuple of the tokenized text and the fitted tokenizer for future use.
        The first element of the tuple is an array of shape (len(*string_list*), max_len)
    """
    
    tokenizer = Tokenizer(num_words = max_features)
    tokenizer.fit_on_texts(string_list)
    token = tokenizer.texts_to_sequences(string_list)
    token = pad_sequences(token, maxlen = max_len)
    
    return token, tokenizer

def create_embedding_matrix(embeddings, tokenizer, max_features, 
                            embed_size = 300): 
    """
    Function to create the embedding matrix to use in neural networks. This goes 
    directly to the embedding layer.
    
    Parameters
    ----------
    
    **embeddings**: dictionary
        output of load_from_text() function
        
    **tokenizer**: keras.Tokenizer object
        output of tokenize_text() function
        
    **max_features**: int
        how many unique tokens to use
        
    **embed_size**: int
        how many coordinates does the embedding have; default=300
    
    Returns
    -------
    
        A numpy.ndarray of shape (max_features, embed_size)
    """
    
    embedding_matrix = np.zeros((max_features, embed_size))
    for word, index in tokenizer.word_index.items():
        if index > max_features - 1:
            break
        else:
            try:
                embedding_matrix[index] = embeddings[word]
            except:
                continue
    return embedding_matrix        
    