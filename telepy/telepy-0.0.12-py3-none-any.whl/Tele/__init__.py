# Tele ver 0.0.12
import json
import requests
from threading import Thread
from time import sleep


def get_updates(timeout=10):
    try:
        return _call_api('getUpdates?timeout=%s' % timeout).json()['result']
    except KeyError:
        print('Unauthorized token')
        exit(1)
    except Exception as exc:
        _error(exc)
        sleep(2)
        return


def send_message(chat_id, text, parse_mode='Markdown',
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
        return _chat_ids(send_message, **params)
    return _call_api('sendMessage', params=_check_none(params))


def forward_message(chat_id=None, from_chat_id=None, message_id=None,
                    disable_notification=None, update=None):
    params = {
        'chat_id': chat_id,
        'from_chat_id': from_chat_id,
        'message_id': message_id,
        'disable_notification': disable_notification,
        'update': update,
    }
    if _is_list(chat_id):
        return _chat_ids(forward_message, **params)
    if update:
        params['from_chat_id'], params['message_id'] = _replay(update)
    return _call_api('forwardMessage', params=_check_none(params))


def send_photo(chat_id=None, file=None, caption=None, thumb=None,
               reply_to_message_id=None, parse_mode='Markdown',
               disable_web_page_preview=None, disable_notification=None,
               reply_markup=None):
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
        return _chat_ids(send_photo, **params)
    j, files = _file('photo', params)
    return _call_api('sendPhoto', params=j, files=files)


def send_audio(chat_id=None, file=None, caption=None, parse_mode=None,
               duration=None, performer=None, title=None, thumb=None):
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
        return _chat_ids(send_audio, **params)
    j, files = _file('audio', params)
    return _call_api('sendAudio', params=j, files=files)


def send_document(chat_id, file, caption=None, thumb=None,
                  reply_to_message_id=None, parse_mode='Markdown',
                  disable_web_page_preview=None, disable_notification=None,
                  reply_markup=None):
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
        return _chat_ids(send_document, **params)
    j, files = _file('document', params)
    return _call_api('sendDocument', params=j, files=files)


def send_video(chat_id, file, duration=None, width=None, height=None,
               thumb=None, caption=None, parse_mode=None,
               supports_streaming=None, disable_notification=None,
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
        return _chat_ids(send_video, **params)
    j, files = _file('video', params)
    return _call_api('sendVideo', params=j, files=files)


def send_animation(chat_id, file, duration=None, width=None, height=None,
                   thumb=None, caption=None, parse_mode=None,
                   disable_notification=None, reply_to_message_id=None,
                   reply_markup=None):
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
    return _call_api('sendAnimation', params=j, files=files)


def send_voice(chat_id, file, caption=None, parse_mode=None, duration=None,
               disable_notification=None, reply_to_message_id=None,
               reply_markup=None):
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
        return _chat_ids(send_voice, **params)
    j, files = _file('voice', params)
    return _call_api('sendVoice', params=j, files=files)


def send_video_note(chat_id, file, duration=None, length=None, thumb=None,
                    disable_notification=None, reply_to_message_id=None,
                    reply_markup=None):
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
        return _chat_ids(send_video_note, **params)
    j, files = _file('video_note', params)
    return _call_api('sendVideoNote', params=j, files=files)


def send_media_group(chat_id, media, disable_notification=None,
                     reply_to_message_id=None):
    params = {
        'chat_id': chat_id,
        'media': media,
        'disable_notification': disable_notification,
        'reply_to_message_id': reply_to_message_id,
    }
    if _is_list(chat_id):
        return _chat_ids(send_media_group, **params)
    return _call_api('sendMediaGroup', json=_check_none(params))


def send_location(chat_id, latitude, longitude, live_period=None,
                  disable_notification=None, reply_to_message_id=None,
                  reply_markup=None):
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
        return _chat_ids(send_location, **params)
    return _call_api('sendLocation', params=_check_none(params))


def edit_message_live_location(chat_id=None, message_id=None,
                               inline_message_id=None, latitude=None,
                               longitude=None, reply_markup=None, update=None):
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
    return _call_api('editMessageLiveLocation', params=_check_none(params))


def stop_message_live_location(chat_id=None, message_id=None,
                               inline_message_id=None, reply_markup=None,
                               update=None):
    params = {
        'chat_id': chat_id,
        'message_id': message_id,
        'inline_message_id': inline_message_id,
        'reply_markup': reply_markup,
        'update': update,
    }
    if update:
        params['chat_id'], params['message_id'] = _replay(update)
    return _call_api('stopMessageLiveLocation', params=_check_none(params))


def send_venue(chat_id, latitude, longitude, title, address,
               foursquare_id=None, foursquare_type=None,
               disable_notification=None, reply_to_message_id=None,
               reply_markup=None):
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
        return _chat_ids(send_venue, **params)
    return _call_api('sendVenue', params=_check_none(params))


def send_contact(chat_id, phone_number, first_name, last_name=None,
                 vcard=None, disable_notification=None,
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
        return _chat_ids(send_contact, **params)
    return _call_api('sendContact', params=_check_none(params))


def send_chat_action(chat_id, action):
    params = {
        'chat_id': chat_id,
        'action': action,
    }
    if _is_list(chat_id):
        return _chat_ids(send_chat_action, **params)
    return _call_api('sendChatAction', params=_check_none(params))


def get_user_profile_photos(user_id, offset=None, limit=None):
    params = {
        'user_id': user_id,
        'offset': offset,
        'limit': limit,
    }
    return _call_api('getUserProfilePhotos', params=_check_none(params))


def get_file(file_id):
    return _call_api('getFile?file_id=' + file_id).json()


def kick_chat_member(chat_id, user_id, until_date=None):
    params = {
        'chat_id': chat_id,
        'user_id': user_id,
        'until_date': until_date,
    }
    return _call_api('kickChatMember', params=_check_none(params))


def unban_chat_member(chat_id, user_id):
    params = {
        'chat_id': chat_id,
        'user_id': user_id,
    }

    return _call_api('unbanChatMember', params=_check_none(params))


def restrict_chat_member(chat_id, user_id, until_date=None,
                         can_send_messages=None, can_send_media_messages=None,
                         can_send_other_messages=None,
                         can_add_web_page_previews=None):
    params = {
        'chat_id': chat_id,
        'user_id': user_id,
        'until_date': until_date,
        'can_send_messages': can_send_messages,
        'can_send_media_messages': can_send_media_messages,
        'can_send_other_messages': can_send_other_messages,
        'can_add_web_page_previews': can_add_web_page_previews,
    }

    return _call_api('restrictChatMember', params=_check_none(params))


def promote_chat_member(chat_id, user_id, can_change_info=None,
                        can_post_messages=None, can_edit_messages=None,
                        can_delete_messages=None, can_invite_users=None,
                        can_restrict_members=None, can_pin_messages=None,
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
    return _call_api('promoteChatMember', params=_check_none(params))


def export_chat_invite_link(chat_id):
    params = {
        'chat_id': chat_id,
    }
    return _call_api('exportChatInviteLink', params=params)


def set_chat_photo(chat_id, photo):
    params = {
        'chat_id': chat_id,
        'photo': photo,
    }

    j, files = _file('photo', params)
    return _call_api('sendVideoNote', params=j, files=files)


def delete_chat_photo(chat_id):
    params = {
        'chat_id': chat_id,
    }
    return _call_api('deleteChatPhoto', params=params)


def set_chat_title(chat_id, title):
    params = {
        'chat_id': chat_id,
        'title': title,
    }
    return _call_api('setChatTitle', params=params)


def set_chat_description(chat_id, description):
    params = {
        'chat_id': chat_id,
        'description': description,
    }

    return _call_api('setChatDescription', params=params)


def pin_chat_message(chat_id, message_id, disable_notification=None):
    params = {
        'chat_id': chat_id,
        'message_id': message_id,
        'disable_notification': disable_notification,
    }
    return _call_api('pinChatMessage', params=_check_none(params))


def unpin_chat_message(chat_id):
    params = {
        'chat_id': chat_id,
    }
    return _call_api('unpinChatMessage', params=params)


def leave_chat(chat_id):
    params = {
        'chat_id': chat_id,
    }
    return _call_api('leaveChat', params=params)


def get_chat(chat_id):
    params = {
        'chat_id': chat_id,
    }
    return _call_api('getChat', params=params)


def get_chat_administrators(chat_id):
    params = {
        'chat_id': chat_id,
    }
    return _call_api('getChatAdministrators', params=params)


def get_chat_members_count(chat_id):
    params = {
        'chat_id': chat_id,
    }
    return _call_api('ChatMembersCount', params=params)


def get_chat_member(chat_id, user_id):
    params = {
        'chat_id': chat_id,
        'user_id': user_id,
    }
    return _call_api('getChatMember', params=params)


def set_chat_sticker_set(chat_id, sticker_set_name):
    params = {
        'chat_id': chat_id,
        'sticker_set_name': sticker_set_name,
    }
    return _call_api('setChatStickerSet', params=params)


def delete_chat_sticker_set(chat_id):
    params = {
        'chat_id': chat_id,
    }
    return _call_api('deleteChatStickerSet', params=params)


def answer_callback_query(callback_query_id, text=None, show_alert=None,
                          url=None, cache_time=None):
    params = {
        'callback_query_id': callback_query_id,
        'text': text,
        'show_alert': show_alert,
        'url': url,
        'cache_time': cache_time,
    }
    return _call_api('answerCallbackQuery', params=_check_none(params))


def edit_message_text(chat_id=None, message_id=None, inline_message_id=None,
                      text=None, parse_mode=None,
                      disable_web_page_preview=None,
                      reply_markup=None, update=None):
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
    return _call_api('editMessageText', params=_check_none(params))


def edit_message_caption(chat_id=None, message_id=None, inline_message_id=None,
                         caption=None, parse_mode=None, reply_markup=None,
                         update=None):
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
    return _call_api('editMessageCaption', params=_check_none(params))


def edit_message_media(chat_id=None, message_id=None, inline_message_id=None,
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
    return _call_api('editMessageMedia', params=_check_none(params))


def edit_message_reply_markup(chat_id=None, message_id=None,
                              inline_message_id=None, reply_markup=None,
                              update=None):
    params = {
        'chat_id': chat_id,
        'message_id': message_id,
        'inline_message_id': inline_message_id,
        'reply_markup': reply_markup,
        'update': update,
    }
    if update:
        params['chat_id'], params['message_id'] = _replay(update)
    return _call_api('editMessageReplyMarkup', params=_check_none(params))


def delete_message(chat_id=None, message_id=None, update=None):
    if update:
        chat_id, message_id = _replay(update)
    params = {'chat_id': chat_id, 'message_id': message_id}
    return _call_api('deleteMessage', params=params)


def send_sticker(chat_id, file, disable_notification,
                 reply_to_message_id=None, reply_markup=None):
    params = {
        'chat_id': chat_id,
        'file': file,
        'disable_notification': disable_notification,
        'reply_to_message_id': reply_to_message_id,
        'reply_markup': reply_markup,
    }

    j, files = _file('sticker', params)
    return _call_api('sendSticker', params=j, files=files)


def get_sticker_set(name):
    params = {
        'name': name,
    }
    return _call_api('getStickerSet', params=params)


def upload_sticker_file(user_id, file):
    params = {
        'user_id': user_id,
        'file': file,
    }
    j, files = _file('png_sticker', params)
    return _call_api('uploadStickerFile', params=j, files=files)


def create_new_sticker_set(user_id, name, title, file, emojis,
                           contains_masks=None, mask_position=None):
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
    return _call_api('createNewStickerSet', params=j, files=files)


def add_sticker_to_set(user_id, name, file, emojis, mask_position=None):
    params = {
        'user_id': user_id,
        'name': name,
        'file': file,
        'emojis': emojis,
        'mask_position': mask_position,
    }
    j, files = _file('png_sticker', params)
    return _call_api('addStickerToSet', params=j, files=files)


def set_sticker_position_in_set(sticker, position):
    params = {
        'sticker': sticker,
        'position': position,
    }
    return _call_api('setStickerPositionInSet', params=params)


def delete_sticker_from_set(sticker):
    params = {
        'sticker': sticker,
    }
    return _call_api('deleteStickerFromSet', params=params)


def answer_inline_query(update, results, cache_time='300', is_personal=None,
                        next_offset=None, switch_pm_text=None,
                        switch_pm_parameter=None):
    params = {
        'inline_query_id': update.inline_query.id,
        'results': results,
        'cache_time': cache_time,
        'is_personal': is_personal,
        'next_offset': next_offset,
        'switch_pm_text': switch_pm_text,
        'switch_pm_parameter': switch_pm_parameter,
    }
    return _call_api('answerInlineQuery', json=_check_none(params))


def inline_query_result_article(id, title=None, input_message_content=None,
                                reply_markup=None, url=None, hide_url=None,
                                description=None, thumb_url=None,
                                thumb_width=None, thumb_height=None):
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
    j = _check_none(params)
    j['type'] = 'article'
    return j


def inline_query_result_photo(id, photo_url=None, thumb_url=None,
                              photo_width=None, photo_height=None,
                              title=None, description=None, caption=None,
                              parse_mode='Markdown', reply_markup=None,
                              input_message_content=None):
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
    j = _check_none(params)
    j['type'] = 'photo'
    return j


def inline_query_result_gif(id, gif_url, gif_width=None, gif_height=None,
                            thumb_url=None, title=None, caption=None,
                            parse_mode=None, reply_markup=None,
                            input_message_content=None):
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
    j = _check_none(params)
    j['type'] = 'gif'
    return j


def inline_query_result_mpeg4_gif(id, mpeg4_url, mpeg4_width=None,
                                  mpeg4_height=None, mpeg4_duration=None,
                                  thumb_url=None, title=None, caption=None,
                                  parse_mode=None, reply_markup=None,
                                  input_message_content=None):
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
    j = _check_none(params)
    j['type'] = 'mpeg4_gif'
    return j


def inline_query_result_video(id, video_url, mime_type, thumb_url, title,
                              caption=None, parse_mode=None, video_width=None,
                              video_height=None, video_duration=None,
                              description=None, reply_markup=None,
                              input_message_content=None):
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
    j = _check_none(params)
    j['type'] = 'video'
    return j


def inline_query_result_audio(id, audio_url, title, caption, parse_mode=None,
                              performer=None, audio_duration=None,
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
    j = _check_none(params)
    j['type'] = 'audio'
    return j


def inline_query_result_voice(id, voice_url, title, caption=None,
                              parse_mode=None, voice_duration=None,
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
    j = _check_none(params)
    j['type'] = 'voice'
    return j


def inline_query_result_document(id, title=None, caption=None, parse_mode=None,
                                 document_url=None, mime_type=None,
                                 description=None, reply_markup=None,
                                 input_message_content=None, thumb_url=None,
                                 thumb_width=None, thumb_height=None):
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

    j = _check_none(params)
    j['type'] = 'document'
    return j


def inline_query_result_location(id, latitude, longitude, title,
                                 live_period=None, reply_markup=None,
                                 input_message_content=None, thumb_url=None,
                                 thumb_width=None, thumb_height=None):
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
    j = _check_none(params)
    j['type'] = 'location'
    return j


def inline_query_result_venue(id, latitude, longitude, title, address,
                              foursquare_id=None, reply_markup=None,
                              input_message_content=None, thumb_url=None,
                              thumb_width=None, thumb_height=None):
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

    j = _check_none(params)
    j['type'] = 'venue'
    return j


def inline_query_result_contact(id, phone_number, first_name, last_name=None,
                                vcard=None, reply_markup=None,
                                input_message_content=None, thumb_url=None,
                                thumb_width=None, thumb_height=None):
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
    j = _check_none(params)
    j['type'] = 'contact'
    return j


def inline_query_result_game(id, game_short_name, reply_markup):
    params = {
        'id': id,
        'game_short_name': game_short_name,
        'reply_markup': reply_markup,
    }
    j = _check_none(params)
    j['type'] = 'game'
    return j


def inline_query_result_cached_photo(id, photo_file_id, title=None,
                                     description=None, caption=None,
                                     parse_mode=None, reply_markup=None,
                                     input_message_content=None):
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
    j = _check_none(params)
    j['type'] = 'photo'
    return j


def inline_query_result_cached_gif(id, gif_file_id, title=None, caption=None,
                                   parse_mode=None, reply_markup=None,
                                   input_message_content=None):
    params = {
        'id': id,
        'gif_file_id': gif_file_id,
        'title': title,
        'caption': caption,
        'parse_mode': parse_mode,
        'reply_markup': reply_markup,
        'input_message_content': input_message_content,
    }
    j = _check_none(params)
    j['type'] = 'gif'
    return j


def inline_query_result_cached_mpeg4_gif(id, mpeg4_file_id, title=None,
                                         caption=None, parse_mode=None,
                                         reply_markup=None,
                                         input_message_content=None):
    params = {
        'id': id,
        'mpeg4_file_id': mpeg4_file_id,
        'title': title,
        'caption': caption,
        'parse_mode': parse_mode,
        'reply_markup': reply_markup,
        'input_message_content': input_message_content,
    }
    j = _check_none(params)
    j['type'] = 'mpeg4_gif'
    return j


def inline_query_result_cached_sticker(id, sticker_file_id=None,
                                       reply_markup=None,
                                       input_message_content=None):
    params = {
        'id': id,
        'sticker_file_id': sticker_file_id,
        'reply_markup': reply_markup,
        'input_message_content': input_message_content,
    }
    j = _check_none(params)
    j['type'] = 'sticker'
    return j


def inline_query_result_cached_document(id, title, document_file_id,
                                        description=None, caption=None,
                                        parse_mode=None, reply_markup=None,
                                        input_message_content=None):
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
    j = _check_none(params)
    j['type'] = 'document'
    return j


def inline_query_result_cached_video(id, video_file_id, title,
                                     description=None, caption=None,
                                     parse_mode=None, reply_markup=None,
                                     input_message_content=None):
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
    j = _check_none(params)
    j['type'] = 'video'
    return j


def inline_query_result_cached_voice(id, voice_file_id, title, caption=None,
                                     parse_mode=None, reply_markup=None,
                                     input_message_content=None):
    params = {
        'id': id,
        'voice_file_id': voice_file_id,
        'title': title,
        'caption': caption,
        'parse_mode': parse_mode,
        'reply_markup': reply_markup,
        'input_message_content': input_message_content,
    }
    j = _check_none(params)
    j['type'] = 'voice'
    return j


def inline_query_result_cached_audio(id, audio_file_id,
                                     caption, parse_mode=None,
                                     reply_markup=None,
                                     input_message_content=None):
    params = {
        'id': id,
        'audio_file_id': audio_file_id,
        'caption': caption,
        'parse_mode': parse_mode,
        'reply_markup': reply_markup,
        'input_message_content': input_message_content,
    }
    j = _check_none(params)
    j['type'] = 'audio'
    return j


def input_text_message_content(message_text=None, parse_mode=None):
    params = {
        'message_text': message_text,
        'parse_mode': parse_mode,
    }
    return _check_none(params)


def input_location_message_content(latitude, longitude, live_period=None):
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'live_period': live_period,
    }
    return _check_none(params)


def input_venue_message_content(latitude, longitude, title, address,
                                foursquare_id=None, foursquare_type=None):
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'title': title,
        'address': address,
        'foursquare_id': foursquare_id,
        'foursquare_type': foursquare_type,
    }
    return _check_none(params)


def input_contact_message_content(phone_number, first_name, last_name=None,
                                  vcard=None):
    params = {
        'phone_number': phone_number,
        'first_name': first_name,
        'last_name': last_name,
        'vcard': vcard,
    }
    return _check_none(params)


def chosen_inline_result(result_id, from_user, location=None,
                         inline_message_id=None, query=None):
    params = {
        'result_id': result_id,
        'from_user': from_user,
        'location': location,
        'inline_message_id': inline_message_id,
        'query': query,
    }
    return _check_none(params)


def input_media_photo(media, caption=None, parse_mode=None):
    params = {
        'media': media,
        'caption': caption,
        'parse_mode': parse_mode,
    }

    j = _check_none(params)
    j['type'] = 'photo'
    return j


def input_media_video(media, thumb=None, caption=None, parse_mode=None,
                      width=None, height=None, duration=None,
                      supports_streaming=None):
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
    j = _check_none(params)
    j['type'] = 'video'
    return j


def input_media_animation(media, thumb=None, caption=None, parse_mode=None,
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
    j = _check_none(params)
    j['type'] = 'animation'
    return j


def input_media_audio(media, thumb=None, caption=None, parse_mode=None,
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
    j = _check_none(params)
    j['type'] = 'audio'
    return j


def input_media_document(media, thumb=None, caption=None, parse_mode=None):
    params = {
        'media': media,
        'thumb': thumb,
        'caption': caption,
        'parse_mode': parse_mode,
    }
    j = _check_none(params)
    j['type'] = 'document'
    return j


def keyboard_markup(k=None, resize_keyboard=True,
                    one_time_keyboard=None, num_line=None, remove=False):
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


def inline_keyboard(k=None, num_line=2, obj='callback_data'):
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


"""
The following functions do not exist in the methods or object of Telegram api.
These functions are optimized for use
"""


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


def message_reply(update, text=None, file=None, photo=None,
                  parse_mode='Markdown', disable_web_page_preview=None,
                  reply_markup=None):
    chat_id, reply_to_message_id = _replay(update)
    if file:
        if photo:
            return sendPhoto(chat_id, reply_to_message_id=reply_to_message_id,
                             file=photo, caption=text,
                             reply_markup=reply_markup)
        else:
            return sendDocument(chat_id,
                                reply_to_message_id=reply_to_message_id,
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
    return _call_api('sendMessage', json=_check_none(params))


def down_document(file_id=None, name='', dest='', update=None):
    try:
        if update:
            name = update['document']['file_name']
            file_id = update['document']['file_id']
        file_path = getFile(file_id)['result']['file_path']
        file = requests.get('{}file/{}/{}'.format(_api[:25], _api[25:],
                                                  file_path))
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
    j = _check_none(loc)
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
        chat_id = update.edited_message['from'].id
        message_id = update.edited_message.message_id
    else:
        chat_id, message_id = update['from'].id, update.message.message_id
    return chat_id, message_id


def _offset(update_id=False):
    """cleaning the getUpdates"""
    try:
        if update_id:
            params = {'offset': update_id + 1}
        else:
            params = {
                'offset':
                    _call_api('getUpdates').json()['result'][-1]['update_id']+1
            }
        return _call_api('getUpdates', params=params)
    except Exception as exc:
        _error(exc)
        pass


def _check_none(params):
    return dict(filter(lambda item: item[1] is not None, params.items()))


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


def _call_api(function, **kwargs):
    """Make api call"""
    try:
        response = requests.post(_api + function, **kwargs)
        if not response.json()['ok']:
            _error(response)
        return response
    except Exception as exc:
        return _error(exc)


_funcs_list = {}
_error_func_list = []


def _error(update):
    if _error_func_list:
        for func in _error_func_list:
            func(update)


def bot(filters=None, type_chat=None, not_on=None, on_error=None):
    def decorator(func):
        if on_error:
            _error_func_list.append(func)
        else:
            _funcs_list[func] = {'filter': filters, 'type_chat': type_chat,
                                 'not_on': not_on}

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
    for func in _funcs_list:
        f = _funcs_list[func]
        if f['type_chat']:
            if 'message' in up:
                if f['type_chat'] != up['message']['chat']['type']:
                    continue
            elif f['type_chat'] != up['chat']['type']:
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
    if not _api:
        print('You need to insert token to "account" function')
        exit(1)
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


_api = None


def account(token=None):
    if not token:
        return 'no token'
    global _api
    _api = 'https://api.telegram.org/bot%s/' % token
    return _api


# camelCase aliases

getUpdates = get_updates
sendMessage = send_message
forwardMessage = forward_message
sendPhoto = send_photo
sendAudio = send_audio
sendDocument = send_document
sendVideo = send_video
sendAnimation = send_animation
sendVoice = send_voice
sendVideoNote = send_video_note
sendMediaGroup = send_media_group
sendLocation = send_location
editMessageLiveLocation = edit_message_live_location
stopMessageLiveLocation = stop_message_live_location
sendVenue = send_venue
sendContact = send_contact
sendChatAction = send_chat_action
getUserProfilePhotos = get_user_profile_photos
getFile = get_file
kickChatMember = kick_chat_member
unbanChatMember = unban_chat_member
restrictChatMember = restrict_chat_member
promoteChatMember = promote_chat_member
exportChatInviteLink = export_chat_invite_link
setChatPhoto = set_chat_photo
deleteChatPhoto = delete_chat_photo
setChatTitle = set_chat_title
setChatDescription = set_chat_description
pinChatMessage = pin_chat_message
unpinChatMessage = unpin_chat_message
leaveChat = leave_chat
getChat = get_chat
getChatAdministrators = get_chat_administrators
getChatMembersCount = get_chat_members_count
getChatMember = get_chat_member
setChatStickerSet = set_chat_sticker_set
deleteChatStickerSet = delete_chat_sticker_set
answerCallbackQuery = answer_callback_query
editMessageText = edit_message_text
editMessageCaption = edit_message_caption
editMessageMedia = edit_message_media
editMessageReplyMarkup = edit_message_reply_markup
deleteMessage = delete_message
sendSticker = send_sticker
getStickerSet = get_sticker_set
uploadStickerFile = upload_sticker_file
createNewStickerSet = create_new_sticker_set
addStickerToSet = add_sticker_to_set
setStickerPositionInSet = set_sticker_position_in_set
deleteStickerFromSet = delete_sticker_from_set
answerInlineQuery = answer_inline_query
InlineQueryResultArticle = inline_query_result_article
InlineQueryResultPhoto = inline_query_result_photo
InlineQueryResultGif = inline_query_result_gif
InlineQueryResultMpeg4Gif = inline_query_result_mpeg4_gif
InlineQueryResultVideo = inline_query_result_video
InlineQueryResultAudio = inline_query_result_audio
InlineQueryResultVoice = inline_query_result_voice
InlineQueryResultDocument = inline_query_result_document
InlineQueryResultLocation = inline_query_result_location
InlineQueryResultVenue = inline_query_result_venue
InlineQueryResultContact = inline_query_result_contact
InlineQueryResultGame = inline_query_result_game
InlineQueryResultCachedPhoto = inline_query_result_cached_photo
InlineQueryResultCachedGif = inline_query_result_cached_gif
InlineQueryResultCachedMpeg4Gif = inline_query_result_cached_mpeg4_gif
InlineQueryResultCachedSticker = inline_query_result_cached_sticker
InlineQueryResultCachedDocument = inline_query_result_cached_document
InlineQueryResultCachedVideo = inline_query_result_cached_video
InlineQueryResultCachedVoice = inline_query_result_cached_voice
InlineQueryResultCachedAudio = inline_query_result_cached_audio
InputTextMessageContent = input_text_message_content
InputLocationMessageContent = input_location_message_content
InputVenueMessageContent = input_venue_message_content
InputContactMessageContent = input_contact_message_content
chosenInlineResult = chosen_inline_result
InputMediaPhoto = input_media_photo
InputMediaVideo = input_media_video
InputMediaAnimation = input_media_animation
InputMediaAudio = input_media_audio
InputMediaDocument = input_media_document
Keyboard = keyboard_markup
InlineKeyboard = inline_keyboard
