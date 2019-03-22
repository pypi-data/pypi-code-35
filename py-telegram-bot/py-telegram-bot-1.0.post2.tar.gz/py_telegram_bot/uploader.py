from io import BufferedReader

from .exceptions import TelegramAPIException


class TelegramUploader:
    def __init__(self, bot):
        self.url = bot.url
        self.bot = bot

    def send_photo(self, chat_id, photo, **kwargs):
        if 'chat_id' not in kwargs:
            kwargs.update({'chat_id': chat_id})
        if isinstance(photo, str):
            if 'photo' not in kwargs:
                kwargs.update({'photo': photo})
            r = self.bot.session.post(self.url + '/sendPhoto', params=kwargs).json()
        elif isinstance(photo, BufferedReader):
            if 'photo' in kwargs:
                kwargs.pop('photo')

            r = self.bot.session.post(self.url + '/sendPhoto',
                                      files={'photo': photo},
                                      params=kwargs).json()
        else:
            raise TelegramAPIException('Photo must be string or file!')
        if not r['ok']:
            raise TelegramAPIException(r['description'])
        return r['result']

    def send_document(self, chat_id, document, **kwargs):
        if 'chat_id' not in kwargs:
            kwargs.update({'chat_id': chat_id})

        if isinstance(document, str):
            if 'photo' not in kwargs:
                kwargs.update({'document': document})

            r = self.bot.session.post(self.url + '/sendDocument',
                                      params=kwargs).json()

        elif isinstance(document, BufferedReader):
            if 'photo' in kwargs:
                kwargs.pop('photo')

            r = self.bot.session.post(self.url + '/sendDocument',
                                      files={'document': document},
                                      params=kwargs).json()

        else:
            raise TelegramAPIException('Document must be string or file!')
        if not r['ok']:
            raise TelegramAPIException(r['description'])
        return r['result']

    def send_video(self, chat_id, video, **kwargs):
        if 'chat_id' not in kwargs:
            kwargs.update({'chat_id': chat_id})

        if isinstance(video, str):
            if 'video' not in kwargs:
                kwargs.update({'video': video})

            r = self.bot.session.post(self.url + '/sendVideo',
                                      params=kwargs).json()

        elif isinstance(video, BufferedReader):
            if 'video' in kwargs:
                kwargs.pop('video')

            r = self.bot.session.post(self.url + '/sendVideo',
                                      files={'video': video},
                                      params=kwargs).json()

        else:
            raise TelegramAPIException('Video must be string or file!')
        if not r['ok']:
            raise TelegramAPIException(r['description'])
        return r['result']
