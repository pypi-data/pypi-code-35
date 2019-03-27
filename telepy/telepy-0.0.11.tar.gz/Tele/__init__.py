# Tele ver 0.0.11
import json
import requests
from threading import Thread
from time import sleep
from urllib3 import disable_warnings

disable_warnings()


def getUpdates(timeout=10):
    try:
        return requests.get(api + 'getUpdates?timeout=%s' % timeout).json()['result']
    except NameError:
        print('You need to insert token to "account" function')
        exit(1)
    except KeyError:
        print('Unauthorized token')
        exit(1)
    except requests.exceptions.ConnectionError or requests.exceptions.ReadTimeout:
        sleep(2)
        return


def sendMessage(chat_id, text, parse_mode='Markdown',
                disable_web_page_preview=None, disable_notification=None,
                reply_to_message_id=None, reply_markup=None):
    params = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': parse_mode,
        'disable_web_page_preview': disable_web_page_preview,
        'disable_notification': disable_notification,
        'reply_to_message_id': reply_to_message_id,
        'reply_markup': reply_markup,
    }
    if _is_list(chat_id):
        return _chat_ids(sendMessage, **params)
    return requests.post(api + 'sendMessage', params=_j_ord(params))


def forwardMessage(chat_id=None, from_chat_id=None, message_id=None, disable_notification=None, update=None):
    params = {
        'chat_id': chat_id,
        'from_chat_id': from_chat_id,
        'message_id': message_id,
        'disable_notification': disable_notification,
        'update': update,
    }
    if _is_list(chat_id):
        return _chat_ids(forwardMessage, **params)
    if update:
        params['from_chat_id'], params['message_id'] = _replay(update)
    return requests.post(api + 'forwardMessage', params=_j_ord(params))


def sendPhoto(chat_id=None, file=None, caption=None, thumb=None, reply_to_message_id=None, parse_mode='Markdown',
              disable_web_page_preview=None, disable_notification=None, reply_markup=None):
    params = {
        'chat_id': chat_id,
        'file': file,
        'caption': caption,
        'thumb': thumb,
        'reply_to_message_id': reply_to_message_id,
        'parse_mode': parse_mode,
        'disable_web_page_preview': disable_web_page_preview,
        'disable_notification': disable_notification,
        'reply_markup': reply_markup,
    }
    if _is_list(chat_id):
        return _chat_ids(sendPhoto, **params)
    j, files = _file('photo', params)
    return requests.post(api + 'sendPhoto', params=j, files=files)


def sendAudio(chat_id=None, file=None, caption=None, parse_mode=None, duration=None,
              performer=None, title=None, thumb=None):
    params = {
        'chat_id': chat_id,
        'file': file,
        'caption': caption,
        'parse_mode': parse_mode,
        'duration': duration,
        'performer': performer,
        'title': title,
        'thumb': thumb,
    }
    if _is_list(chat_id):
        return _chat_ids(sendAudio, **params)
    j, files = _file('audio', params)
    return requests.post(api + 'sendAudio', params=j, files=files)


def sendDocument(chat_id, file, caption=None, thumb=None, reply_to_message_id=None, parse_mode='Markdown',
                 disable_web_page_preview=None, disable_notification=None, reply_markup=None):
    params = {
        'chat_id': chat_id,
        'file': file,
        'caption': caption,
        'thumb': thumb,
        'reply_to_message_id': reply_to_message_id,
        'parse_mode': parse_mode,
        'disable_web_page_preview': disable_web_page_preview,
        'disable_notification': disable_notification,
        'reply_markup': reply_markup,
    }
    if _is_list(chat_id):
        return _chat_ids(sendDocument, **params)
    j, files = _file('document', params)
    return requests.post(api + 'sendDocument', params=j, files=files)


def sendVideo(chat_id, file, duration=None, width=None, height=None, thumb=None,
              caption=None, parse_mode=None, supports_streaming=None, disable_notification=None,
              reply_to_message_id=None, reply_markup=None):
    params = {
        'chat_id': chat_id,
        'file': file,
        'duration': duration,
        'width': width,
        'height': height,
        'thumb': thumb,
        'caption': caption,
        'parse_mode': parse_mode,
        'supports_streaming': supports_streaming,
        'disable_notification': disable_notification,
        'reply_to_message_id': reply_to_message_id,
        'reply_markup': reply_markup,
    }
    if _is_list(chat_id):
        return _chat_ids(sendVideo, **params)
    j, files = _file('video', params)
    return requests.post(api + 'sendVideo', params=j, files=files)


def sendAnimation(chat_id, file, duration=None, width=None, height=None, thumb=None, caption=None,
                  parse_mode=None, disable_notification=None, reply_to_message_id=None, reply_markup=None):
    params = {
        'chat_id': chat_id,
        'file': file,
        'duration': duration,
        'width': width,
        'height': height,
        'thumb': thumb,
        'caption': caption,
        'parse_mode': parse_mode,
        'disable_notification': disable_notification,
        'reply_to_message_id': reply_to_message_id,
        'reply_markup': reply_markup,
    }
    if _is_list(chat_id):
        return _chat_ids(sendAnimation, **params)
    j, files = _file('animation', params)
    return requests.post(api + 'sendAnimation', params=j, files=files)


