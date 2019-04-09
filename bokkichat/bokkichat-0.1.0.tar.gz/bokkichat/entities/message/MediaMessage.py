"""LICENSE
Copyright 2018 Hermann Krumrey <hermann@krumreyh.com>

This file is part of bokkichat.

bokkichat is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

bokkichat is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with bokkichat.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

from bokkichat.entities.message.Message import Message
from bokkichat.entities.Address import Address
from bokkichat.entities.message.MediaType import MediaType


class MediaMessage(Message):
    """
    Class that defines an interface for media messages.
    Each media message has a media type, data and caption.
    """

    def __init__(
            self,
            sender: Address,
            receiver: Address,
            media_type: MediaType,
            data: bytes,
            caption: str
    ):
        """
        Initializes the TextMessage object
        :param sender: The sender of the message
        :param receiver: The receiver of the message
        :param media_type: The type of the contained media
        :param data: The data of the attached media
        :param caption: The caption attached to the media
        """
        super().__init__(sender, receiver)
        self.media_type = media_type
        self.data = data
        self.caption = caption

    def __str__(self) -> str:
        """
        :return: A string representation of the MediaMessage object
        """
        return "{}: {}".format(self.media_type.name, self.caption)
