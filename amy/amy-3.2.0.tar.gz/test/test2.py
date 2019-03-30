from fbchat import Client
from fbchat.models import *

client = Client('aussprung.c@aon.at', 'pw')

print('Own id: {}'.format(client.uid))

client.send(Message(text='Hi me!'), thread_id=client.uid, thread_type=ThreadType.USER)

client.logout()