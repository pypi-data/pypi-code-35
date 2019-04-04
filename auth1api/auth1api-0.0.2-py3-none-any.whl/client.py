import requests

class Auth1Client(object):
    def __init__(self, base_url):
        self.base_url = base_url

    # Returns boolean indicating success
    def register(self, username, email, password):
        if not username:
            print("No username provided")
            return False
        elif not email:
            print("No email provided")
            return False
        elif not password:
            print("No password provided")
            return False

        req_body ={'username': username, 'email': email, 'password': password} 
        r = requests.post(f'{self.base_url}/register',
                          data=req_body)
        if r.status_code == 200:
            res = r.json()
            if res['result'] == 'SUCCESS':
                return True
            else:
                return False
        else:
            print(f"Auth1 error: {r.text}")
            return False

    # Returns tuple of (auth_token, token_expiration_time)
    def login(self, username_or_email, username, email, password):
        req_body = {'password': password}
        if username_or_email:
            req_body['usernameOrEmail'] = username_or_email
        elif username:
            req_body['username'] = username
        elif email:
            req_body['email'] = email
        else:
            print("No email or username provided")
            return None, None
        
        r = requests.post(f'{self.base_url}/login', data=req_body)
        if r.status_code == 200:
            res = r.json()
            if res['resultType'] == 'SUCCESS':
                return res['token']['tokenValue'], res['token']['expirationTime']
            else:
                return None, None
        else:
            print(f"Auth1 error: {r.text}")
            return None, None

    # Returns tuple of (user_id, token_is_valid)
    def check_auth_token(self, token):
        if not token:
            print("No token provided")
            return None, False

        req_body = {'token': token}
        r = requests.post(f'{self.base_url}/checkAuthToken', data=req_body)
        if r.status_code == 200:
            res = r.json()
            return res['username'], res['valid']
        else :
            print(f"Auth1 error: {r.text}")
            return None, False

    # Returns tuple of (password_reset_token, token_expiration_time)
    def get_password_reset_token(self, username_or_email, username, email):
        req_body = {}
        if username_or_email:
            req_body['usernameOrEmail'] = username_or_email
        elif username:
            req_body['username'] = username
        elif email:
            req_body['email'] = email
        else:
            print("No email or username provided")
            return None, None
        
        r = requests.post(f'{self.base_url}/getPasswordResetToken', data=req_body)
        if r.status_code == 200:
            res = r.json()
            if res['resultType'] == 'SUCCESS':
                return res['token']['tokenValue'], res['token']['expirationTime']
            else:
                return None, None
        else:
            print(f"Auth1 error: {r.text}")
            return None, None 

    # Returns boolean indicating reset success
    def reset_password(self, token, new_password):
        if not token:
            print("No token provided")
            return False
        elif not new_password:
            print("No new password provided")
            return False

        req_body = {'token': token, 'newPassword': new_password}
        r = requests.post(f'{self.base_url}/resetPassword', data=req_body)
        if r.status_code == 200:
            res = r.json()
            return res["result"] == "SUCCESS"
        else:
            print(f"Auth1 error: {r.text}")
            return False

# client = Auth1Client("http://localhost:8080")
# # client.register("brianli", "brian@li.com", "hello")
# token, exp_time = client.login("brianli", "brianli", "brian@li.com", "hello")
# client.check_auth_token(token)
# reset_token, exp_time = client.get_password_reset_token("brianli", "brianli", "brian@li.com")
# client.reset_password(reset_token, "welldone")
# token, exp_time = client.login("brianli", "brianli", "brian@li.com", "hello") # Expect failure
# token, exp_time = client.login("brianli", "brianli", "brian@li.com", "welldone") # Expect success

