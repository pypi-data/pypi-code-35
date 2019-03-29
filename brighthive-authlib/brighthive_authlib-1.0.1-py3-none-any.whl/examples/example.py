"""Quick Example Flask App to Test Auth Service."""

import json
from flask import Flask, request
from brighthive_authlib import OAuth2ProviderError, OAuth2ProviderFactory, AuthLibConfiguration, token_required


# Warning: Testing purposes only. These attributes need to be protected.
PROVIDER = 'AUTH0'
OAUTH2_URL = 'https://brighthive-test.auth0.com'
JSON_URL = '{}/.well-known/jwks.json'.format(OAUTH2_URL)
AUDIENCE = 'http://localhost:8000'
ALGORITHMS = ['RS256']

# Build the Auth Service Configuration Object
auth_config = AuthLibConfiguration(
    provider=PROVIDER, base_url=OAUTH2_URL, jwks_url=JSON_URL, algorithms=ALGORITHMS, audience=AUDIENCE)
oauth2_provider = OAuth2ProviderFactory.get_provider(PROVIDER, auth_config)


# Builed the Flask App
app = Flask(__name__)

# Add a Public Route
@app.route('/public')
def public_resource():
    return json.dumps({'message': 'You can see me because I am public!'}), 200

# Add a Private Route
@app.route('/private')
@token_required(oauth2_provider, ['get:users'])
def private_resource():
    return json.dumps({'message': 'If you can see me, you have a valid token.'}), 200

# Error Handler for Invalid or Expired Tokens
@app.errorhandler(OAuth2ProviderError)
def handle_auth_error(e):
    return json.dumps({'message': 'Access Denied'}), 401


if __name__ == '__main__':
    app.run(debug=True)
