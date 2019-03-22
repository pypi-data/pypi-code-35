"""
MIT License

Copyright (c) 2019 truedl

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import asyncio, aiohttp, websockets, json, platform, time
from .exceptions import *
from .struct import *

base_url = 'https://discordapp.com/api/v6'
library = 'dispyt'
command_list = {}
commands_links = {}

READY_EVENT = None
MESSAGE_EVENT = None
MESSAGE_EDIT_EVENT = None
MESSAGE_DELETE_EVENT = None
REACTION_ADD_EVENT = None
REACTION_REMOVE_EVENT = None
PREFIX_EVENT = None
NEW_CHANNEL_EVENT = None
CHANNEL_UPDATE_EVENT = None
CHANNEL_DELETE_EVENT = None

GLOBAL_BOT = None
BOT_MODERATORS = []
HANDLER_IS_USED = False

class Events:
    def ready(self, event_func):
        globals().update(READY_EVENT=event_func)

    def message(self, event_func):
        globals().update(MESSAGE_EVENT=event_func)
    
    def message_edit(self, event_func):
        globals().update(MESSAGE_EDIT_EVENT=event_func)
    
    def message_delete(self, event_func):
        globals().update(MESSAGE_DELETE_EVENT=event_func)
    
    def reaction_add(self, event_func):
        globals().update(REACTION_ADD_EVENT=event_func)
    
    def reaction_remove(self, event_func):
        globals().update(REACTION_REMOVE_EVENT=event_func)
    
    def new_channel(self, event_func):
        globals().update(NEW_CHANNEL_EVENT=event_func)
    
    def channel_update(self, event_func):
        globals().update(CHANNEL_UPDATE_EVENT=event_func)
    
    def channel_delete(self, event_func):
        globals().update(CHANNEL_DELETE_EVENT=event_func)
    
    def prefix(self, event_func):
        globals().update(PREFIX_EVENT=event_func)

event = Events()

class Handler:
    def moderators(self, moderator_list:list):
        globals().update(BOT_MODERATORS=moderator_list)
    
    def setCommand(self, command_func, name:str, links:list, only_mod:bool):
        if name == None:
            name = command_func.__name__
        globals().update(HANDLER_IS_USED=True)
        command_list[name] = {}
        command_list[name]['call'] = command_func
        command_list[name]['args'] = list(command_func.__code__.co_varnames)
        if only_mod:
            if len(BOT_MODERATORS) > 0:
                command_list[name]['only_mod'] = True
            else:
                raise NoModerators('Can\'t set only_mod because BOT_MODERATORS list is empty.')
        else:
            command_list[name]['only_mod'] = False
        if links != None:
            for x in links:
                commands_links[x] = name

    def command(self, name:str=None, links:list=None, only_mod:bool=False):
        def decorator(command_func, name=name, links=links, only_mod=only_mod):
            self.setCommand(command_func, name, links, only_mod)
        return decorator

handler = Handler()

class Guild:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.icon_url = f'https://cdn.discordapp.com/icons/{self.id}/{data["icon"]}.png'
        self.splash = data['splash']
        self.owner_id = data['owner_id']
        self.region = data['region']
        self.afk_channel_id = data['afk_channel_id']
        self.afk_timeout = data['afk_timeout']
        self.embed_enabled = data['embed_enabled']
        self.embed_channel_id = data['embed_channel_id']
        self.verification_level = data['verification_level']
        self.default_message_notifications = data['default_message_notifications']
        self.explicit_content_filter = data['explicit_content_filter']
        self.roles = data['roles']
        self.emojis = data['emojis']
        self.features = data['features']
        self.mfa_level = data['mfa_level']
        self.application_id = data['application_id']
        self.widget_enabled = data['widget_enabled']
        self.widget_channel_id = data['widget_channel_id']
        self.system_channel_id = data['system_channel_id']
        self.max_presences = data['max_presences']
        self.max_member = data['max_members']
        self.vanity_url_code = data['vanity_url_code']
        self.description = data['description']
        self.banner = f'banners/{self.id}/{data["banner"]}.png'
        self.channels = []
    
    async def audit_log(self, limit:int=50):
        async with GLOBAL_SESSION.get(f'{base_url}/guilds/{self.id}/audit-logs?limit={limit}') as r:
            try:
                return AuditLog(await r.json())
            except:
                raise BadResponse(f'Guild.audit_log bad response. Response: {await r.json()}')
    
    async def leave(self):
        async with GLOBAL_SESSION.get(f'{base_url}/users/@me/guilds/{self.id}') as r:
            return

class Message:
    def __init__(self, data, channel):
        self.nonce = data['nonce']
        self.attachments = data['attachments']
        self.tts = data['tts']
        self.embeds = data['embeds']
        self.timestamp = data['timestamp']
        self.mention_everyone = data['mention_everyone']
        self.id = data['id']
        self.pinned = data['pinned']
        self.edited_timestamp = data['edited_timestamp']
        self.author = User(data['author'])
        self.mention_roles = data['mention_roles']
        self.content = data['content']
        if GLOBAL_BOT.prefix != None:
            self.command = data['content'][len(GLOBAL_BOT.prefix):].strip().split(' ')[0]
            self.args = data['content'][len(GLOBAL_BOT.prefix):].strip().split(' ')[1:]
        self.channel = channel
        self.mentions = data['mentions']
        self.type = data['type']
    
    async def react(self, action:str='add', emoji:str=None, id:str=None):
        if id != None:
            _emoji = f'{emoji}:{id}'
        else:
            _emoji = emoji
        if action == 'add':
            await GLOBAL_SESSION.put(f'{base_url}/channels/{self.channel.id}/messages/{self.id}/reactions/{_emoji}/@me')
        elif action == 'remove':
            await GLOBAL_SESSION.delete(f'{base_url}/channels/{self.channel.id}/messages/{self.id}/reactions/{_emoji}/@me')

    async def edit(self, content:str):
        payload = {'content': content}
        async with GLOBAL_SESSION.patch(f'{base_url}/channels/{self.channel.id}/messages/{self.id}', data=json.dumps(payload), headers=APPLICATION_HEADERS) as r:
            return await r.json()

    async def delete(self):
        await GLOBAL_SESSION.delete(f'{base_url}/channels/{self.channel.id}/messages/{self.id}')

class Channel:
    def __init__(self, data):
        self.id = data['id']
        self.mention = f'<#{self.id}>'
        self.type = data['type']
        self.position = data['position']
        self.name = data['name']
        self.nsfw = data['nsfw']
        self.parent_id = data['parent_id']
        self.guild_id = data['guild_id']
    
    async def send(self, content:str=None, embed:Embed=None):
        if embed != None:
            payload = {'content': content, 'embed': embed.to_dict()}
        else:
            payload = {'content': content}
        async with GLOBAL_SESSION.post(f'{base_url}/channels/{self.id}/messages', data=json.dumps(payload), headers=APPLICATION_HEADERS) as r:
            try:
                return Message(await r.json(), self)
            except:
                raise BadResponse(f'Channel.send bad response. Response: {await r.json()}')
    
    async def trigger(self):
        await GLOBAL_SESSION.post(f'{base_url}/channels/{self.id}/typing')
    
    async def history(self, limit:int=50):
        async with GLOBAL_SESSION.get(f'{base_url}/channels/{self.id}/messages?limit={limit}') as r:
            try:
                return [Message(x, None) for x in await r.json()]
            except:
                raise BadResponse(f'Channel.history bad response. Response: {await r.json()}')

class Bot:
    def __init__(self):
        self.__identify_info = {
            'token': None,
            'properties': {
                '$os': platform.platform(),
                '$browser': library,
                '$device': library
            },
            'compress': False,
            'large_threshold': 250,
            'shard': [0, None],
            'presence': ClientStatus('online', None).dict
        }
        self.prefix = None
        self.ready = False
        self.loop = asyncio.get_event_loop()
    
    async def __authorization(self, token:str):
        self.headers = {'Authorization': f'Bot {token}'}
        self.app_headers = {'Authorization': f'Bot {token}', 'Content-Type': 'application/json'}
        self.token = token
        self.__identify_info['token'] = token
        globals().update(GLOBAL_SESSION=aiohttp.ClientSession(headers=self.headers))
        globals().update(GLOBAL_HEADERS=self.headers)
        globals().update(APPLICATION_HEADERS=self.app_headers)
    
    async def __gateway(self):
        async with GLOBAL_SESSION.get(f'{base_url}/gateway/bot') as r:
            gateway = await r.json()
            try:
                self.shards = gateway['shards']
            except:
                raise BadToken(self.token)
                await GLOBAL_SESSION.close()
                self.loop.close()
                return
            self.__identify_info['shard'][1] = self.shards
            self.gateway = gateway['url']
            self.first = True
            self.seq = 0
            self.websocket = await websockets.connect(f'{self.gateway}/?v=6&encoding=json')
            self.websocket.max_size = 2 ** 20 * 2
            self.connected = True
            while True:
                if self.connected:
                    try:
                        recv = json.loads(await self.websocket.recv())
                    except Exception as e:
                        print(f'Something occured and connection is lost. Trying to resume...\nException: {e}')
                        self.connected = False
                        await self.__resume()
                    self.seq += 1
                    if self.ready:
                        if recv['t'] == 'MESSAGE_CREATE':
                            if HANDLER_IS_USED and recv['d']['content'][:len(self.prefix)] == self.prefix:
                                msg = Message(recv['d'], await self.get_channel(recv['d']['channel_id']))
                                if msg.command in command_list or msg.command in commands_links:
                                    if msg.command in commands_links:
                                        msg.command = commands_links[msg.command]
                                    if command_list[msg.command]['only_mod']:
                                        if msg.author.id in BOT_MODERATORS:
                                            if 'author' in command_list[msg.command]['args']:
                                                await command_list[msg.command]['call'](Response(msg), msg.args, author=msg.author)
                                            else:
                                                await command_list[msg.command]['call'](Response(msg), msg.args)
                                        else:
                                            # Later add & call no_moderator event
                                            pass
                                    else:
                                        if 'author' in command_list[msg.command]['args']:
                                            await command_list[msg.command]['call'](Response(msg), msg.args, author=msg.author)
                                        else:
                                            await command_list[msg.command]['call'](Response(msg), msg.args)
                            else:
                                if MESSAGE_EVENT != None:
                                    await MESSAGE_EVENT(Message(recv['d'], await self.get_channel(recv['d']['channel_id'])))
                                elif PREFIX_EVENT != None and recv['d']['content'][:len(self.prefix)] == self.prefix:
                                    await PREFIX_EVENT(Message(recv['d'], await self.get_channel(recv['d']['channel_id'])))
                        elif recv['t'] == 'MESSAGE_UPDATE' and MESSAGE_EDIT_EVENT != None:
                            await MESSAGE_EDIT_EVENT(Message(recv['d'], await self.get_channel(recv['d']['channel_id'])))
                        elif recv['t'] == 'MESSAGE_DELETE' and MESSAGE_DELETE_EVENT != None:
                            await MESSAGE_EDIT_EVENT(DeletedMessage(recv['d']['id'], await self.get_channel(recv['d']['channel_id']), recv['d']['guild_id']))
                        elif recv['t'] == 'MESSAGE_REACTION_ADD' and REACTION_ADD_EVENT != None:
                            if recv['d']['emoji']['id'] == None:
                                _emoji = Emoji(recv['d']['emoji']['name'], channel=await self.get_channel(recv['d']['channel_id']), guild_id=recv['d']['guild_id'])
                            else:
                                _emoji = Emoji(recv['d']['emoji']['name'], recv['d']['emoji']['id'], channel=await self.get_channel(recv['d']['channel_id']), guild_id=data['d']['guild_id'])
                            
                            await REACTION_ADD_EVENT(_emoji, await self.get_user(recv['d']['user_id']))
                        elif recv['t'] == 'MESSAGE_REACTION_REMOVE' and REACTION_REMOVE_EVENT != None:
                            if recv['d']['emoji']['id'] == None:
                                _emoji = Emoji(recv['d']['emoji']['name'], channel=await self.get_channel(recv['d']['channel_id']), guild_id=recv['d']['guild_id'])
                            else:
                                _emoji = Emoji(recv['d']['emoji']['name'], recv['d']['emoji']['id'], channel=await self.get_channel(recv['d']['channel_id']), guild_id=data['d']['guild_id'])
                            
                            await REACTION_REMOVE_EVENT(_emoji, await self.get_user(recv['d']['user_id']))
                        elif recv['t'] == 'CHANNEL_CREATE' and NEW_CHANNEL_EVENT != None:
                            await NEW_CHANNEL_EVENT(Channel(recv['d']))
                        elif recv['t'] == 'CHANNEL_UPDATE' and CHANNEL_UPDATE_EVENT != None:
                            await CHANNEL_UPDATE_EVENT(Channel(recv['d']))
                        elif recv['t'] == 'CHANNEL_DELETE' and CHANNEL_DELETE_EVENT != None:
                            await CHANNEL_DELETE_EVENT(Channel(recv['d']))
                    else:
                        if recv['op'] == 10:
                            self.heartbeat_interval = recv['d']['heartbeat_interval']/1000
                            self.loop.create_task(self.__heartbeat())
                            if self.first:
                                self.loop.create_task(self.__identify())
                                self.first = False
                        elif recv['op'] == 9:
                            print('Invalid Session.')
                        elif recv['t'] == 'READY':
                            self.me = User(recv['d']['user'])
                            self.session_id = recv['d']['session_id']
                            async with GLOBAL_SESSION.get(f'{base_url}/users/@me/guilds') as r:
                                self.me.guilds = await r.json()
                                self.me.guild_count = len(self.me.guilds)
                            self.ready = True
                            await READY_EVENT()
                        elif recv['t'] == 'RESUMED':
                            print('Resumed successfully.')

    async def __update_status(self):
        await self.websocket.send(json.dumps({'op': 3, 'd': self.__identify_info['presence']}))

    async def __identify(self):
        await self.websocket.send(json.dumps({'op': 2, 'd': self.__identify_info}))

    async def __heartbeat(self):
        while True:
            if self.connected:
                await self.__just_heartbeat()
                await asyncio.sleep(self.heartbeat_interval)
            else:
                break
    
    async def __resume(self):
        while True:
            try:
                self.websocket = await websockets.connect(f'{self.gateway}/?v=6&encoding=json')
                self.websocket.max_size = 2 ** 20 * 2
                await self.websocket.send(json.dumps({'op': 6, 'd': {'token': self.token, 'session_id': self.session_id, 'seq': self.seq}}))
                self.connected = True
                self.loop.create_task(self.__heartbeat())
                break
            except Exception as e:
                print(f'Resume failed. Trying again in 5 seconds. [{e}]')
                await asyncio.sleep(5)
    
    async def __just_heartbeat(self):
        await self.websocket.send(json.dumps({'op': 1, 'd': self.seq}))

    async def get_guild(self, guild_id:str=None, guild_name:str=None):
        if not guild_id:
            if not guild_name:
                raise ValueError('guild_id, guild_name')
            else:
                try:
                    guild_id = [x['id'] for x in self.me.guilds if x['name'] == guild_name][0]
                except:
                    raise f'Guild "{guild_name}" is undefined.'
        async with GLOBAL_SESSION.get(f'{base_url}/guilds/{guild_id}') as r:
            try:
                guild = Guild(await r.json())
            except:
                raise BadResponse(f'Bot.get_guild bad response. Response: {await r.json()}')
        async with GLOBAL_SESSION.get(f'{base_url}/guilds/{guild_id}/channels') as r:
            channels = await r.json()
            for channel in channels:
                guild.channels.append(Channel(channel))
        
        return guild
    
    async def get_channel(self, channel_id:str):
        async with GLOBAL_SESSION.get(f'{base_url}/channels/{channel_id}') as r:
            try:
                return Channel(await r.json())
            except:
                raise BadResponse(f'Bot.get_channel bad response. Response: {await r.json()}')
    
    async def get_user(self, user_id:str):
        async with GLOBAL_SESSION.get(f'{base_url}/users/{user_id}') as r:
            try:
                return User(await r.json())
            except:
                raise BadResponse(f'Bot.get_user bad response. Response: {await r.json()}')

    async def update_status(self, status:str):
        self.__identify_info['presence'] = ClientStatus(status, self.__identify_info['presence']['game']).dict
        await self.__update_status()
    
    async def update_activity(self, activity:Activity):
        self.__identify_info['presence'] = ClientStatus(self.__identify_info['presence']['status'], activity.dict).dict
        await self.__update_status()

    def authorize(self, token:str, prefix:str=None):
        self.loop.run_until_complete(self.__authorization(token))
        self.prefix = prefix
        globals().update(GLOBAL_BOT=self)
        self.loop.create_task(self.__gateway())
        self.loop.run_forever()
