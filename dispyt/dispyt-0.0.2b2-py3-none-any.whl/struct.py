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

from datetime import datetime
from time import time

class Response:
    def __init__(self, message):
        self.message = message
        self.author = message.author
        self.send = message.channel.send

class OptionalAuditEntry:
    def __init__(self, data):
        self.delete_member_days = data['delete_member_days']
        self.members_removed = data['members_removed']
        self.channel_id = data['channel_id']
        self.count = data['count']
        self.id = data['id']
        self.type = data['type']
        self.role_name = data['role_name']

class AuditLogChange:
    def __init__(self, data):
        self.new_value = data['new_value']
        self.old_value = data['old_value']
        self.key = data['key']

class AuditLogEntry:
    def __init__(self, data):
        self.target_id = data['target_id']
        self.changes = [AuditLogChange(x) for x in data['changes']]
        self.user_id = data['user_id']
        self.id = data['id']
        self.action_type = data['action_type']
        self.action = AuditLogEvents[self.action_type]
        self.options = [OptionalAuditEntry(x) for x in data['options']]
        self.reason = data['reason']

class AuditLog:
    def __init__(self, data):
        self.webhooks = data['webhooks']
        self.users = [User(x) for x in data['users']]
        self.entries = [AuditLogEntry(x) for x in data['audit_log_entries']]

class User:
    def __init__(self, data):
        self.username = data['username']
        try:
            self.verified = data['verified']
        except:
            pass
        try:
            self.locale = data['locale']
        except:
            pass
        try:
            self.mfa_enabled = data['mfa_enabled']
        except:
            pass
        try:
            self.bot = data['bot']
        except:
            pass
        self.id = data['id']
        self.mention = f'<@{self.id}>'
        self.nick = f'<@!{self.id}>'
        try:
            self.flags = data['flags']
        except:
            pass
        self.avatar_url = f'https://cdn.discordapp.com/avatars/{self.id}/{data["avatar"]}.png'
        self.discriminator = data['discriminator']
        self.fullname = f'{self.username}#{self.discriminator}'
        try:
            self.email = data['email']
        except:
            pass

class UpdatedMember:
    def __init__(self, data, user):
        self.guild_id = data['guild_id']
        self.roles = data['roles']
        self.user = user
        self.nick = data['nick']

class ClientStatus:
    def __init__(self, status:str, game, afk:bool=False):
        self.dict = {
            'game': game,
            'status': status,
            'since': int(time()),
            'afk': afk
        }

class Activity:
    def __init__(self, name:str, _type:int):
        self.dict = {'name': name, 'type': _type}

class DeletedMessage:
    def __init__(self, id:str, channel, guild_id):
        self.id = id
        self.channel = channel
        self.guild_id = guild_id

def EmbedFooter(text:str=None, icon_url:str=None, proxy_icon_url:str=None):
    return {
        'text': text,
        'icon_url': icon_url,
        'proxy_icon_url': proxy_icon_url
    }

def EmbedImage(url:str=None, proxy_url:str=None, height:int=None, width:int=None):
    return {
        'url': url,
        'prxy_url': proxy_url,
        'height': height,
        'width': width
    }

def EmbedVideo(url:str=None, height:int=None, width:int=None):
    return {
        'url': url,
        'height': height,
        'width': width
    }

def EmbedProvider(name:str=None, url:str=None):
    return {
        'name': name,
        'url': url
    }

def EmbedField(name:str=None, value:str=None, inline:bool=True):
    return {
        'name': name,
        'value': value,
        'inline': inline
    }

def EmbedAuthor(name:str=None, url:str=None, icon_url:str=None, proxy_icon_url:str=None):
    return {
        'name': name,
        'url': url,
        'icon_url': icon_url,
        'proxy_icon_url': proxy_icon_url
    }

