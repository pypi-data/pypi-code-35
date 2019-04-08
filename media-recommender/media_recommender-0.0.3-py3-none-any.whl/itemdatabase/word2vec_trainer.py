from gensim.utils import simple_preprocess
from gensim.test.utils import get_tmpfile
from gensim.models import Word2Vec
import pandas as pd
import csv
from mediarecommender.itemdatabase.data_preprocessing import lemmatize_words
from mediarecommender.itemdatabase.data_preprocessing import remove_html_tags
from mediarecommender.itemdatabase.data_preprocessing import preprocess_text_for_word2vec
from mediarecommender.itemdatabase.parameters import *


def prepare_word2vec_training_data():
    processed_book_documents = read_book_documents()
    processed_game_documents = read_game_documents()
    processed_movie_documents = read_movie_documents()
    return processed_movie_documents + processed_game_documents + processed_book_documents


def read_movie_documents():
    movies_df = pd.read_csv(raw_movie_csv)
    documents = movies_df['documents'].values
    processed_documents = []
    with open(movie_samples_csv, encoding='utf-8') as movie_metadata_csv:
        csv_reader = csv.reader(movie_metadata_csv, delimiter=',')
        for i, row in enumerate(csv_reader):
            print(f'Reading movie documents, iter = {i}, file = movies_metadata.csv')
            if i != 0:
                d = row[9]
                processed_d = preprocess_text_for_word2vec(d)
                processed_documents.append(processed_d)
    for i, d in enumerate(documents):
        print(f'Reading movie documents, iter = {i}, file = raw_movies.csv')
        if pd.notna(d):
            d_list = d.split('::')
            for el in d_list:
                processed_documents.append(preprocess_text_for_word2vec(el))
    return processed_documents


def read_game_documents():
    games_df = pd.read_csv(raw_game_csv)
    documents = games_df['documents'].values
    processed_documents = []
    for i, d in enumerate(documents):
        print(f'Reading game documents, iter = {i}, file = games_metadata.csv')
        if pd.notna(d):
            d_list = d.split('::')
            for el in d_list:
                processed_documents.append(preprocess_text_for_word2vec(el))
    return processed_documents


def read_book_documents():
    books_df = pd.read_csv(raw_book_csv)
    documents = books_df['documents'].values
    processed_documents = []
    with open(book_samples_csv, encoding='utf-8') as book_metedata_csv:
        csv_reader = csv.reader(book_metedata_csv, delimiter='\t')
        for i, row in enumerate(csv_reader):
            print(f'Reading book documents, iter = {i}, file = books_metadata.csv')
            if i != 0:
                d = row[6]
                processed_d = preprocess_text_for_word2vec(d)
                processed_documents.append(processed_d)
    for i, d in enumerate(documents):
        print(f'Reading book documents, iter = {i}, file = raw_books.csv')
        if pd.notna(d):
            d_list = d.split('::')
            for el in d_list:
                processed_documents.append(preprocess_text_for_word2vec(el))
    return processed_documents


def word2vec_train(training_documents):
    print(f'Total number of training examples: {str(len(training_documents))}')
    print('Training model...')
    model = Word2Vec(training_documents, size=50, min_count=2, workers=4)
    model.train(training_documents, total_examples=len(training_documents), epochs=10)
    print('Model trained')
    return model


def save_model_vectors(model):
    word_vectors = model.wv
    word_vectors.save(word_vectors_kv)


def main():
    training_documents = prepare_word2vec_training_data()
    model = word2vec_train(training_documents)
    save_model_vectors(model)


if __name__ == '__main__':
    main()
    