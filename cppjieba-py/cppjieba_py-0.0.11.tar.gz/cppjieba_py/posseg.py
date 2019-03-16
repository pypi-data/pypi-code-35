
import libcppjieba

def cut(sentence,HMM=False):
       it = libcppjieba.tag(sentence)
       return iter(it)

def lcut(sentence,HMM=False):
    return libcppjieba.tag(sentence)