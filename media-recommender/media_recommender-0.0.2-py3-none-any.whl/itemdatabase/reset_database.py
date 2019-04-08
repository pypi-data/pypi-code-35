# A script for resetting server's database

import pandas as pd
from mediarecommender.recommender import db
from mediarecommender.recommender.models import Movie, Game, Book
from mediarecommender.itemdatabase.parameters import *

# Clear the database first
db.drop_all()

# Create tables for all models
db.create_all()

# Read items in DataFrame
movie_df = pd.read_csv(vectorized_movie_csv)
movie_df.set_index('id', inplace=True)
game_df = pd.read_csv(vectorized_game_csv)
game_df.set_index('id', inplace=True)
book_df = pd.read_csv(vectorized_book_csv)
book_df.set_index('id', inplace=True)

# Populate movie table
for i, row in movie_df.iterrows():
    movie = Movie(
        id=i, 
        imdb_id=row['imdb_id'], 
        title=row['title'], 
        genres=row['genres'],
        rating=row['rating'], 
        url=row['url'], 
        vector=row['vector']
        )
    db.session.add(movie)

db.session.commit()

# Populate game table
for i, row in game_df.iterrows():
    game = Game(
        id=i, 
        steam_id=row['steam_id'], 
        title=row['title'],
        rating=row['rating'], 
        url=row['url'], 
        vector=row['vector']
        )
    db.session.add(game)

db.session.commit()

# Populate book table
for i, row in book_df.iterrows():
    book = Book(
        id=i, 
        goodreads_id=row['goodreads_id'], 
        title=row['title'], 
        rating=row['rating'], 
        url=row['url'], 
        vector=row['vector']
        )
    db.session.add(book)

db.session.commit()