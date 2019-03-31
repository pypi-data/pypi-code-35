from .. import api

account = api.module("users", prefix='/accounts')

@account.route('/')
def list_users():
    return "users"
