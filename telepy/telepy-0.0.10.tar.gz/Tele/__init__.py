# Tele ver 0.0.9
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
    if _is_list(chat_id):
        return _chat_ids(sendMessage, **locals())
    return requests.post(api + 'sendMessage', params=_j_ord(locals()))


def forwardMessage(chat_id=None, from_chat_id=None, message_id=None, disable_notification=None, update=None):
    if _is_list(chat_id):
        return _chat_ids(forwardMessage, **locals())
    if update:
        from_chat_id, message_id = _replay(update)
    return requests.post(api + 'forwardMessage', params=_j_ord(locals()))


def sendPhoto(chat_id=None, file=None, caption=None, thumb=None, reply_to_message_id=None, parse_mode='Markdown',
              disable_web_page_preview=None, disable_notification=None, reply_markup=None):
    if _is_list(chat_id):
        return _chat_ids(sendPhoto, **locals())
    j, files = _file('photo', locals())
    return requests.post(api + 'sendPhoto', params=j, files=files)


def sendAudio(chat_id=None, file=None, caption=None, parse_mode=None, duration=None,
              performer=None, title=None, thumb=None):
    if _is_list(chat_id):
        return _chat_ids(sendAudio, **locals())
    j, files = _file('audio', locals())
    return requests.post(api + 'sendAudio', params=j, files=files)


def sendDocument(chat_id, file, caption=None, thumb=None, reply_to_message_id=None, parse_mode='Markdown',
                 disable_web_page_preview=None, disable_notification=None, reply_markup=None):
    if _is_list(chat_id):
        return _chat_ids(sendDocument, **locals())
    j, files = _file('document', locals())
    return requests.post(api + 'sendDocument', params=j, files=files)


def sendVideo(chat_id, file, duration=None, width=None, height=None, thumb=None,
              caption=None, parse_mode=None, supports_streaming=None, disable_notification=None,
              reply_to_message_id=None, reply_markup=None):
    if _is_list(chat_id):
        return _chat_ids(sendVideo, **locals())
    j, files = _file('video', locals())
    return requests.post(api + 'sendVideo', params=j, files=files)


def sendAnimation(chat_id, file, duration=None, width=None, height=None, thumb=None, caption=None,
                  parse_mode=None, disable_notification=None, reply_to_message_id=None, reply_markup=None):
    if _is_list(chat_id):
        return _chat_ids(sendAnimation, **locals())
    j, files = _file('animation', locals())
    return requests.post(api + 'sendAnimation', params=j, files=files)


def sendVoice(chat_id, file, caption=None, parse_mode=None, duration=None, disable_notification=None,
              reply_to_message_id=None, reply_markup=None):
    if _is_list(chat_id):
        return _chat_ids(sendVoice, **locals())
    j, files = _file('voice', locals())
    return requests.post(api + 'sendVoice', params=j, files=files)


def sendVideoNote(chat_id, file, duration=None, length=None, thumb=None,
                  disable_notification=None, reply_to_message_id=None, reply_markup=None):
    if _is_list(chat_id):
        return _chat_ids(sendVideoNote, **locals())
    j, files = _file('video_note', locals())
    return requests.post(api + 'sendVideoNote', params=j, files=files)


def sendMediaGroup(chat_id, media, disable_notification=None, reply_to_message_id=None):
    if _is_list(chat_id):
        return _chat_ids(sendMediaGroup, **locals())
    return requests.post(api + 'sendMediaGroup', json=_j_ord(locals()))


def sendLocation(chat_id, latitude, longitude, live_period=None, disable_notification=None,
                 reply_to_message_id=None, reply_markup=None):
    if _is_list(chat_id):
        return _chat_ids(sendLocation, **locals())
    return requests.post(api + 'sendLocation', params=_j_ord(locals()))


def editMessageLiveLocation(chat_id=None, message_id=None, inline_message_id=None,
                            latitude=None, longitude=None, reply_markup=None, update=None):
    if update:
        chat_id, message_id = _replay(update)
    return requests.post(api + 'editMessageLiveLocation', params=_j_ord(locals()))


def stopMessageLiveLocation(chat_id=None, message_id=None, inline_message_id=None,
                            reply_markup=None, update=None):
    if update:
        chat_id, message_id = _replay(update)
    return requests.post(api + 'stopMessageLiveLocation', params=_j_ord(locals()))


def sendVenue(chat_id, latitude, longitude, title, address, foursquare_id=None, foursquare_type=None,
              disable_notification=None, reply_to_message_id=None, reply_markup=None):
    if _is_list(chat_id):
        return _chat_ids(sendVenue, **locals())
    return requests.post(api + 'sendVenue', params=_j_ord(locals()))