def sendVoice(chat_id, file, caption=None, parse_mode=None, duration=None, disable_notification=None,
              reply_to_message_id=None, reply_markup=None):
    params = {
        'chat_id': chat_id,
        'file': file,
        'caption': caption,
        'parse_mode': parse_mode,
        'duration': duration,
        'disable_notification': disable_notification,
        'reply_to_message_id': reply_to_message_id,
        'reply_markup': reply_markup,
    }
    if _is_list(chat_id):
        return _chat_ids(sendVoice, **params)
    j, files = _file('voice', params)
    return requests.post(api + 'sendVoice', params=j, files=files)


def sendVideoNote(chat_id, file, duration=None, length=None, thumb=None,
                  disable_notification=None, reply_to_message_id=None, reply_markup=None):
    params = {
        'chat_id': chat_id,
        'file': file,
        'duration': duration,
        'length': length,
        'thumb': thumb,
        'disable_notification': disable_notification,
        'reply_to_message_id': reply_to_message_id,
        'reply_markup': reply_markup,
    }
    if _is_list(chat_id):
        return _chat_ids(sendVideoNote, **params)
    j, files = _file('video_note', params)
    return requests.post(api + 'sendVideoNote', params=j, files=files)


def sendMediaGroup(chat_id, media, disable_notification=None, reply_to_message_id=None):
    params = {
        'chat_id': chat_id,
        'media': media,
        'disable_notification': disable_notification,
        'reply_to_message_id': reply_to_message_id,
    }
    if _is_list(chat_id):
        return _chat_ids(sendMediaGroup, **params)
    return requests.post(api + 'sendMediaGroup', json=_j_ord(params))


def sendLocation(chat_id, latitude, longitude, live_period=None, disable_notification=None,
                 reply_to_message_id=None, reply_markup=None):
    params = {
        'chat_id': chat_id,
        'latitude': latitude,
        'longitude': longitude,
        'live_period': live_period,
        'disable_notification': disable_notification,
        'reply_to_message_id': reply_to_message_id,
        'reply_markup': reply_markup,
    }
    if _is_list(chat_id):
        return _chat_ids(sendLocation, **params)
    return requests.post(api + 'sendLocation', params=_j_ord(params))


def editMessageLiveLocation(chat_id=None, message_id=None, inline_message_id=None,
                            latitude=None, longitude=None, reply_markup=None, update=None):
    params = {
        'chat_id': chat_id,
        'message_id': message_id,
        'inline_message_id': inline_message_id,
        'latitude': latitude,
        'longitude': longitude,
        'reply_markup': reply_markup,
        'update': update,
    }
    if update:
        params['chat_id'], params['message_id'] = _replay(update)
    return requests.post(api + 'editMessageLiveLocation', params=_j_ord(params))


def stopMessageLiveLocation(chat_id=None, message_id=None, inline_message_id=None,
                            reply_markup=None, update=None):
    params = {
        'chat_id': chat_id,
        'message_id': message_id,
        'inline_message_id': inline_message_id,
        'reply_markup': reply_markup,
        'update': update,
    }
    if update:
        params['chat_id'], params['message_id'] = _replay(update)
    return requests.post(api + 'stopMessageLiveLocation', params=_j_ord(params))


def sendVenue(chat_id, latitude, longitude, title, address, foursquare_id=None, foursquare_type=None,
              disable_notification=None, reply_to_message_id=None, reply_markup=None):
    params = {
        'chat_id': chat_id,
        'latitude': latitude,
        'longitude': longitude,
        'title': title,
        'address': address,
        'foursquare_id': foursquare_id,
        'foursquare_type': foursquare_type,
        'disable_notification': disable_notification,
        'reply_to_message_id': reply_to_message_id,
        'reply_markup': reply_markup,
    }
    if _is_list(chat_id):
        return _chat_ids(sendVenue, **params)
    return requests.post(api + 'sendVenue', params=_j_ord(params))


def sendContact(chat_id, phone_number, first_name, last_name=None, vcard=None, disable_notification=None,
                reply_to_message_id=None, reply_markup=None):
    params = {
        'chat_id': chat_id,
        'phone_number': phone_number,
        'first_name': first_name,
        'last_name': last_name,
        'vcard': vcard,
        'disable_notification': disable_notification,
        'reply_to_message_id': reply_to_message_id,
        'reply_markup': reply_markup,
    }

    if _is_list(chat_id):
        return _chat_ids(sendContact, **params)
    return requests.post(api + 'sendContact', params=_j_ord(params))


def sendChatAction(chat_id, action):
    params = {
        'chat_id': chat_id,
        'action': action,
    }
    if _is_list(chat_id):
        return _chat_ids(sendChatAction, **params)
    return requests.post(api + 'sendChatAction', params=_j_ord(params))


