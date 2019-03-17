from .exceptions import InvalidParseMode


class _ChatOrInlineMessage:
    def __chat_or_inline_message(self, chat_or_inline_message_id, message_id):
        if message_id is not None:
            self.args = {
                **self.args,
                'chat_id': chat_or_inline_message_id,
                'message_id': message_id
            }
        else:
            self.args['inline_message_id'] = chat_or_inline_message_id


class ReplyToMessageId:
    def reply_to_message_id(self, message_id):
        self.args['reply_to_message_id'] = message_id
        return self


class DisableNotification:
    def disable_notification(self):
        self.args['disable_notification'] = True
        return self


class ParseMode:
    def parse_mode(self, _parse_mode):
        if _parse_mode not in ['Markdown', 'HTML']:
            raise InvalidParseMode

        self.args['parse_mode'] = _parse_mode
        return self
