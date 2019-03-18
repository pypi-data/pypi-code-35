import logging
from asyncio import PriorityQueue, get_event_loop, iscoroutinefunction
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class Bot(object):
    update_types = [
        ('message', 'message'),
        ('edited_message', 'message'),
        ('channel_post', 'message'),
        ('edited_channel_post', 'message'),
        ('inline_query', 'inline_query'),
        ('chosen_inline_result', 'chosen_inline_result'),
        ('callback_query', 'callback_query'),
        ('shipping_query', 'shipping_query'),
        ('pre_checkout_query', 'pre_checkout_query')
    ]
    discover_type_and_flavor = False

    def __init__(self, token, json_lib=None, max_handlers=1, loop=None):
        """
        The Class(TM).

        :param token: The Telegram-given token
        """

        self.token = token

        if json_lib is not None:
            self.json = json_lib
        else:
            import json
            self.json = json

        self.max_handlers = max_handlers

        if loop is None:
            self.loop = get_event_loop()
        else:
            self.loop = loop

        self.logger = logging.getLogger('ubot')
        self.triggers = []
        self.ignore_check_triggers = []
        self.update_queue = PriorityQueue(loop=loop)
        self.base_url = 'https://api.telegram.org:443/bot%s/' % token

    async def api_request(self, method, endpoint, data=None, headers=None):
        """
        Wraps the urllib3 request in a more user friendly way, making it async and premitting the base Telegram API url.

        :param method: The HTTP method name (GET, POST, PUT, DELETE, HEAD)
        :param endpoint: A Telegram API endpoint (e.g. sendMessage), omitting
            the first slash
        :param data: Binary data to send with the request
        :param headers: A dict of headers
        :return: The response from the server, in the form of a dict
        """

        url = '%s%s' % (self.base_url, endpoint)

        if data and 'content-length' not in [x.lower() for x in headers.keys()]:
            headers['Content-Length'] = len(data)

        req = Request(url=url, method=method, data=data, headers=headers)
        return urlopen(req)

    async def set_webhook_url(self, url):
        await self.api_request('GET', 'setWebhook?url=%s' % url)

    async def start(self):  # noqa: C901
        """
        Main loop

        >>> import asyncio
        >>> loop = asyncio.get_event_loop()
        >>> bot = Bot('token')
        >>> loop.run_until_complete(asyncio.wait([
        >>>     loop.create_task(bot.start())
        >>>     # other tasks
        >>> ]))
        >>> loop.run_forever()

        or (if you want to use a custom event loop

        >>> import asyncio
        >>> loop = asyncio.new_event_loop()
        >>> bot = Bot('token', loop=loop)
        >>> loop.run_until_complete(asyncio.wait([
        >>>     loop.create_task(bot.start())
        >>>     # other tasks
        >>> ]))
        >>> loop.run_forever()

        note: single instance, multiple threads unsupported (for now), use an instance of the bot for every thread
        """

        while True:
            _, update = await self.update_queue.get()

            # get type and flavor if needed or simply leave them to None
            if self.discover_type_and_flavor is True:
                for _type, flavor in self.update_types:
                    if _type in update:
                        update_type, update_flavor = _type, flavor
                        break
                else:
                    update_type, update_flavor = None, None
            else:
                update_type, update_flavor = None, None

            # check the update if the function is implemented and skip if it's not passed
            if hasattr(self, 'check_update'):
                check_update = self.check_update
                if iscoroutinefunction(check_update):
                    is_check_passed = await check_update(update, update_type, update_flavor)
                else:
                    is_check_passed = check_update(update, update_type, update_flavor)

                if is_check_passed is True:
                    checked_triggers = self.ignore_check_triggers + self.triggers
                else:
                    checked_triggers = self.triggers
            else:
                checked_triggers = self.triggers

            # loop through the triggers to find one that matches
            curr_handlers = 0

            for trigger in checked_triggers:
                if curr_handlers > self.max_handlers:
                    break

                match = trigger.match

                if iscoroutinefunction(match):
                    is_update_matched = await match(update, update_type, update_flavor)
                else:
                    is_update_matched = match(update, update_type, update_flavor)

                if is_update_matched is not True:
                    continue

                curr_handlers += 1

                # if a matching one is found call the corresponding handler
                handle = trigger.handle

                if iscoroutinefunction(handle):
                    endpoint = await handle(update, update_type, update_flavor)
                else:
                    endpoint = handle(update, update_type, update_flavor)

                if endpoint is None:
                    continue

                method, url, args, data, headers = endpoint

                _url = '%s?%s' % (url, urlencode(args))
                response = await self.api_request(method, _url, data, headers)

                # call the callback if existing
                callback = trigger.callback

                if callback is None:
                    continue

                if iscoroutinefunction(callback):
                    await callback(response)
                else:
                    callback(response)

    def push_update(self, update):
        """
        Pushes an update (already json decoded) into the queue.

        :param update: The update to be pushed in the queue
        """

        self.update_queue.put_nowait((update['update_id'], update))

    def trigger(self, requires_type_and_flavor=False, ignore_check=False):
        """
        Decorates a Trigger, inserting it into the bot check list

        :param requires_type_and_flavor: Forces the bot to discover the type and the flavor of an update and to call
            the trigger methods with those as arguments
        :param ignore_check: ignores a possible "check_update" function
        """

        def decorator(trigger):
            if ignore_check is True:
                self.ignore_check_triggers.append(trigger())
            else:
                self.triggers.append(trigger())

            if requires_type_and_flavor is True:
                self.discover_type_and_flavor = True

            return trigger

        return decorator
