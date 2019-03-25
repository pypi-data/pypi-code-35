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
command_list = {}
commands_links = {}
commands = []
library = 'dispyt'

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
CHANNEL_PINS_UPDATE_EVENT = None
GUILD_CREATE_EVENT = None
GUILD_UPDATE_EVENT = None
GUILD_DELETE_EVENT = None
USER_BAN_EVENT = None
USER_UNBAN_EVENT = None
GUILD_EMOJIS_UPDATE_EVENT = None
GUILD_INTEGRATIONS_UPDATE_EVENT = None
MEMBER_JOIN_EVENT = None
MEMBER_REMOVE_EVENT = None
MEMBER_UPDATE_EVENT = None

GLOBAL_BOT = None
BOT_MODERATORS = []
HANDLER_IS_USED = False

def parse_args(args):
    save = ''
    arglist = []
    instr = False
    for c in args:
        if c == '"':
            instr = not instr
        elif c == ' ' and instr == False:
            if save != '':
                arglist.append(save)
                save = ''
        else:
            save += c
    if save != '':
        arglist.append(save)
    return arglist

class GuildMember:
    def __init__(self, data, user):
        self.username = user['username']
        try:
            self.verified = user['verified']
            self.locale = user['locale']
            self.mfa_enabled = user['mfa_enabled']
        except:
            pass
        try:
            self.bot = user['bot']
        except:
            pass
        self.id = user['id']
        self.mention = f'<@{self.id}>'
        self.mention_nick = f'<@!{self.id}>'
        try:
            self.flags = user['flags']
        except:
            pass
        self.avatar_url = f'https://cdn.discordapp.com/avatars/{self.id}/{user["avatar"]}.png'
        self.discriminator = user['discriminator']
        self.fullname = f'{self.username}#{self.discriminator}'
        try:
            self.email = user['email']
        except:
            pass
        try:
            self.nick = data['nick']
        except:
            pass
        self.roles = data['roles']
        self.joined_at = data['joined_at']
        self.deaf = data['deaf']
        self.mute = data['mute']
        try:
            self.guild_id = data['guild_id']
        except:
            pass
    
    async def set_nick(self, nickname:str):
        payload = {'nick': nickname}
        async with GLOBAL_SESSION.patch(f'{base_url}/guilds/{self.guild_id}/members/{self.id}', data=json.dumps(payload), headers=APPLICATION_HEADERS) as r:
            if r.status != 204:
                raise BadResponse(f'GuildMember.set_nick bad response. Response: {await r.json()}')
    
    async def mute(self):
        payload = {'mute': True}
        async with GLOBAL_SESSION.patch(f'{base_url}/guilds/{self.guild_id}/members/{self.id}', data=json.dumps(payload), headers=APPLICATION_HEADERS) as r:
            if r.status != 204:
                raise BadResponse(f'GuildMember.mute bad response. Response: {await r.json()}')
    
    async def unmute(self):
        payload = {'mute': False}
        async with GLOBAL_SESSION.patch(f'{base_url}/guilds/{self.guild_id}/members/{self.id}', data=json.dumps(payload), headers=APPLICATION_HEADERS) as r:
            if r.status != 204:
                raise BadResponse(f'GuildMember.mute bad response. Response: {await r.json()}')
    
    async def deaf(self):
        payload = {'deaf': True}
        async with GLOBAL_SESSION.patch(f'{base_url}/guilds/{self.guild_id}/members/{self.id}', data=json.dumps(payload), headers=APPLICATION_HEADERS) as r:
            if r.status != 204:
                raise BadResponse(f'GuildMember.mute bad response. Response: {await r.json()}')
    
    async def undeaf(self):
        payload = {'deaf': True}
        async with GLOBAL_SESSION.patch(f'{base_url}/guilds/{self.guild_id}/members/{self.id}', data=json.dumps(payload), headers=APPLICATION_HEADERS) as r:
            if r.status != 204:
                raise BadResponse(f'GuildMember.mute bad response. Response: {await r.json()}')

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
    
    def channel_pins_update(self, event_func):
        globals().update(CHANNEL_PINS_UPDATE_EVENT=event_func)
    
    def guild_create(self, event_func):
        globals().update(GUILD_CREATE_EVENT=event_func)
    
    def guild_update(self, event_func):
        globals().update(GUILD_UPDATE_EVENT=event_func)
    
    def guild_delete(self, event_func):
        globals().update(GUILD_DELETE_EVENT=event_func)
    
    def ban(self, event_func):
        globals().update(USER_BAN_EVENT=event_func)
    
    def unban(self, event_func):
        globals().update(USER_UNBAN_EVENT=event_func)
    
    def guild_emojis_update(self, event_func):
        globals().update(GUILD_EMOJIS_UPDATE_EVENT=event_func)
    
    def integrations_update(self, event_func):
        globals().update(GUILD_INTEGRATIONS_UPDATE_EVENT=event_func)
    
    def member_join(self, event_func):
        globals().update(MEMBER_JOIN_EVENT=event_func)
    
    def member_remove(self, event_func):
        globals().update(MEMBER_REMOVE_EVENT=event_func)
    
    def member_update(self, event_func):
        globals().update(MEMBER_UPDATE_EVENT=event_func)
    
    def prefix(self, event_func):
        globals().update(PREFIX_EVENT=event_func)

