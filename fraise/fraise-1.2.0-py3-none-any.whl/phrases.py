from . import words


def generate(word_count=4, minimum_length=16, separator=' '):
    word_list = []
    for _ in range(word_count):
        word_list.append(words.get_random_word())
    passphrase = separator.join(map(str, word_list))
    while len(passphrase) < minimum_length:
        passphrase += f' {words.get_random_word()}'
    return passphrase
