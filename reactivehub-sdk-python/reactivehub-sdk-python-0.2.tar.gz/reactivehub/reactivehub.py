import requests
import json

class Client:
  def __init__(self, team_name, client_key, client_secret):
    if (team_name == None or client_key == None or client_secret == None):
      raise ValueError('Empty values are not allowed. Please instantiate a Client class with your team name, client key and client secret')
    self.team_name = team_name
    self.client_key = client_key
    self.client_secret = client_secret

  def publish_event(self, event_name, payload):
    headers = {"Content-type": "application/json",
              "client_key": self.client_key,
              "client_secret": self.client_secret}
    url = 'https://{team_name}.reactivehub.io/event/{event_name}'.format(team_name=self.team_name, event_name=event_name)
    return requests.post(url, data=json.dumps(payload), headers=headers)
