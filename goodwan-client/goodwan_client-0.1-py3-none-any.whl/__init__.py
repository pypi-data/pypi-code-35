"""
GoodWan client library.
Usage:
from goodwan_client import Client

client = Client(api_login, api_password)
client.events(from=from_datetime, to=to_datetime, device_id=123)
"""

from goodwan_client.client import Client
