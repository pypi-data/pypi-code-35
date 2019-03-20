"""
Main execution script. Launches Flask application to respond to requests.
"""
from flask import Flask
from flask_cors import CORS

if __name__ == "__main__":
    T_ADJ = 0
    APP = Flask(__name__)
    CORS(APP, resources={r"/*": {"origins": "http://senorpez.com"}})

    APP.run(host="0.0.0.0", port=5002)