event = Events()

class Handler:
    def moderators(self, moderator_list:list):
        globals().update(BOT_MODERATORS=moderator_list)
    
    def setCommand(self, command_func, name:str, links:list, only_mod:bool, description:str):
        if name == None:
            name = command_func.__name__
        globals().update(HANDLER_IS_USED=True)
        commands.append(name)
        command_list[name] = {}
        command_list[name]['call'] = command_func
        command_list[name]['args'] = list(command_func.__code__.co_varnames)
        command_list[name]['description'] = description
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

    def command(self, name:str=None, links:list=None, only_mod:bool=False, description:str=None):
        def decorator(command_func, name=name, links=links, only_mod=only_mod, description=description):
            self.setCommand(command_func, name, links, only_mod, description)
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
        await GLOBAL_SESSION.get(f'{base_url}/users/@me/guilds/{self.id}')

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
        self.channel = channel
        try:
            data['member']['guild_id'] = self.channel.guild_id
            self.author = GuildMember(data['member'], data['author'])
        except:
            self.author = User(data['author'])
        self.mention_roles = data['mention_roles']
        self.content = data['content']
        if GLOBAL_BOT.prefix != None:
            self.command = data['content'][len(GLOBAL_BOT.prefix):].strip().split(' ', 1)[0]
            self.args = parse_args(data['content'][len(GLOBAL_BOT.prefix):].split(' ', 1)[1])
        self.mentions = data['mentions']
        self.type = data['type']
    
    async def get_member(self):
        member = GuildMember(self.mentions[-1]['member'], self.mentions[-1])
        async with GLOBAL_SESSION.get(f'{base_url}/guilds/{self.channel.guild_id}/members/{member.id}') as r:
            _dict = await r.json()
            _dict['guild_id'] = self.channel.guild_id
            return GuildMember(_dict, _dict['user'])
    
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
    def __init__(self, prefix:str=None):
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
        self.prefix = prefix
        self.members = []
        self.call_events = {
            'MESSAGE_CREATE': {
                'call': self.__message_create,
                'event': None
            },
            'MESSAGE_UPDATE': {
                'call': self.__message_edit,
                'event': 'MESSAGE_EDIT_EVENT'
            },
            'MESSAGE_DELETE': {
                'call': self.__message_delete,
                'event': 'MESSAGE_DELETE_EVENT'
            },
            'MESSAGE_REACTION_ADD': {
                'call': self.__reaction_add,
                'event': 'REACTION_ADD_EVENT'
            },
            'MESSAGE_REACTION_REMOVE': {
                'call': self.__reaction_remove,
                'event': 'REACTION_REMOVE_EVENT'
            },
            'CHANNEL_CREATE': {
                'call': self.__new_channel,
                'event': 'NEW_CHANNEL_EVENT'
            },
            'CHANNEL_UPDATE': {
                'call': self.__channel_update,
                'event': 'CHANNEL_UPDATE_EVENT'
            },
            'CHANNEL_DELETE': {
                'call': self.__channel_delete,
                'event': 'CHANNEL_DELETE_EVENT'
            },
            'CHANNEL_PINS_UPDATE': {
                'call': self.__channel_pins_update,
                'event': 'CHANNEL_PINS_UPDATE_EVENT'
            },
            'GUILD_CREATE': {
                'call': self.__guild_create,
                'event': 'GUILD_CREATE_EVENT'
            },
            'GUILD_UPDATE': {
                'call': self.__guild_update,
                'event': 'GUILD_UPDATE_EVENT'
            },
            'GUILD_DELETE': {
                'call': self.__guild_delete,
                'event': 'GUILD_DELETE_EVENT'
            },
            'GUILD_BAN_ADD': {
                'call': self.__guild_ban_add,
                'event': 'USER_BAN_EVENT'
            },
            'GUILD_BAN_REMOVE': {
                'call': self.__guild_ban_remove,
                'event': 'USER_UNBAN_EVENT'
            },
            'GUILD_EMOJIS_UPDATE': {
                'call': self.__guild_emojis_update,
                'event': 'GUILD_EMOJIS_UPDATE_EVENT'
            },
            'GUILD_INTEGRATIONS_UPDATE': {
                'call': self.__guild_integrations_update,
                'event': 'GUILD_INTEGRATIONS_UPDATE_EVENT'
            },
            'GUILD_MEMBER_ADD': {
                'call': self.__guild_member_add,
                'event': 'MEMBER_JOIN_EVENT'
            },
            'GUILD_MEMBER_REMOVE': {
                'call': self.__guild_member_remove,
                'event': 'MEMBER_REMOVE_EVENT'
            },
            'GUILD_MEMBER_UPDATE': {
                'call': self.__guild_member_update,
                'event': 'GUILD_MEMBER_UPDATE'
            },
            'GUILD_MEMBERS_CHUNK': {
                'call': self.__guild_members_chunk,
                'event': None
            },
            'PRESENCE_UPDATE': {
                'call': None,
                'event': 'None'
            },
            'TYPING_START': {
                'call': None,
                'event': 'None'
            }
        }
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
    
    async def __guild_members_chunk(self, recv):
        for x in recv['d']['members']:
            x['guild_id'] = recv['d']['guild_id']
            self.members.append(GuildMember(x, x['user']))
    
    async def __guild_member_update(self, recv):
        await MEMBER_UPDATE_EVENT(UpdatedMember(recv['d'], User(recv['d']['user'])))
    
    async def __guild_member_remove(self, recv):
        await MEMBER_REMOVE_EVENT(User(recv['d']['user']), recv['d']['guild_id'])
    
    async def __guild_member_add(self, recv):
        await MEMBER_JOIN_EVENT(GuildMember(recv['d'], recv['d']['user']))
    
    async def __guild_integrations_update(self, recv):
        await GUILD_INTEGRATIONS_UPDATE_EVENT(recv['d']['guild_id'])
    
    async def __guild_emojis_update(self, recv):
        await GUILD_EMOJIS_UPDATE_EVENT([UEmoji(x, await self.get_user(recv['d']['user']['id'])) for x in recv['d']['emojis']])
    
    async def __guild_ban_remove(self, recv):
        await USER_BAN_EVENT(UnbannedUser(recv['d']['guild_id'], User(recv['d']['user'])))

    async def __guild_ban_add(self, recv):
        await USER_BAN_EVENT(BannedUser(recv['d']['guild_id'], User(recv['d']['user'])))

    async def __guild_delete(self, recv):
        await GUILD_DELETE_EVENT(UnavailableGuild(recv['d']))

    async def __guild_update(self, recv):
        await GUILD_UPDATE_EVENT(Guild(recv['d']))
    
    async def __guild_create(self, recv):
        await GUILD_CREATE_EVENT(Guild(recv['d']))
    
    async def __channel_pins_update(self, recv):
        await CHANNEL_PINS_UPDATE_EVENT(await self.get_channel(recv['d']['channel_id']))
    
    async def __channel_delete(self, recv):
        await CHANNEL_DELETE_EVENT(Channel(recv['d']))

    async def __channel_update(self, recv):
        await CHANNEL_UPDATE_EVENT(Channel(recv['d']))

    async def __new_channel(self, recv):
        await NEW_CHANNEL_EVENT(Channel(recv['d']))
    
    async def __reaction_add(self, recv):
        if recv['d']['emoji']['id'] == None:
            _emoji = Emoji(recv['d']['emoji']['name'], channel=await self.get_channel(recv['d']['channel_id']), guild_id=recv['d']['guild_id'])
        else:
            _emoji = Emoji(recv['d']['emoji']['name'], recv['d']['emoji']['id'], channel=await self.get_channel(recv['d']['channel_id']), guild_id=data['d']['guild_id'])
                            
        await REACTION_ADD_EVENT(_emoji, await self.get_user(recv['d']['user_id']))
    
    async def __reaction_remove(self, recv):
        if recv['d']['emoji']['id'] == None:
            _emoji = Emoji(recv['d']['emoji']['name'], channel=await self.get_channel(recv['d']['channel_id']), guild_id=recv['d']['guild_id'])
        else:
            _emoji = Emoji(recv['d']['emoji']['name'], recv['d']['emoji']['id'], channel=await self.get_channel(recv['d']['channel_id']), guild_id=data['d']['guild_id'])

        await REACTION_REMOVE_EVENT(_emoji, await self.get_user(recv['d']['user_id']))
    
    async def __message_delete(self, recv):
        await MESSAGE_DELETE_EVENT(DeletedMessage(recv['d']['id'], await self.get_channel(recv['d']['channel_id']), recv['d']['guild_id']))
    
    async def __message_edit(self, recv):
        await MESSAGE_EDIT_EVENT(Message(recv['d'], await self.get_channel(recv['d']['channel_id'])))
    
    async def __message_create(self, recv):
        if HANDLER_IS_USED and recv['d']['content'][:len(self.prefix)] == self.prefix:
            msg = Message(recv['d'], await self.get_channel(recv['d']['channel_id']))
            if msg.command in command_list or msg.command in commands_links:
                if msg.command in commands_links:
                    msg.command = commands_links[msg.command]
                if command_list[msg.command]['only_mod']:
                    if msg.author.id in BOT_MODERATORS:
                        msg.args = [x.replace('"', '') for x in msg.args]
                        request = ','.join([f'"{x}"' for x in msg.args])
                        if len(request) > 0:
                            exec(f'self.loop.create_task(command_list[msg.command]["call"](Response(msg),{request}))')
                        else:
                            self.loop.create_task(command_list[msg.command]["call"](Response(msg)))
                    else:
                        print('only mod')
                        # Later add & call no_moderator event
                        pass
                else:
                    msg.args = [x.replace('"', '') for x in msg.args]
                    request = ','.join([f'"{x}"' for x in msg.args])
                    if len(request) > 0:
                        exec(f'self.loop.create_task(command_list[msg.command]["call"](Response(msg),{request}))')
                    else:
                        self.loop.create_task(command_list[msg.command]["call"](Response(msg)))
            else:
                print('command not found')
                # Later add & call no_command event
                pass
        else:
            if MESSAGE_EVENT != None:
                await MESSAGE_EVENT(Message(recv['d'], await self.get_channel(recv['d']['channel_id'])))
            elif PREFIX_EVENT != None and recv['d']['content'][:len(self.prefix)] == self.prefix:
                await PREFIX_EVENT(Message(recv['d'], await self.get_channel(recv['d']['channel_id'])))
    
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
            self.websocket.max_size = 2 ** 20 * 4
            self.connected = True
            while True:
                if self.connected:
                    try:
                        recv = json.loads(await self.websocket.recv())
                    except Exception as e:
                        print(f'Something occured and connection is lost. Trying to resume...\nException: {e}')
                        self.connected = False
                        self.loop.create_task(self.__resume())
                    self.seq += 1
                    if self.ready:
                        try:
                            if self.call_events[recv['t']]['event'] == None or eval(self.call_events[recv['t']]['event']) != None:
                                await self.call_events[recv['t']]['call'](recv)
                        except Exception as e:
                            print(e)
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
                            for x in self.me.guilds:
                                await self.websocket.send(json.dumps({'op': 8, 'd': {'guild_id': x['id'], 'query': '', 'limit': 0}}))
                            if HANDLER_IS_USED:
                                commands.append('help')
                                command_list['help'] = {}
                                command_list['help']['call'] = self.__help_command
                                command_list['help']['args'] = ['response', 'args']
                                command_list['help']['only_mod'] = False
                                command_list['help']['description'] = 'Help command.'
                            self.ready = True
                            await READY_EVENT()
                        elif recv['t'] == 'RESUMED':
                            print('Resumed successfully.')
    
    async def __help_command(self, response, args):
        _desc = ''
        for x in command_list:
            if command_list[x]['description'] == None:
                _use_desc = 'No description.'
            else:
                _use_desc = command_list[x]['description']
            _desc += f'__{x}__ ⮞ **{_use_desc}**\n'
        embed = Embed(title=f'Help Command :: Prefix `{self.prefix}`', description=_desc)
        embed.autoauthor(response.author)
        embed.autofooter(response.author)
        await response.send(embed=embed)

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
                self.websocket.max_size = 2 ** 20 * 4
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
                raise BadArguments('guild_id and guild_name')
            else:
                try:
                    guild_id = [x['id'] for x in self.me.guilds if x['name'] == guild_name][0]
                except:
                    raise NotFound(f'Guild "{guild_name}"')
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

    def authorize(self, token:str):
        self.loop.run_until_complete(self.__authorization(token))
        globals().update(GLOBAL_BOT=self)
        self.loop.create_task(self.__gateway())
        self.loop.run_forever()
