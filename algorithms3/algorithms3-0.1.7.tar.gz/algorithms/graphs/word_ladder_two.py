'''
Given two words (beginWord and endWord), and a dictionary's word list, find all 
shortest transformation sequence(s) from beginWord to endWord, such that:

Only one letter can be changed at a time
Each transformed word must exist in the word list. Note that beginWord is not a 
transformed word.
Note:

Return an empty list if there is no such transformation sequence.
All words have the same length.
All words contain only lowercase alphabetic characters.
You may assume no duplicates in the word list.
You may assume beginWord and endWord are non-empty and are not the same.
Example 1:

Input:
beginWord = "hit",
endWord = "cog",
wordList = ["hot","dot","dog","lot","log","cog"]

Output:
[
  ["hit","hot","dot","dog","cog"],
  ["hit","hot","lot","log","cog"]
]
Example 2:

Input:
beginWord = "hit"
endWord = "cog"
wordList = ["hot","dot","dog","lot","log"]

Output: []

Explanation: The endWord "cog" is not in wordList, therefore no possible 
transformation.
'''

from collections import defaultdict, deque
import string
def generateNeighbors(word, wordList):
    for i in range(len(word)):
        for letter in string.ascii_lowercase:
            candidate = word[:i] + letter + word[i+1:]
            if candidate in wordList:
                yield candidate
def createAllPaths(parentDict, word, beginWord):
    if word == beginWord:
        return [[beginWord]]
    output = []
    for w in parentDict[word]:
       x = createAllPaths(parentDict, w, beginWord)
       for l in x:
           l.append(word)
           output.append(l)
    return output

def word_ladder_v2(beginWord, endWord, wordList):
    q = deque([beginWord ])
    seen = set([beginWord])
    wordList = set(wordList)
    parents = defaultdict(set)
    while q:
        num_in_level = len(q)
        finished = False
        seen_this_level = set()
        for i in range(num_in_level):
            q_item = q.popleft()
            for candidate in generateNeighbors(q_item, wordList):
                if candidate == endWord:
                    finished = True
                elif candidate in seen:
                    continue
                if candidate not in seen_this_level:
                    q.append(candidate)
                seen_this_level.add(candidate)
                parents[candidate].add(q_item)
        if finished:
            break
        seen |= seen_this_level
    return createAllPaths(parents, endWord, beginWord)


#print(word_ladder_v2('hit', 'cog', ["hot","dot","dog","lot","log","cog"]))
#print(word_ladder_v2('a', 'c', ['a', 'b', 'c']))

import string

def word_ladder_v3(first, last, words):
	graph = defaultdict(list)
	words.append(first)
	words = set(words)

	for word in words:
		for i in range(len(word)):
			for letter in string.ascii_lowercase:
				candidate = word[:i] + letter + word[i+1:]
				if candidate in words and candidate != word:
					graph[word].append(candidate)

	#print(graph)

	visited, path, result = set(), list(), set()
	'''
	generate_paths(first, last, visited, path, result, graph)
	minx = float('inf')
	for val in result:
		if len(val) < minx:
			minx = len(val)
	final = []
	for val in result:
		if len(val) == minx:
			final.append(val)
	return final
	'''
	
	distances = {}
	parents = defaultdict(list)
	


def generate_paths(first, last, visited, path, result, graph):
	visited.add(first)
	path.append(first)
	#print(graph, first, last)
	if first == last:
		#print(result)
		result.add(tuple(path[:]))
	else:
		for vertex in graph[first]:
			if vertex not in visited:
				generate_paths(vertex, last, visited, path, result, graph)

	path.pop()
	visited.remove(first)

def bfs(root, graph):
		que = deque([root])
		visited = set()
		result = []
		parents = {}
		parents[root] = -1

		while len(que) > 0:
			current = que.popleft()
			visited.add(current)
			result.append(current)

			for vertex in graph[current]:
				if vertex not in visited:
					parents[vertex] = current
					visited.add(vertex)
					que.append(vertex)

		return result

