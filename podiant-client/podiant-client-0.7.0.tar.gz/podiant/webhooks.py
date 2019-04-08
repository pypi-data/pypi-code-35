from . import settings
from .api import Client
from .exceptions import UnknownError
import json
import requests


class WebhookMetaCollection(object):
    def __init__(self, data):
        for key, value in data.items():
            setattr(self, key, value)


class Webhook(object):
    def __init__(self, stream):
        data = json.loads(stream.decode('utf-8'))

        self.meta = WebhookMetaCollection(
            data.get('meta', {})
        )

        try:
            client = Client(data['meta']['access_token'])
            assert data['type'] == 'events'
            self.id = data['id']

            obj = data['attributes'].pop('object')
            assert 'type' in obj
            assert 'id' in obj

            collection = getattr(client, obj['type'])
            self.object = collection.filter(id=obj['id'])

            for key, value in data['attributes'].items():
                setattr(self, key, value)

            links = data.get('links', {})
            postback_url = links.get('postback')

            if postback_url:
                def postback(data):
                    response = requests.post(
                        postback_url,
                        params={
                            'client_id': settings.CLIENT_ID
                        },
                        headers={
                            'Authorization': 'Bearer %s' % (
                                settings.CLIENT_SECRET
                            ),
                            'Content-Type': 'application/vnd.api+json',
                            'Accepts': 'application/vnd.api+json'
                        },
                        data=json.dumps(
                            {
                                'data': data
                            }
                        )
                    )

                    response.raise_for_status()

                self.postback = postback

        except (AssertionError, KeyError):
            raise UnknownError(
                'Data does not conform to expected Webhook object.'
            )
