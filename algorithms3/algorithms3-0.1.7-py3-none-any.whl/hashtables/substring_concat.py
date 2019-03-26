'''
You are given a string, s, and a list of words, words, that are all of the same length. 
Find all starting indices of substring(s) in s that is a concatenation of each word in words 
exactly once and without any intervening characters.

Example 1:
Input:
  s = "barfoothefoobarman",
  words = ["foo","bar"]
Output: [0,9]
Explanation: Substrings starting at index 0 and 9 are "barfoor" and "foobar" respectively.
The output order does not matter, returning [9,0] is fine too.

Example 2:
Input:
  s = "wordgoodgoodgoodbestword",
  words = ["word","good","best","word"]
Output: []
'''

def substring_concat(s:str, words:list) -> list:
    if not s or not words:
        return []
    words_len = len(words) * len(words[0])
    
    target_hash = 0
    for word in words:
        target_hash += hash(word)

    result = []
    for i in range(len(s) - words_len + 1):
        words_hash = 0
        for j in range(i, i+words_len-1, len(words[0])):
            words_hash += hash(s[j:j+len(words[0])])

        if target_hash == words_hash:
            result.append(i)
    
    return result


