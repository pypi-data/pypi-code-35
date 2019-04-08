from enum import Enum
import numpy as np
from sklearn.neighbors import NearestNeighbors
from mediarecommender.recommender.models import Movie, Game, Book


class Media(Enum):
    MOVIE = 'Movie'
    GAME = 'Game'
    BOOK = 'Book'


class Recommender:
    def __init__(self, user_favorites_dict):
        self.user_favorites_dict = user_favorites_dict
        self.user_vector = self.__user_favorites_to_user_vector()

    def generate_k_recommendations(self, media_type, k):
        item_vectors = []
        all_items_without_favorites = []

        if media_type == Media.MOVIE:
            favorite_movies_id = self.__get_favorites_id('Movie')
            all_items_without_favorites = Movie.query.filter(~Movie.id.in_(favorite_movies_id), Movie.rating > 6.5).all()
            item_vectors = np.vstack([np.fromstring(movie.vector, dtype=float, sep=' ') for movie in all_items_without_favorites])
        elif media_type == Media.GAME:
            favorite_games_id = self.__get_favorites_id('Game')
            all_items_without_favorites = Game.query.filter(~Game.id.in_(favorite_games_id), Game.rating > 65.0).all()
            item_vectors = np.vstack([np.fromstring(game.vector, dtype=float, sep=' ') for game in all_items_without_favorites])
        elif media_type == Media.BOOK:
            favorite_books_id = self.__get_favorites_id('Book')
            all_items_without_favorites = Book.query.filter(~Book.id.in_(favorite_books_id), Book.rating > 3.0).all()
            item_vectors = np.vstack([np.fromstring(book.vector, dtype=float, sep=' ') for book in all_items_without_favorites])
        else:
            print('Unknown media type: generate_k_recommendations')
            return
        nbrs = NearestNeighbors(n_neighbors=k, algorithm='brute').fit(item_vectors)
        _, indices = nbrs.kneighbors(self.user_vector)
        
        recommended_movies = []

        for i in indices[0]:
            recommended_movie_dict = {
                'id': all_items_without_favorites[i].id,
                'title': all_items_without_favorites[i].title, 
                'url': all_items_without_favorites[i].url
            }
            recommended_movies.append(recommended_movie_dict)

        return recommended_movies

    def __user_favorites_to_user_vector(self):
        favorite_vectors = []
        
        for f in self.user_favorites_dict['favorites']:
            item_id = int(f['id'])
            media_type = f['type']
            
            if Media(media_type) == Media.MOVIE:
                movie = Movie.query.filter(Movie.id == item_id).first()
                favorite_vectors.append(np.fromstring(movie.vector, dtype=float, sep=' '))
            elif Media(media_type) == Media.GAME:
                game = Game.query.filter(Game.id == item_id).first()
                favorite_vectors.append(np.fromstring(game.vector, dtype=float, sep=' '))
            elif Media(media_type) == Media.BOOK:
                book = Book.query.filter(Book.id == item_id).first()
                favorite_vectors.append(np.fromstring(book.vector, dtype=float, sep=' '))
            else:
                print('Unknown media type: __user_favorites_to_user_vector')
                return

        return np.mean(np.asarray(favorite_vectors), axis=0).reshape(1, -1)

    def __get_favorites_id(self, media_type):
        favorites_id = []

        for f in self.user_favorites_dict['favorites']:
            item_id = f['id']
            f_media_type = f['type']

            if Media(f_media_type) == Media(media_type):
                favorites_id.append(item_id)

        return favorites_id