def getUserProfilePhotos(user_id, offset=None, limit=None):
    params = {
        'user_id': user_id,
        'offset': offset,
        'limit': limit,
    }
    return requests.post(api + 'getUserProfilePhotos', params=_j_ord(params))


def getFile(file_id):
    return requests.get(api + 'getFile?file_id=' + file_id).json()


def kickChatMember(chat_id, user_id, until_date=None):
    params = {
        'chat_id': chat_id,
        'user_id': user_id,
        'until_date': until_date,
    }
    return requests.post(api + 'kickChatMember', params=_j_ord(params))


def unbanChatMember(chat_id, user_id):
    params = {
        'chat_id': chat_id,
        'user_id': user_id,
    }

    return requests.post(api + 'unbanChatMember', params=_j_ord(params))


def restrictChatMember(chat_id, user_id, until_date=None, can_send_messages=None,
                       can_send_media_messages=None, can_send_other_messages=None, can_add_web_page_previews=None):
    params = {
        'chat_id': chat_id,
        'user_id': user_id,
        'until_date': until_date,
        'can_send_messages': can_send_messages,
        'can_send_media_messages': can_send_media_messages,
        'can_send_other_messages': can_send_other_messages,
        'can_add_web_page_previews': can_add_web_page_previews,
    }

    return requests.post(api + 'restrictChatMember', params=_j_ord(params))


def promoteChatMember(chat_id, user_id, can_change_info=None, can_post_messages=None, can_edit_messages=None,
                      can_delete_messages=None, can_invite_users=None, can_restrict_members=None, can_pin_messages=None,
                      can_promote_members=None):
    params = {
        'chat_id': chat_id,
        'user_id': user_id,
        'can_change_info': can_change_info,
        'can_post_messages': can_post_messages,
        'can_edit_messages': can_edit_messages,
        'can_delete_messages': can_delete_messages,
        'can_invite_users': can_invite_users,
        'can_restrict_members': can_restrict_members,
        'can_pin_messages': can_pin_messages,
        'can_promote_members': can_promote_members,
    }
    return requests.post(api + 'promoteChatMember', params=_j_ord(params))


def exportChatInviteLink(chat_id):
    params = {
        'chat_id': chat_id,
    }
    return requests.post(api + 'exportChatInviteLink', params=params)


def setChatPhoto(chat_id, photo):
    params = {
        'chat_id': chat_id,
        'photo': photo,
    }

    j, files = _file('photo', params)
    return requests.post(api + 'sendVideoNote', params=j, files=files)


def deleteChatPhoto(chat_id):
    params = {
        'chat_id': chat_id,
    }
    return requests.post(api + 'deleteChatPhoto', params=params)


def setChatTitle(chat_id, title):
    params = {
        'chat_id': chat_id,
        'title': title,
    }
    return requests.post(api + 'setChatTitle', params=params)


def setChatDescription(chat_id, description):
    params = {
        'chat_id': chat_id,
        'description': description,
    }

    return requests.post(api + 'setChatDescription', params=params)


def pinChatMessage(chat_id, message_id, disable_notification=None):
    params = {
        'chat_id': chat_id,
        'message_id': message_id,
        'disable_notification': disable_notification,
    }
    return requests.post(api + 'pinChatMessage', params=_j_ord(params))


def unpinChatMessage(chat_id):
    params = {
        'chat_id': chat_id,
    }
    return requests.post(api + 'unpinChatMessage', params=params)


def leaveChat(chat_id):
    params = {
        'chat_id': chat_id,
    }
    return requests.post(api + 'leaveChat', params=params)


def getChat(chat_id):
    params = {
        'chat_id': chat_id,
    }
    return requests.post(api + 'getChat', params=params)


def getChatAdministrators(chat_id):
    params = {
        'chat_id': chat_id,
    }
    return requests.post(api + 'getChatAdministrators', params=params)


def getChatMembersCount(chat_id):
    params = {
        'chat_id': chat_id,
    }
    return requests.post(api + 'ChatMembersCount', params=params)


def getChatMember(chat_id, user_id):
    params = {
        'chat_id': chat_id,
        'user_id': user_id,
    }
    return requests.post(api + 'getChatMember', params=params)


def setChatStickerSet(chat_id, sticker_set_name):
    params = {
        'chat_id': chat_id,
        'sticker_set_name': sticker_set_name,
    }
    return requests.post(api + 'setChatStickerSet', params=params)


def deleteChatStickerSet(chat_id):
    params = {
        'chat_id': chat_id,
    }
    return requests.post(api + 'deleteChatStickerSet', params=params)


def answerCallbackQuery(callback_query_id, text=None, show_alert=None, url=None, cache_time=None):
    params = {
        'callback_query_id': callback_query_id,
        'text': text,
        'show_alert': show_alert,
        'url': url,
        'cache_time': cache_time,
    }
    return requests.post(api + 'answerCallbackQuery', params=_j_ord(params))


