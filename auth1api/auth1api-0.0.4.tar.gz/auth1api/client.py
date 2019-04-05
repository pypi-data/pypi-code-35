import requests

class Auth1Client(object):
    def __init__(self, base_url):
        self.base_url = base_url

    def register(self, username, email, password):
        req_body ={'username': username, 'email': email, 'password': password} 
        r = requests.post(f'{self.base_url}/register',
                          data=req_body)
        return r.json()

    def login(self, username_or_email, username, email, password):
        req_body = {'password': password}
        if username_or_email:
            req_body['usernameOrEmail'] = username_or_email
        elif username:
            req_body['username'] = username
        elif email:
            req_body['email'] = email
        
        r = requests.post(f'{self.base_url}/login', data=req_body)
        return r.json()

    def check_auth_token(self, token):
        if not token:
            print("No token provided")
            return None, False

        req_body = {'token': token}
        r = requests.post(f'{self.base_url}/checkAuthToken', data=req_body)
        return r.json()

    def get_password_reset_token(self, username_or_email, username, email):
        req_body = {}
        if username_or_email:
            req_body['usernameOrEmail'] = username_or_email
        elif username:
            req_body['username'] = username
        elif email:
            req_body['email'] = email
        
        r = requests.post(f'{self.base_url}/getPasswordResetToken', data=req_body)
        return r.json()

    # Returns boolean indicating reset success
    def reset_password(self, token, new_password):
        req_body = {'token': token, 'newPassword': new_password}
        r = requests.post(f'{self.base_url}/resetPassword', data=req_body)
        return r.json()

# client = Auth1Client("http://localhost:8080")
# client.register("brianli", "brian@li.com", "hello")
# token, exp_time = client.login("brianli", "brianli", "brian@li.com", "hello")
# client.check_auth_token(token)
# reset_token, exp_time = client.get_password_reset_token("brianli", "brianli", "brian@li.com")
# client.reset_password(reset_token, "welldone")
# token, exp_time = client.login("brianli", "brianli", "brian@li.com", "hello") # Expect failure
# token, exp_time = client.login("brianli", "brianli", "brian@li.com", "welldone") # Expect success

