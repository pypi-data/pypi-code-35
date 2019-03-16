from abc import ABC


class TelegramEndpoint(ABC):
    method = 'GET'  # type: str
    endpoint = None  # type: str
    args = {}  # type: dict
    # data = None
    headers = {}  # type: dict

    def __init__(self):
        _classname = self.__class__.__name__
        self.endpoint = '%s%s' % (_classname[0].lower(), _classname[1:])

    def serialize(self):
        return self.method, self.endpoint, self.args, None, self.headers


from .chat import ExportChatInviteLink, SetChatPhoto, DeleteChatPhoto, SetChatTitle, SetChatDescription, PinChatMessage, UnpinChatMessage, LeaveChat, GetChat, GetChatAdministrators, GetChatMemberCount, GetChatMember, SetChatStickerSet, DeleteChatStickerSet  # noqa: F401, I101, E501
from .chat_action import SendChatAction  # noqa: F401, I101, E501
from .chat_member import KickChatMember, UnbanChatMember, RestrictChatMember, PromoteChatMember  # noqa: F401, I101, E501
from .contact import SendContact  # noqa: F401, I101, E501
from .file import EditMessageCaption, EditMessageMedia, GetFile, SendAudio, SendAnimation, SendDocument, SendMediaGroup, SendPhoto, SendVideo, SendVideoNote, SendVoice  # noqa: F401, I101, E501
from .forward import ForwardMessage  # noqa: F401, I101, E501
from .inline_mode import AnswerInlineQuery  # noqa: F401, I101, E501
from .location import SendLocation, EditMessageLiveLocation, StopMessageLiveLocation  # noqa: F401, I101, E501
from .reply_markup import InlineKeyboard, ReplyKeyboard, ReplyKeyboardRemove, ForceReply, AnswerCallbackQuery  # noqa: F401, I101, E501
from .text import SendMessage, EditMessageText  # noqa: F401, I101, E501
from .uncategorized import GetMe, GetUserProfilePhotos, EditMessageReplyMarkup, DeleteMessage  # noqa: F401, I101, E501
from .venue import SendVenue  # noqa: F401, I101, E501

from .exceptions import *  # noqa: F401, I101, F403, I100, I202