def editMessageText(chat_id=None, message_id=None, inline_message_id=None, text=None,
                    parse_mode=None, disable_web_page_preview=None, reply_markup=None, update=None):
    params = {
        'chat_id': chat_id,
        'message_id': message_id,
        'inline_message_id': inline_message_id,
        'text': text,
        'parse_mode': parse_mode,
        'disable_web_page_preview': disable_web_page_preview,
        'reply_markup': reply_markup,
        'update': update,
    }
    if update:
        params['chat_id'], params['message_id'] = _replay(update)
    return requests.post(api + 'editMessageText', params=_j_ord(params))


def editMessageCaption(chat_id=None, message_id=None, inline_message_id=None,
                       caption=None, parse_mode=None, reply_markup=None, update=None):
    params = {
        'chat_id': chat_id,
        'message_id': message_id,
        'inline_message_id': inline_message_id,
        'caption': caption,
        'parse_mode': parse_mode,
        'reply_markup': reply_markup,
        'update': update,
    }
    if update:
        params['chat_id'], params['message_id'] = _replay(update)
    return requests.post(api + 'editMessageCaption', params=_j_ord(params))


####

def editMessageMedia(chat_id=None, message_id=None, inline_message_id=None,
                     media=None, reply_markup=None, update=None):
    params = {
        'chat_id': chat_id,
        'message_id': message_id,
        'inline_message_id': inline_message_id,
        'media': media,
        'reply_markup': reply_markup,
        'update': update,
    }
    if update:
        params['chat_id'], params['message_id'] = _replay(update)
    params['media'] = {"type": "document", "media": media}
    return requests.post(api + 'editMessageMedia', params=_j_ord(params))


def editMessageReplyMarkup(chat_id=None, message_id=None,
                           inline_message_id=None, reply_markup=None, update=None):
    params = {
        'chat_id': chat_id,
        'message_id': message_id,
        'inline_message_id': inline_message_id,
        'reply_markup': reply_markup,
        'update': update,
    }
    if update:
        params['chat_id'], params['message_id'] = _replay(update)
    return requests.post(api + 'editMessageReplyMarkup', params=_j_ord(params))


def deleteMessage(chat_id=None, message_id=None, update=None):
    if update:
        chat_id, message_id = _replay(update)
    params = {'chat_id': chat_id, 'message_id': message_id}
    return requests.get(api + 'deleteMessage', params=params)


def sendSticker(chat_id, file, disable_notification, reply_to_message_id=None, reply_markup=None):
    params = {
        'chat_id': chat_id,
        'file': file,
        'disable_notification': disable_notification,
        'reply_to_message_id': reply_to_message_id,
        'reply_markup': reply_markup,
    }

    j, files = _file('sticker', params)
    return requests.post(api + 'sendSticker', params=j, files=files)


def getStickerSet(name):
    params = {
        'name': name,
    }
    return requests.get(api + 'getStickerSet', params=params)


def uploadStickerFile(user_id, file):
    params = {
        'user_id': user_id,
        'file': file,
    }
    j, files = _file('png_sticker', params)
    return requests.post(api + 'uploadStickerFile', params=j, files=files)


def createNewStickerSet(user_id, name, title, file, emojis, contains_masks=None, mask_position=None):
    params = {
        'user_id': user_id,
        'name': name,
        'title': title,
        'file': file,
        'emojis': emojis,
        'contains_masks': contains_masks,
        'mask_position': mask_position,
    }
    j, files = _file('png_sticker', params)
    return requests.post(api + 'createNewStickerSet', params=j, files=files)


def addStickerToSet(user_id, name, file, emojis, mask_position=None):
    params = {
        'user_id': user_id,
        'name': name,
        'file': file,
        'emojis': emojis,
        'mask_position': mask_position,
    }
    j, files = _file('png_sticker', params)
    return requests.post(api + 'addStickerToSet', params=j, files=files)


def setStickerPositionInSet(sticker, position):
    params = {
        'sticker': sticker,
        'position': position,
    }
    return requests.get(api + 'setStickerPositionInSet', params=params)


def deleteStickerFromSet(sticker):
    params = {
        'sticker': sticker,
    }
    return requests.get(api + 'deleteStickerFromSet', params=params)


def answerInlineQuery(update, results, cache_time='300', is_personal=None,
                      next_offset=None, switch_pm_text=None, switch_pm_parameter=None):
    params = {
        'inline_query_id': update.inline_query.id,
        'results': results,
        'cache_time': cache_time,
        'is_personal': is_personal,
        'next_offset': next_offset,
        'switch_pm_text': switch_pm_text,
        'switch_pm_parameter': switch_pm_parameter,
    }
    return requests.post(api + 'answerInlineQuery', json=_j_ord(params))


def InlineQueryResultArticle(id, title=None, input_message_content=None,
                             reply_markup=None, url=None, hide_url=None, description=None,
                             thumb_url=None, thumb_width=None, thumb_height=None):
    params = {
        'id': id,
        'title': title,
        'input_message_content': input_message_content,
        'reply_markup': reply_markup,
        'url': url,
        'hide_url': hide_url,
        'description': description,
        'thumb_url': thumb_url,
        'thumb_width': thumb_width,
        'thumb_height': thumb_height,
    }
    j = _j_ord(params)
    j['type'] = 'article'
    return j