def sendContact(chat_id, phone_number, first_name, last_name=None, vcard=None, disable_notification=None,
                reply_to_message_id=None, reply_markup=None):
    if _is_list(chat_id):
        return _chat_ids(sendContact, **locals())
    return requests.post(api + 'sendContact', params=_j_ord(locals()))


def sendChatAction(chat_id, action):
    if _is_list(chat_id):
        return _chat_ids(sendChatAction, **locals())
    return requests.post(api + 'sendChatAction', params=_j_ord(locals()))


def getUserProfilePhotos(user_id, offset=None, limit=None):
    return requests.post(api + 'getUserProfilePhotos', params=_j_ord(locals()))


def getFile(file_id):
    return requests.get(api + 'getFile?file_id=' + file_id).json()


def kickChatMember(chat_id, user_id, until_date=None):
    return requests.post(api + 'kickChatMember', params=_j_ord(locals()))


def unbanChatMember(chat_id, user_id):
    return requests.post(api + 'unbanChatMember', params=_j_ord(locals()))


def restrictChatMember(chat_id, user_id, until_date=None, can_send_messages=None,
                       can_send_media_messages=None, can_send_other_messages=None, can_add_web_page_previews=None):
    return requests.post(api + 'restrictChatMember', params=_j_ord(locals()))


def promoteChatMember(chat_id, user_id, can_change_info=None, can_post_messages=None, can_edit_messages=None,
                      can_delete_messages=None, can_invite_users=None, can_restrict_members=None, can_pin_messages=None,
                      can_promote_members=None):
    return requests.post(api + 'promoteChatMember', params=_j_ord(locals()))


def exportChatInviteLink(chat_id):
    return requests.post(api + 'exportChatInviteLink', params=_j_ord(locals()))


def setChatPhoto(chat_id, photo):
    j, files = _file('photo', locals())
    return requests.post(api + 'sendVideoNote', params=j, files=files)


def deleteChatPhoto(chat_id):
    return requests.post(api + 'deleteChatPhoto', params=_j_ord(locals()))


def setChatTitle(chat_id, title):
    return requests.post(api + 'setChatTitle', params=_j_ord(locals()))


def setChatDescription(chat_id, description):
    return requests.post(api + 'setChatDescription', params=_j_ord(locals()))


def pinChatMessage(chat_id, message_id, disable_notification=None):
    return requests.post(api + 'pinChatMessage', params=_j_ord(locals()))


def unpinChatMessage(chat_id):
    return requests.post(api + 'unpinChatMessage', params=_j_ord(locals()))


def leaveChat(chat_id):
    return requests.post(api + 'leaveChat', params=_j_ord(locals()))


def getChat(chat_id):
    return requests.post(api + 'getChat', params=_j_ord(locals()))


def getChatAdministrators(chat_id):
    return requests.post(api + 'getChatAdministrators', params=_j_ord(locals()))


def getChatMembersCount(chat_id):
    return requests.post(api + 'ChatMembersCount', params=_j_ord(locals()))


def getChatMember(chat_id, user_id):
    return requests.post(api + 'getChatMember', params=_j_ord(locals()))


def setChatStickerSet(chat_id, sticker_set_name):
    return requests.post(api + 'setChatStickerSet', params=_j_ord(locals()))


def deleteChatStickerSet(chat_id):
    return requests.post(api + 'deleteChatStickerSet', params=_j_ord(locals()))


def answerCallbackQuery(callback_query_id, text=None, show_alert=None, url=None, cache_time=None):
    return requests.post(api + 'answerCallbackQuery', params=_j_ord(locals()))


def editMessageText(chat_id=None, message_id=None, inline_message_id=None, text=None,
                    parse_mode=None, disable_web_page_preview=None, reply_markup=None, update=None):
    if update:
        chat_id, message_id = _replay(update)
    return requests.post(api + 'editMessageText', params=_j_ord(locals()))


def editMessageCaption(chat_id=None, message_id=None, inline_message_id=None,
                       caption=None, parse_mode=None, reply_markup=None, update=None):
    if update:
        chat_id, message_id = _replay(update)
    return requests.post(api + 'editMessageCaption', params=_j_ord(locals()))


def editMessageMedia(chat_id=None, message_id=None, inline_message_id=None,
                     media=None, reply_markup=None, update=None):
    if update:
        chat_id, message_id = _replay(update)
    media = {"type": "document", "media": media}
    return requests.post(api + 'editMessageMedia', params=_j_ord(locals()))


def editMessageReplyMarkup(chat_id=None, message_id=None,
                           inline_message_id=None, reply_markup=None, update=None):
    if update:
        chat_id, message_id = _replay(update)
    return requests.post(api + 'editMessageReplyMarkup', params=_j_ord(locals()))


def deleteMessage(chat_id=None, message_id=None, update=None):
    if update:
        chat_id, message_id = _replay(update)
    params = {'chat_id': chat_id, 'message_id': message_id}
    return requests.get(api + 'deleteMessage', params=params)


def sendSticker(chat_id, file, disable_notification, reply_to_message_id=None, reply_markup=None):
    j, files = _file('sticker', locals())
    return requests.post(api + 'sendSticker', params=j, files=files)


def getStickerSet(name):
    return requests.get(api + 'getStickerSet', params=_j_ord(locals()))


def uploadStickerFile(user_id, file):
    j, files = _file('png_sticker', locals())
    return requests.post(api + 'uploadStickerFile', params=j, files=files)


def createNewStickerSet(user_id, name, title, file, emojis, contains_masks=None, mask_position=None):
    j, files = _file('png_sticker', locals())
    return requests.post(api + 'createNewStickerSet', params=j, files=files)


def addStickerToSet(user_id, name, file, emojis, mask_position=None):
    j, files = _file('png_sticker', locals())
    return requests.post(api + 'addStickerToSet', params=j, files=files)


def setStickerPositionInSet(sticker, position):
    return requests.get(api + 'setStickerPositionInSet', params=_j_ord(locals()))


def deleteStickerFromSet(sticker):
    return requests.get(api + 'deleteStickerFromSet', params=_j_ord(locals()))


def answerInlineQuery(update, results, cache_time='300', is_personal=None,
                      next_offset=None, switch_pm_text=None, switch_pm_parameter=None):
    inline_query_id = update.inline_query.id
    return requests.post(api + 'answerInlineQuery', json=_j_ord(locals()))


def InlineQueryResultArticle(id, title=None, input_message_content=None,
                             reply_markup=None, url=None, hide_url=None, description=None,
                             thumb_url=None, thumb_width=None, thumb_height=None):
    j = _j_ord(locals())
    j['type'] = 'article'
    return j


def InlineQueryResultPhoto(id, photo_url=None, thumb_url=None, photo_width=None,
                           photo_height=None, title=None, description=None, caption=None,
                           parse_mode='Markdown', reply_markup=None, input_message_content=None):
    j = _j_ord(locals())
    j['type'] = 'photo'
    return j


def InlineQueryResultGif(id, gif_url, gif_width=None, gif_height=None, thumb_url=None, title=None,
                         caption=None, parse_mode=None, reply_markup=None, input_message_content=None):
    j = _j_ord(locals())
    j['type'] = 'gif'
    return j


def InlineQueryResultMpeg4Gif(id, mpeg4_url, mpeg4_width=None, mpeg4_height=None, mpeg4_duration=None, thumb_url=None,
                              title=None, caption=None, parse_mode=None, reply_markup=None, input_message_content=None):
    j = _j_ord(locals())
    j['type'] = 'mpeg4_gif'
    return j


def InlineQueryResultVideo(id, video_url, mime_type, thumb_url, title, caption=None, parse_mode=None,
                           video_width=None, video_height=None, video_duration=None, description=None,
                           reply_markup=None, input_message_content=None):
    j = _j_ord(locals())
    j['type'] = 'video'
    return j


def InlineQueryResultAudio(id, audio_url, title, caption, parse_mode=None, performer=None, audio_duration=None,
                           reply_markup=None, input_message_content=None):
    j = _j_ord(locals())
    j['type'] = 'audio'
    return j


def InlineQueryResultVoice(id, voice_url, title, caption=None, parse_mode=None, voice_duration=None,
                           reply_markup=None, input_message_content=None):
    j = _j_ord(locals())
    j['type'] = 'voice'
    return j


def InlineQueryResultDocument(id, title=None, caption=None, parse_mode=None,
                              document_url=None, mime_type=None, description=None,
                              reply_markup=None, input_message_content=None,
                              thumb_url=None, thumb_width=None, thumb_height=None):
    j = _j_ord(locals())
    j['type'] = 'document'
    return j


def InlineQueryResultLocation(id, latitude, longitude, title, live_period=None, reply_markup=None,
                              input_message_content=None, thumb_url=None, thumb_width=None, thumb_height=None):
    j = _j_ord(locals())
    j['type'] = 'location'
    return j


def InlineQueryResultVenue(id, latitude, longitude, title, address, foursquare_id=None, reply_markup=None,
                           input_message_content=None, thumb_url=None, thumb_width=None, thumb_height=None):
    j = _j_ord(locals())
    j['type'] = 'venue'
    return j


