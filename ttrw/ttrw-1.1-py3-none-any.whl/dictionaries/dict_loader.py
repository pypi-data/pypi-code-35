from os import path, walk

words = {}

path_to_dictionaries = path.dirname(path.abspath(__file__))

# get a list of directories in dictionaries
languages = [x for x in next(walk(path_to_dictionaries))[1] if not x.startswith("_")]

# fill words dictionary with all the languages and words
for lang in languages:

    with open(path.join(path_to_dictionaries, lang, "adverbs.txt"), "r") as f:
        adv = list(f)

    with open(path.join(path_to_dictionaries, lang, "adjectives.txt"), "r") as f:
        adj = list(f)

    with open(path.join(path_to_dictionaries, lang, "nouns.txt"), "r") as f:
        nou = list(f)

    words[lang] = {
        "adverbs": adv,
        "adjectives": adj,
        "nouns": nou
    }