def InlineQueryResultPhoto(id, photo_url=None, thumb_url=None, photo_width=None,
                           photo_height=None, title=None, description=None, caption=None,
                           parse_mode='Markdown', reply_markup=None, input_message_content=None):
    params = {
        'id': id,
        'photo_url': photo_url,
        'thumb_url': thumb_url,
        'photo_width': photo_width,
        'photo_height': photo_height,
        'title': title,
        'description': description,
        'caption': caption,
        'parse_mode': parse_mode,
        'reply_markup': reply_markup,
        'input_message_content': input_message_content,
    }
    j = _j_ord(params)
    j['type'] = 'photo'
    return j


def InlineQueryResultGif(id, gif_url, gif_width=None, gif_height=None, thumb_url=None, title=None,
                         caption=None, parse_mode=None, reply_markup=None, input_message_content=None):
    params = {
        'id': id,
        'gif_url': gif_url,
        'gif_width': gif_width,
        'gif_height': gif_height,
        'thumb_url': thumb_url,
        'title': title,
        'caption': caption,
        'parse_mode': parse_mode,
        'reply_markup': reply_markup,
        'input_message_content': input_message_content,
    }
    j = _j_ord(params)
    j['type'] = 'gif'
    return j


def InlineQueryResultMpeg4Gif(id, mpeg4_url, mpeg4_width=None, mpeg4_height=None, mpeg4_duration=None, thumb_url=None,
                              title=None, caption=None, parse_mode=None, reply_markup=None, input_message_content=None):
    params = {
        'id': id,
        'mpeg4_url': mpeg4_url,
        'mpeg4_width': mpeg4_width,
        'mpeg4_height': mpeg4_height,
        'mpeg4_duration': mpeg4_duration,
        'thumb_url': thumb_url,
        'title': title,
        'caption': caption,
        'parse_mode': parse_mode,
        'reply_markup': reply_markup,
        'input_message_content': input_message_content,
    }
    j = _j_ord(params)
    j['type'] = 'mpeg4_gif'
    return j


def InlineQueryResultVideo(id, video_url, mime_type, thumb_url, title, caption=None, parse_mode=None,
                           video_width=None, video_height=None, video_duration=None, description=None,
                           reply_markup=None, input_message_content=None):
    params = {
        'id': id,
        'video_url': video_url,
        'mime_type': mime_type,
        'thumb_url': thumb_url,
        'title': title,
        'caption': caption,
        'parse_mode': parse_mode,
        'video_width': video_width,
        'video_height': video_height,
        'video_duration': video_duration,
        'description': description,
        'reply_markup': reply_markup,
        'input_message_content': input_message_content,
    }
    j = _j_ord(params)
    j['type'] = 'video'
    return j


def InlineQueryResultAudio(id, audio_url, title, caption, parse_mode=None, performer=None, audio_duration=None,
                           reply_markup=None, input_message_content=None):
    params = {
        'id': id,
        'audio_url': audio_url,
        'title': title,
        'caption': caption,
        'parse_mode': parse_mode,
        'performer': performer,
        'audio_duration': audio_duration,
        'reply_markup': reply_markup,
        'input_message_content': input_message_content,
    }
    j = _j_ord(params)
    j['type'] = 'audio'
    return j


def InlineQueryResultVoice(id, voice_url, title, caption=None, parse_mode=None, voice_duration=None,
                           reply_markup=None, input_message_content=None):
    params = {
        'id': id,
        'voice_url': voice_url,
        'title': title,
        'caption': caption,
        'parse_mode': parse_mode,
        'voice_duration': voice_duration,
        'reply_markup': reply_markup,
        'input_message_content': input_message_content,
    }
    j = _j_ord(params)
    j['type'] = 'voice'
    return j


def InlineQueryResultDocument(id, title=None, caption=None, parse_mode=None,
                              document_url=None, mime_type=None, description=None,
                              reply_markup=None, input_message_content=None,
                              thumb_url=None, thumb_width=None, thumb_height=None):
    params = {
        'id': id,
        'title': title,
        'caption': caption,
        'parse_mode': parse_mode,
        'document_url': document_url,
        'mime_type': mime_type,
        'description': description,
        'reply_markup': reply_markup,
        'input_message_content': input_message_content,
        'thumb_url': thumb_url,
        'thumb_width': thumb_width,
        'thumb_height': thumb_height,
    }

    j = _j_ord(params)
    j['type'] = 'document'
    return j


def InlineQueryResultLocation(id, latitude, longitude, title, live_period=None, reply_markup=None,
                              input_message_content=None, thumb_url=None, thumb_width=None, thumb_height=None):
    params = {
        'id': id,
        'latitude': latitude,
        'longitude': longitude,
        'title': title,
        'live_period': live_period,
        'reply_markup': reply_markup,
        'input_message_content': input_message_content,
        'thumb_url': thumb_url,
        'thumb_width': thumb_width,
        'thumb_height': thumb_height,
    }
    j = _j_ord(params)
    j['type'] = 'location'
    return j