class Embed:
    def __init__(self, title:str=None, description:str=None, color:int=None):
        self.title = title
        self.description = description
        self.timestamp = datetime.now().isoformat()
        self.color = color
        self._footer = None
        self._image = None
        self._thumbnail = None
        self._video = None
        self._provider = None
        self._author = None
        self._fields = []
    
    def footer(self, text:str=None, icon_url:str=None, proxy_icon_url:str=None):
        self._footer = EmbedFooter(text=text, icon_url=icon_url, proxy_icon_url=proxy_icon_url)
    
    def author(self, name:str=None, url:str=None, icon_url:str=None, proxy_icon_url:str=None):
        self._author = EmbedAuthor(name=name, url=url, icon_url=icon_url, proxy_icon_url=proxy_icon_url)
    
    def image(self, url:str=None, proxy_url:str=None, height:int=None, width:int=None):
        self._image = EmbedImage(url=url, proxy_url=proxy_url, height=height, width=width)
    
    def thumbnail(self, url:str=None, proxy_url:str=None, height:int=None, width:int=None):
        self._thumbnail = EmbedImage(url=url, proxy_url=proxy_url, height=height, width=width)
    
    def video(self, url:str=None, height:int=None, width:int=None):
        self._video = EmbedVideo(url=url, height=height, width=width)
    
    def provider(self, name:str=None, url:str=None):
        self._provider = EmbedProvider(name=name, url=url)
    
    def field(self, name:str=None, value:str=None, inline:bool=True):
        self._fields.append(EmbedField(name=name, value=value, inline=inline))
    
    def autofooter(self, author:User):
        self.footer(text=f'Requested by {author.fullname}', icon_url=author.avatar_url)
    
    def autoauthor(self, author:User):
        self.author(name=author.fullname, icon_url=author.avatar_url)
    
    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'timestamp': self.timestamp,
            'color': self.color,
            'footer': self._footer,
            'image': self._image,
            'thumbnail': self._thumbnail,
            'video': self._video,
            'provider': self._provider,
            'author': self._author,
            'fields': self._fields
        }

class Emoji:
    def __init__(self, name:str, custom_id:str=None, channel=None, guild_id=None):
        self.name = name
        self.id = custom_id
        if self.id != None:
            self.text = f'<:{self.name}:{self.id}>'
        else:
            self.text = self.name
        self.channel = channel
        self.guild_id = guild_id

class Role:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.color = data['color']
        self.hoist = data['hoist']
        self.position = data['position']
        self.permissions = data['permissions']
        self.managed = data['managed']
        self.mentionable = data['mentionable']

class UEmoji:
    def __init__(self, data, user):
        self.id = data['id']
        self.roles = data['roles']
        self.user = user
        self.require_colons = data['require_colons']
        self.managed = data['managed']
        self.animated = data['animated']

class UnavailableGuild:
    def __init__(self, id:str):
        self.id = id

class BannedUser:
    def __init__(self, guild_id:str, user):
        self.guild_id = guild_id
        self.user = user

class UnbannedUser:
    def __init__(self, guild_id:str, user):
        self.guild_id = guild_id
        self.user = user

AuditLogEvents = {
    1: 'GUILD_UPDATE',
    10: 'CHANNEL_CREATE',
    11: 'CHANNEL_UPDATE',
    12: 'CHANNEL_DELETE',
    13: 'CHANNEL_OVERWRITE_CREATE',
    14: 'CHANNEL_OVERWRITE_UPDATE',
    15: 'CHANNEL_OVERWRITE_DELETE',
    20: 'MEMBER_KICK',
    21: 'MEMBER_PRUNE',
    22: 'MEMBER_BAN_ADD',
    23: 'MEMBER_BAN_REMOVE',
    24: 'MEMBER_UPDATE',
    25: 'MEMBER_ROLE_UPDATE',
    30: 'ROLE_CREATE',
    31: 'ROLE_UPDATE',
    32: 'ROLE_DELETE',
    40: 'INVITE_CREATE',
    41: 'INVITE_UPDATE',
    42: 'INVITE_DELETE',
    50: 'WEBHOOK_CREATE',
    51: 'WEBHOOK_UPDATE',
    52: 'WEBHOOK_DELETE',
    60: 'EMOJI_CREATE',
    61: 'EMOJI_UPDATE',
    62: 'EMOJI_DELETE',
    72: 'MESSAGE_DELETE'
}