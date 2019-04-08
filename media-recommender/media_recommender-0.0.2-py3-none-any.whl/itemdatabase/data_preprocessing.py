import nltk
import pandas as pd
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from unidecode import unidecode
from mediarecommender.itemdatabase.parameters import *


def extract_nouns_and_adjs(tokenized_text):
    tagged_text = nltk.pos_tag(tokenized_text)
    grammar = 'NOUN_OR_ADJ:{<NN>||<JJ>}'
    parse_result = nltk.RegexpParser(grammar).parse(tagged_text)
    nouns_and_adjs = []
    
    for elem in parse_result:
        if type(elem) == nltk.tree.Tree:
            nouns_and_adjs.append(' '.join([pair[0] for pair in elem.leaves()]))

    return nouns_and_adjs


def lemmatize_words(tokenized_text):
    lemmatizer = WordNetLemmatizer()
    lemmatized_text = []
    tagged_text = nltk.pos_tag(tokenized_text)
    
    for pair in tagged_text:
        if pair[1] == 'NN':
            lemmatized_text.append(lemmatizer.lemmatize(pair[0], pos='n'))
        elif pair[1] == 'JJ':
            lemmatized_text.append(lemmatizer.lemmatize(pair[0], pos='a'))

    return lemmatized_text


def remove_html_tags(text):
    soup = BeautifulSoup(text, 'lxml')
    return soup.get_text()


def replace_accents(text):
    return unidecode(text)


def replace_simple_apostrophe(text):
    return re.sub(r'’+', '\'', text)


def remove_non_alphabet_and_useless_symbols(text):
    return re.sub(r'[^a-zA-Z-\'’]+', ' ', text)


def remove_stop_words(word_list):
    filtered_word_list = []
    stop_words = set(stopwords.words('english'))
    for w in word_list:
        if w not in stop_words:
            filtered_word_list.append(w)
    return filtered_word_list


def preprocess_text(text):
    text_no_html_tags = remove_html_tags(text)
    text_simple_apostrophe = replace_simple_apostrophe(text_no_html_tags)
    text_accents_replaced = replace_accents(text_simple_apostrophe)
    text_alphabets_dash_apostrophe = remove_non_alphabet_and_useless_symbols(text_accents_replaced)
    text_accents_replaced = replace_accents(text_alphabets_dash_apostrophe)
    tokenized_text = nltk.word_tokenize(text_accents_replaced)
    nouns_and_adjs = extract_nouns_and_adjs(tokenized_text)
    lemmatized_text = lemmatize_words(nouns_and_adjs)
    return ' '.join(lemmatized_text)


def preprocess_text_for_word2vec(text):
    text_no_html_tags = remove_html_tags(text)
    text_simple_apostrophe = replace_simple_apostrophe(text_no_html_tags)
    text_accents_replaced = replace_accents(text_simple_apostrophe)
    text_alphabets_dash_apostrophe = remove_non_alphabet_and_useless_symbols(text_accents_replaced)
    text_accents_replaced = replace_accents(text_alphabets_dash_apostrophe)
    tokenized_text = nltk.word_tokenize(text_accents_replaced)
    text_no_stop_words = remove_stop_words(tokenized_text)
    lemmatized_text = lemmatize_words(text_no_stop_words)
    return lemmatized_text


def preprocess_item_documents(in_file_str, out_file_str):
    item_df = pd.read_csv(in_file_str)
    item_df.set_index('id', inplace=True)
    item_remove_id = []
    
    for i, row in item_df.iterrows():
        print(f'Preprocessing {in_file_str}, item id = {str(i)}')
        if pd.isnull(item_df.at[i, 'documents']):
            item_remove_id.append(i)
        else:
            item_df.at[i, 'title'] = row['title'].replace(',', ' ')
            documents = row['documents'].split('::')
            keywords = ' '.join([preprocess_text(d) for d in documents])
            if keywords != '':
                item_df.at[i, 'documents'] = keywords
            else:
                item_remove_id.append(i)

    print(f'Id of items to be removed: {item_remove_id}')
    item_df.drop(item_remove_id, inplace=True)
    item_df.rename(columns = {'documents': 'words'}, inplace=True)
    item_df.to_csv(out_file_str, sep=',', encoding='utf-8')


def main():
    preprocess_item_documents(raw_movie_csv, preprocessed_movie_csv)
    preprocess_item_documents(raw_game_csv, preprocessed_game_csv)
    preprocess_item_documents(raw_book_csv, preprocessed_book_csv)


if __name__ == '__main__':
    main()