def InlineQueryResultVenue(id, latitude, longitude, title, address, foursquare_id=None, reply_markup=None,
                           input_message_content=None, thumb_url=None, thumb_width=None, thumb_height=None):
    params = {
        'id': id,
        'latitude': latitude,
        'longitude': longitude,
        'title': title,
        'address': address,
        'foursquare_id': foursquare_id,
        'reply_markup': reply_markup,
        'input_message_content': input_message_content,
        'thumb_url': thumb_url,
        'thumb_width': thumb_width,
        'thumb_height': thumb_height,
    }

    j = _j_ord(params)
    j['type'] = 'venue'
    return j


def InlineQueryResultContact(id, phone_number, first_name, last_name=None, vcard=None, reply_markup=None,
                             input_message_content=None, thumb_url=None, thumb_width=None, thumb_height=None):
    params = {
        'id': id,
        'phone_number': phone_number,
        'first_name': first_name,
        'last_name': last_name,
        'vcard': vcard,
        'reply_markup': reply_markup,
        'input_message_content': input_message_content,
        'thumb_url': thumb_url,
        'thumb_width': thumb_width,
        'thumb_height': thumb_height,
    }
    j = _j_ord(params)
    j['type'] = 'contact'
    return j


def InlineQueryResultGame(id, game_short_name, reply_markup):
    params = {
        'id': id,
        'game_short_name': game_short_name,
        'reply_markup': reply_markup,
    }
    j = _j_ord(params)
    j['type'] = 'game'
    return j


def InlineQueryResultCachedPhoto(id, photo_file_id, title=None, description=None, caption=None,
                                 parse_mode=None, reply_markup=None, input_message_content=None):
    params = {
        'id': id,
        'photo_file_id': photo_file_id,
        'title': title,
        'description': description,
        'caption': caption,
        'parse_mode': parse_mode,
        'reply_markup': reply_markup,
        'input_message_content': input_message_content,
    }
    j = _j_ord(params)
    j['type'] = 'photo'
    return j


def InlineQueryResultCachedGif(id, gif_file_id, title=None, caption=None, parse_mode=None,
                               reply_markup=None, input_message_content=None):
    params = {
        'id': id,
        'gif_file_id': gif_file_id,
        'title': title,
        'caption': caption,
        'parse_mode': parse_mode,
        'reply_markup': reply_markup,
        'input_message_content': input_message_content,
    }
    j = _j_ord(params)
    j['type'] = 'gif'
    return j


def InlineQueryResultCachedMpeg4Gif(id, mpeg4_file_id, title=None, caption=None, parse_mode=None,
                                    reply_markup=None, input_message_content=None):
    params = {
        'id': id,
        'mpeg4_file_id': mpeg4_file_id,
        'title': title,
        'caption': caption,
        'parse_mode': parse_mode,
        'reply_markup': reply_markup,
        'input_message_content': input_message_content,
    }
    j = _j_ord(params)
    j['type'] = 'mpeg4_gif'
    return j


def InlineQueryResultCachedSticker(id, sticker_file_id=None, reply_markup=None, input_message_content=None):
    params = {
        'id': id,
        'sticker_file_id': sticker_file_id,
        'reply_markup': reply_markup,
        'input_message_content': input_message_content,
    }
    j = _j_ord(params)
    j['type'] = 'sticker'
    return j


def InlineQueryResultCachedDocument(id, title, document_file_id, description=None, caption=None,
                                    parse_mode=None, reply_markup=None, input_message_content=None):
    params = {
        'id': id,
        'title': title,
        'document_file_id': document_file_id,
        'description': description,
        'caption': caption,
        'parse_mode': parse_mode,
        'reply_markup': reply_markup,
        'input_message_content': input_message_content,
    }
    j = _j_ord(params)
    j['type'] = 'document'
    return j


def InlineQueryResultCachedVideo(id, video_file_id, title, description=None, caption=None, parse_mode=None,
                                 reply_markup=None, input_message_content=None):
    params = {
        'id': id,
        'video_file_id': video_file_id,
        'title': title,
        'description': description,
        'caption': caption,
        'parse_mode': parse_mode,
        'reply_markup': reply_markup,
        'input_message_content': input_message_content,
    }
    j = _j_ord(params)
    j['type'] = 'video'
    return j


def InlineQueryResultCachedVoice(id, voice_file_id, title, caption=None,
                                 parse_mode=None, reply_markup=None, input_message_content=None):
    params = {
        'id': id,
        'voice_file_id': voice_file_id,
        'title': title,
        'caption': caption,
        'parse_mode': parse_mode,
        'reply_markup': reply_markup,
        'input_message_content': input_message_content,
    }
    j = _j_ord(params)
    j['type'] = 'voice'
    return j


