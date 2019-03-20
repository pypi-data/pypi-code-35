from pyctogram.instagram_client import client
from pyctogram.instagram_client import web


if __name__ == '__main__':
    insta_client = client.InstagramClient('ruzzy_rullezz', 'heckfy20')
    insta_client.login()
    response = insta_client.like('1999209083546506513_11648210360')
    print(response)
