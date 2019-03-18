from tdameritrade_client.auth import TDAuthenticator

def test_tdauth_server():
    td_auth = TDAuthenticator(host='127.0.0.1', port=8080,
                              oauth_client_id='DATASOURCECAS@AMER.OAUTHAP',
                              token_path='asdf')
    td_auth.authenticate()