def InlineQueryResultCachedAudio(id, audio_file_id, caption, parse_mode=None,
                                 reply_markup=None, input_message_content=None):
    params = {
        'id': id,
        'audio_file_id': audio_file_id,
        'caption': caption,
        'parse_mode': parse_mode,
        'reply_markup': reply_markup,
        'input_message_content': input_message_content,
    }
    j = _j_ord(params)
    j['type'] = 'audio'
    return j


def InputTextMessageContent(message_text=None, parse_mode=None):
    params = {
        'message_text': message_text,
        'parse_mode': parse_mode,
    }
    return _j_ord(params)


def InputLocationMessageContent(latitude, longitude, live_period=None):
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'live_period': live_period,
    }
    return _j_ord(params)


def InputVenueMessageContent(latitude, longitude, title, address, foursquare_id=None, foursquare_type=None):
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'title': title,
        'address': address,
        'foursquare_id': foursquare_id,
        'foursquare_type': foursquare_type,
    }
    return _j_ord(params)


def InputContactMessageContent(phone_number, first_name, last_name=None, vcard=None):
    params = {
        'phone_number': phone_number,
        'first_name': first_name,
        'last_name': last_name,
        'vcard': vcard,
    }
    return _j_ord(params)


def ChosenInlineResult(result_id, from_user, location=None, inline_message_id=None, query=None):
    params = {
        'result_id': result_id,
        'from_user': from_user,
        'location': location,
        'inline_message_id': inline_message_id,
        'query': query,
    }
    return _j_ord(params)


def InputMediaPhoto(media, caption=None, parse_mode=None):
    params = {
        'media': media,
        'caption': caption,
        'parse_mode': parse_mode,
    }

    j = _j_ord(params)
    j['type'] = 'photo'
    return j


def InputMediaVideo(media, thumb=None, caption=None, parse_mode=None,
                    width=None, height=None, duration=None, supports_streaming=None):
    params = {
        'media': media,
        'thumb': thumb,
        'caption': caption,
        'parse_mode': parse_mode,
        'width': width,
        'height': height,
        'duration': duration,
        'supports_streaming': supports_streaming,
    }
    j = _j_ord(params)
    j['type'] = 'video'
    return j


def InputMediaAnimation(media, thumb=None, caption=None, parse_mode=None,
                        width=None, height=None, duration=None):
    params = {
        'media': media,
        'thumb': thumb,
        'caption': caption,
        'parse_mode': parse_mode,
        'width': width,
        'height': height,
        'duration': duration,
    }
    j = _j_ord(params)
    j['type'] = 'animation'
    return j


def InputMediaAudio(media, thumb=None, caption=None, parse_mode=None,
                    duration=None, performer=None, title=None):
    params = {
        'media': media,
        'thumb': thumb,
        'caption': caption,
        'parse_mode': parse_mode,
        'duration': duration,
        'performer': performer,
        'title': title,
    }
    j = _j_ord(params)
    j['type'] = 'audio'
    return j


def InputMediaDocument(media, thumb=None, caption=None, parse_mode=None):
    params = {
        'media': media,
        'thumb': thumb,
        'parse_mode': parse_mode,
    }
    j = _j_ord(params)
    j['type'] = 'document'
    return j


def Keyboard(k=None, resize_keyboard=True, one_time_keyboard=None, num_line=None, remove=False):
    if remove:
        return '{"remove_keyboard": true}'
    if num_line:
        k = _num_ln(k, num_line)
    key = []
    for line in k:
        key.append([{'text': button} for button in line])
    key = {'keyboard': key, 'resize_keyboard': resize_keyboard}
    if one_time_keyboard:
        key['one_time_keyboard'] = one_time_keyboard

    return json.dumps(key, ensure_ascii=False)


def InlineKeyboard(k=None, num_line=2, obj='callback_data'):
    if num_line:
        k = _num_ln(k, num_line)
    key = []
    for line in k:
        for b in line:
            if len(b) < 2:
                b['type'] = obj
        key.append([{'text': tuple(b.keys())[0],
                     tuple(b.values())[1]: tuple(b.values())[0]} for b in line])
    return json.dumps({'inline_keyboard': key}, ensure_ascii=False)


"""The following functions do not exist in the methods or object of Telegram api.
These functions are optimized for use"""


def _num_ln(kbd, n):
    """Arranging buttons"""
    if type(kbd[0]) is list:
        kbd = kbd[0]
    lst = []
    k = len(kbd)
    n_l = k // n
    cor = 0
    for d in range(n_l):
        lst1 = []
        for e in range(cor, n + cor):
            lst1.append(kbd[e])
        lst.append(lst1)
        cor += n
    lst.append(kbd[k - (k % n): k])
    return lst


