#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
from slugify import slugify
from fuzzywuzzy import fuzz


# In[6]:


def build_ngrams(line, count, stopwords, replacements):
    normalised_line = slugify(
        line, separator=" ", stopwords=stopwords, replacements=replacements
    )
    tokens = normalised_line.split()
    sequences = [tokens[i:] for i in range(count)]
    ngrams = zip(*sequences)
    ngram_list = []
    for row in ngrams:
        ngram_list.append("_".join(row))
    return ngram_list


# In[ ]:


def build_ngram_list(text, ngram_count, stopwords, replacements):
    ngram_list = []
    for n in range(5, 1, -1):
        ngram_list.extend(build_ngrams(text, n, stopwords, replacements))
    return ngram_list


# In[10]:


def match_name(name_to_match, list_names):
    max_score = -1
    max_name = ""
    for name in list_names:
        name = name.lower()
        score = fuzz.token_set_ratio(name_to_match, name)
        if score > max_score:
            if type(list_names) == dict:
                max_name = list_names[name]
            else:
                max_name = name
            max_score = score
    return (max_name, max_score)


# In[ ]:


def get_best_match(company_list, ngram_list, stopwords=[], replacements=[]):
    top_name = ("Missing", 0)
    for item in company_list:
        item = slugify(
            item, separator="_", stopwords=stopwords, replacements=replacements
        )
        print("------------------")
        print()
        print(item, ":")
        result = match_name(item, ngram_list)
        if result[1] > top_name[1]:
            top_name = result
            short_name = item
        print()
    return short_name, top_name


# In[ ]:
