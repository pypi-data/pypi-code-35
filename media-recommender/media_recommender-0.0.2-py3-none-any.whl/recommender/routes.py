from flask import render_template, url_for, request, jsonify
import pandas as pd
import numpy as np
import json
from mediarecommender.recommender import app
from mediarecommender.recommender import db
from mediarecommender.recommender.models import Movie, Game, Book
from mediarecommender.recommender.recommender import Recommender, Media


@app.route("/")
def home():
    return render_template('home.html', title='Media Recommender')


@app.route("/search", methods=['GET'])
def search():
    query = request.args.get('query')
    movie_results = Movie.query.filter(Movie.title.like('%' + query + '%')).all()
    game_results = Game.query.filter(Game.title.like('%' + query + '%')).all()
    book_results = Book.query.filter(Book.title.like('%' + query + '%')).all()
    results = movie_results + game_results + book_results
    results_list_of_dict = [{'id': r.id, 'title': r.title, 'type': type(r).__name__} for r in results][0:10]
    return jsonify({'results': results_list_of_dict})


@app.route("/submit", methods=['GET'])
def submit():
    favorites_json = request.args.get('favorites')
    favorites_dict = json.loads(favorites_json)
    r = Recommender(favorites_dict)

    # Generate recommendation
    movie_recommendation = r.generate_k_recommendations(Media.MOVIE, 5)
    game_recommendation = r.generate_k_recommendations(Media.GAME, 5)
    book_recommendation = r.generate_k_recommendations(Media.BOOK, 5)
    
    return jsonify({
        'movie': movie_recommendation,
        'game': game_recommendation,
        'book': book_recommendation
    })


    
        