def message_reply(update, text=None, file=None, photo=None, parse_mode='Markdown',
                  disable_web_page_preview=None, reply_markup=None):
    chat_id, reply_to_message_id = _replay(update)
    if file:
        if photo:
            return sendPhoto(chat_id, reply_to_message_id=reply_to_message_id,
                             file=photo, caption=text,
                             reply_markup=reply_markup)
        else:
            return sendDocument(chat_id, reply_to_message_id=reply_to_message_id,
                                file=file, caption=text)
    params = {
        'chat_id': chat_id,
        'reply_to_message_id': reply_to_message_id,
        'text': text,
        'file': file,
        'photo': photo,
        'parse_mode': parse_mode,
        'disable_web_page_preview': disable_web_page_preview,
        'reply_markup': reply_markup,
    }
    return requests.post(api + 'sendMessage', json=_j_ord(params))


def down_document(file_id=None, name='', dest='', update=None):
    try:
        if update:
            name = update['document']['file_name']
            file_id = update['document']['file_id']
        file_path = getFile(file_id)['result']['file_path']
        file = requests.get('{}file/{}/{}'.format(api[:25], api[25:], file_path))
        with open(dest + '/' + name, 'wb') as new_file:
            new_file.write(file.content)
        return True
    except Exception as e:
        return e


def _is_list(x):
    return True if type(x) is list or type(x) is tuple else False


def _chat_ids(func, **loc):
    global _response
    _response = []
    for chat_id in loc['chat_id']:
        loc['chat_id'] = chat_id
        _response += func(**loc)
    return _response


def _file(func, loc):
    loc[func] = loc.pop('file')
    j = _j_ord(loc)
    try:
        files = {func: open(loc[func], 'rb')}
        del j[func]
    except FileNotFoundError:
        files = None
    if 'thumb' in loc:
        if loc['thumb']:
            try:
                tmb = open(loc['thumb'], 'rb')
                files['thumb'] = tmb
            except FileNotFoundError:
                pass
            return j, files
    return j, files


def _replay(update):
    if 'message' in update:
        chat_id, message_id = update.message.chat.id, update.message.message_id
    elif 'chat' in update:
        chat_id, message_id = update.chat.id, update.message_id

    elif 'update_id' in update:
        chat_id, message_id = update.edited_message['from'].id, update.edited_message.message_id
    else:
        chat_id, message_id = update['from'].id, update.message.message_id
    return chat_id, message_id


def _offset(update_id=False):
    """cleaning the getUpdates"""
    try:
        if update_id:
            params = {'offset': update_id + 1}
        else:
            params = {'offset': requests.get(api + 'getUpdates').json()['result'][-1]['update_id'] + 1}
        return requests.get(api + 'getUpdates', params=params)
    except:
        pass


def _j_ord(loc):
    """create dict (json), contain args names and args values:
        {'chat_id': chat_id}
    etc.. """
    j = {}
    for element in loc:
        if loc[element] is not None:
            j[element] = loc[element]
    return j


class _Dict(dict):
    """convert the json to dict and object.
    so:
        update['result']['document']['file_id']
        update.result.document.file_id
    should work properly.."""

    def __init__(self, dict_):
        super(_Dict, self).__init__(dict_)
        for key in self:
            item = self[key]
            if isinstance(item, list):
                for idx, it in enumerate(item):
                    if isinstance(it, dict):
                        item[idx] = _Dict(it)
            elif isinstance(item, dict):
                self[key] = _Dict(item)

    def __getattr__(self, key):
        return self[key]


funcs_list = {}


def bot(filters=None, type=None, not_on=None):
    def decorator(func):
        funcs_list[func] = {'filter': filters, 'type': type, 'not_on': not_on}

    return decorator


def _update_for(gt_up):
    if gt_up:
        for up in gt_up:
            _offset(up['update_id'])
            if 'message' in up:
                return up['message']
            elif 'callback_query' in up:
                return up['callback_query']
            else:
                return up
    else:
        return


def _check_filters(update, fil):
    if fil in update.keys():
        return True
    else:
        for a in update.values():
            if type(a) is list:
                for b in a:
                    if fil in b.values():
                        return True


def _filter_for(f, up):
    if type(f) is list or type(f) is tuple:
        for fil in f:
            if _check_filters(up, fil):
                return True
    else:
        if _check_filters(up, f):
            return True


def _filtering(up):
    for func in funcs_list:
        f = funcs_list[func]
        if f['type']:
            if 'message' in up:
                if f['type'] != up['message']['chat']['type']:
                    continue
            elif f['type'] != up['chat']['type']:
                continue

        if f['not_on']:
            if _filter_for(f['not_on'], up):
                continue

        if f['filter']:
            if _filter_for(f['filter'], up):
                func(_Dict(up))
        else:
            func(_Dict(up))


def bot_run(offset_=None, multi=None, timeout=10):
    if offset_:
        _offset()

    if multi:
        while True:
            update = _update_for(getUpdates(timeout))
            if update:
                Thread(target=_filtering, args=(update,)).start()

    else:
        while True:
            update = _update_for(getUpdates(timeout))
            if update:
                _filtering(update)


def account(token):
    if not token:
        return 'no token'
    global api
    api = 'https://api.telegram.org/bot%s/' % token
    return api
