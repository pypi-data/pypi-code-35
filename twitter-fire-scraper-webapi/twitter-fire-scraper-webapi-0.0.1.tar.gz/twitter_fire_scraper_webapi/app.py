import os
from flask import Flask, request, render_template, jsonify, url_for, abort, Response
import twitter_fire_scraper
from twitter_fire_scraper.scraper import Scraper
from twitter_fire_scraper.twitter import TwitterAuthentication
from twitter_fire_scraper.util import jsonify_status_dict

app = Flask(__name__, static_url_path="/static")
scraper = Scraper(twitter_authentication=TwitterAuthentication.autodetect_twitter_auth())

@app.route('/scrape_terms', methods=['GET'])
def scrape_terms():

    count = request.args.get("count")
    if not count:
        abort(400, "'count' is a required URL parameter!")

    try:
        count = int(count)

        if count < 0:
            raise ValueError
    except ValueError:
        abort(400, "'count' should be a valid number!")

    terms = request.args.get("terms")

    if not terms:
        abort(400, "'terms' is a required URL parameter!")

    terms = terms.split(",")
    if len(terms) <= 0:
        abort(400, "'terms' cannot be an empty list!")

    geocode = request.args.get("geocode")

    results = (scraper.scrape_terms(terms=terms, count=count, geocode=geocode))

    results = jsonify_status_dict(results)

    return jsonify(results)

@app.route('/info', methods=['GET'])
def info():
    return "twitter-fire-scraper-webapi"

@app.route('/')
def index():
    return jsonify({'json': 'hacked'})

@app.route('/add/<int:x>/<int:y>', methods=['GET'])
def add_numbers(x, y):
    return str(x+y)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3620))

    app.run(host="127.0.0.1", port=port, debug=True)
