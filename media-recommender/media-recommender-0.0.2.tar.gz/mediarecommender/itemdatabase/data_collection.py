from imdb import IMDb
from requests.exceptions import RequestException
from xml.sax._exceptions import SAXException
from bs4 import BeautifulSoup
import requests
import pandas as pd
import xml.sax
import untangle
import time
from mediarecommender.itemdatabase.parameters import *


def extract_movies(num_of_samples):
    imdb_ids = read_sample_movies_imdb_id()[0:num_of_samples]
    ia = IMDb()
    movie_df = pd.DataFrame(columns=['id', 'imdb_id', 'title', 'genres', 'rating', 'url', 'documents'])
    
    for i, imdb_id in enumerate(imdb_ids):
        try:
            movie = ia.get_movie(imdb_id, info=['main', 'synopsis', 'plot'])
            title = f"{movie['title']} ({str(movie['year'])})"
            print(f'Extracting movies, title = {title}, imdb_id = {imdb_id}, iter = {i}')
            genres = '::'.join(movie['genre'])
            url = f'https://www.imdb.com/title/tt{imdb_id}'
            rating = 0.0
            synopsis = []
            plot_list = []
            reviews = scrap_movie_reviews(imdb_id)
            if 'rating' in movie:
                rating = movie['rating']
            if 'synopsis' in movie:
                synopsis = movie['synopsis']
            if 'plot' in movie:
                plot_list = [summary.split('::')[0] for summary in movie['plot']]
            document_list = synopsis + plot_list + reviews
            movie_df.loc[len(movie_df)] = [len(movie_df), imdb_id, title, genres, rating, url, '::'.join(document_list)]
        except:
            continue

    movie_df.to_csv(raw_movie_csv, index=False, sep=',', encoding='utf-8') 


def extract_games(num_of_samples):
    games = read_sample_games()[0:num_of_samples]
    game_df = pd.DataFrame(columns=['id', 'steam_id', 'title', 'rating', 'url', 'documents'])
    
    for i, g in enumerate(games):
        steam_id = g[0]
        release_date = g[2]
        title = g[1]
        year = release_date[len(release_date)-4:]
        rating = g[3]
        description = g[4]
        site_detail_url = f'https://store.steampowered.com/app/{str(steam_id)}'
        retry_count = 0
        while True:
            try:
                # Search IGN review
                review_p_list = []
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
                url = f'https://uk.ign.com/search?q={title}&page=0&count=1&type=article&filter=articles'
                html = requests.get(url, headers=headers).text
                soup = BeautifulSoup(html, 'html.parser')
                search_item_title = soup.find('div', class_='search-item-title')
                if search_item_title == None:
                    break
                review_url = search_item_title.find('a')['href']
                response = requests.get(review_url, headers=headers)
                print(f"Extracting games, title = {title}, steam_id = {steam_id}, response = {response}, iter = {i}")
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                body = soup.find('body', attrs={'layout': 'default-html5'})
                if body == None:
                    print('body == None')
                    break
                article_content = body.find('div', attrs={'id': 'article-content'})
                if article_content == None:
                    print('article_content == None')
                    break
                review_ps = article_content.find_all('p')
                for p in review_ps:
                    review_p_list.append(p.getText())
                document = description + '::' + ' '.join(review_p_list)
                game_df.loc[len(game_df)] = [len(game_df), steam_id, f'{title} ({year})', rating, site_detail_url, document]
            except RequestException:
                print(f'Requests error when extracting {title}, steam_id = {steam_id}, retrying, count = {str(retry_count)}')
                time.sleep(request_error_sleep_seconds)
                retry_count += 1
                if retry_count > request_error_retry_limit:
                    break
                continue
            break

    game_df.to_csv(raw_game_csv, index=False, sep=',', encoding='utf-8')


def extract_books(num_of_samples):
    goodreads_books_ids = read_sample_books_goodreads_ids()[0:num_of_samples]
    book_df = pd.DataFrame(columns=['id', 'goodreads_id', 'title', 'rating', 'url', 'documents'])

    for i, goodreads_book_id in goodreads_books_ids.iteritems():
        while True:
            try:
                print(f'Extracting books, id = {str(goodreads_book_id)}, iter = {i}')
                url = 'https://www.goodreads.com/book/show/?id=' + str(goodreads_book_id) + '&format=xml&key=CoBtO9PVTZqNZ5tDLr9yGQ'
                detail_url = 'https://www.goodreads.com/book/show/?id=' + str(goodreads_book_id)
                parsed_xml = untangle.parse(url)
                year = parsed_xml.GoodreadsResponse.book.publication_year.cdata
                title = f'{parsed_xml.GoodreadsResponse.book.title.cdata} ({year})'
                print(f'Book title: {title}')
                rating = parsed_xml.GoodreadsResponse.book.average_rating.cdata
                description = parsed_xml.GoodreadsResponse.book.description.cdata
                book_df.loc[len(book_df)] = [len(book_df), goodreads_book_id, title, rating, detail_url, description]
            except RequestException:
                print('Requests error, retrying...')
                continue
            except SAXException:
                print('Non-xml response, skipping')
                break
            break

    book_df.to_csv(raw_book_csv, index=False, sep=',', encoding='utf-8')


def scrap_movie_reviews(id):
    url = f'https://www.imdb.com/title/tt{id}/reviews'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')
    main = soup.find('div', attrs={'id': 'main'})
    review_divs = main.find_all('div', class_='text show-more__control')
    reviews = [rd.text for rd in review_divs]
    return reviews


def read_sample_movies_imdb_id():
    dtypes = {'movieId': 'int', 'imdbId': 'str', 'tmdbId': 'str'}
    movie_imdb_ids_df = pd.read_csv(movie_samples_csv, sep=',', dtype=dtypes, encoding='utf-8')
    return movie_imdb_ids_df['imdbId'].values


def read_sample_games():
    game = pd.read_csv(game_samples_csv, sep=',', encoding='utf-8')
    return game[['ResponseID', 'ResponseName', 'ReleaseDate', 'Metacritic', 'DetailedDescrip']].values


def read_sample_books_goodreads_ids():
    books_df = pd.read_csv(book_samples_csv, encoding='utf-8')
    books_df.set_index('id', inplace=True)
    return books_df['book_id']


def main():
    extract_movies(num_of_movie_samples)
    extract_games(num_of_game_samples)
    extract_books(num_of_book_samples)


if __name__ == '__main__':
    main()