def InlineQueryResultContact(id, phone_number, first_name, last_name=None, vcard=None, reply_markup=None,
                             input_message_content=None, thumb_url=None, thumb_width=None, thumb_height=None):
    j = _j_ord(locals())
    j['type'] = 'contact'
    return j


def InlineQueryResultGame(id, game_short_name, reply_markup):
    j = _j_ord(locals())
    j['type'] = 'game'
    return j


def InlineQueryResultCachedPhoto(id, photo_file_id, title=None, description=None, caption=None,
                                 parse_mode=None, reply_markup=None, input_message_content=None):
    j = _j_ord(locals())
    j['type'] = 'photo'
    return j


def InlineQueryResultCachedGif(id, gif_file_id, title=None, caption=None, parse_mode=None,
                               reply_markup=None, input_message_content=None):
    j = _j_ord(locals())
    j['type'] = 'gif'
    return j


def InlineQueryResultCachedMpeg4Gif(id, mpeg4_file_id, title=None, caption=None, parse_mode=None,
                                    reply_markup=None, input_message_content=None):
    j = _j_ord(locals())
    j['type'] = 'mpeg4_gif'
    return j


def InlineQueryResultCachedSticker(id, sticker_file_id=None, reply_markup=None, input_message_content=None):
    j = _j_ord(locals())
    j['type'] = 'sticker'
    return j


def InlineQueryResultCachedDocument(id, title, document_file_id, description=None, caption=None,
                                    parse_mode=None, reply_markup=None, input_message_content=None):
    j = _j_ord(locals())
    j['type'] = 'document'
    return j


def InlineQueryResultCachedVideo(id, video_file_id, title, description=None, caption=None, parse_mode=None,
                                 reply_markup=None, input_message_content=None):
    j = _j_ord(locals())
    j['type'] = 'video'
    return j


def InlineQueryResultCachedVoice(id, voice_file_id, title, caption=None,
                                 parse_mode=None, reply_markup=None, input_message_content=None):
    j = _j_ord(locals())
    j['type'] = 'voice'
    return j


def InlineQueryResultCachedAudio(id, audio_file_id, caption, parse_mode=None,
                                 reply_markup=None, input_message_content=None):
    j = _j_ord(locals())
    j['type'] = 'audio'
    return j


def InputTextMessageContent(message_text=None, parse_mode=None):
    return _j_ord(locals())


def InputLocationMessageContent(latitude, longitude, live_period=None):
    return _j_ord(locals())


def InputVenueMessageContent(latitude, longitude, title, address, foursquare_id=None, foursquare_type=None):
    return _j_ord(locals())


def InputContactMessageContent(phone_number, first_name, last_name=None, vcard=None):
    return _j_ord(locals())


def ChosenInlineResult(result_id, from_user, location=None, inline_message_id=None, query=None):
    return _j_ord(locals())


def InputMediaPhoto(media, caption=None, parse_mode=None):
    j = _j_ord(locals())
    j['type'] = 'photo'
    return j


def InputMediaVideo(media, thumb=None, caption=None, parse_mode=None,
                    width=None, height=None, duration=None, supports_streaming=None):
    j = _j_ord(locals())
    j['type'] = 'video'
    return j


def InputMediaAnimation(media, thumb=None, caption=None, parse_mode=None,
                        width=None, height=None, duration=None):
    j = _j_ord(locals())
    j['type'] = 'animation'
    return j


def InputMediaAudio(media, thumb=None, caption=None, parse_mode=None,
                    duration=None, performer=None, title=None):
    j = _j_ord(locals())
    j['type'] = 'audio'
    return j


def InputMediaDocument(media, thumb=None, caption=None, parse_mode=None):
    j = _j_ord(locals())
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
    chat_id, message_id = _replay(update)
    if file:
        if photo:
            return sendPhoto(chat_id, reply_to_message_id=message_id,
                             file=photo, caption=text,
                             reply_markup=reply_markup)
        else:
            return sendDocument(chat_id, reply_to_message_id=message_id,
                                file=file, caption=text)

    reply_to_message_id = message_id
    return requests.post(api + 'sendMessage', json=_j_ord(locals()), verify=False)


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


def getPhoto(chat_id=None, file=None):
    f = sendPhoto(chat_id, file=file)
    return f.result.photo[0].file_id


def _get_file_send(chat_id=None, file=None, thumb=None):
    f = sendDocument(chat_id, file=file, thumb=thumb)
    a = f.result.document.file_id
    b = f.result.document.mime_type
    c = f.result.document.thumb.file_id
    return a, b, c


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
