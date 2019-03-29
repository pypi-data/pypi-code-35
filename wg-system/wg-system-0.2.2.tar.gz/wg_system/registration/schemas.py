from typesystem import Schema, String, Integer, Boolean
from typesystem.base import ValidationError
from . models import Participants

class Register(Schema):
    name = String(max_length=64, allow_blank=False)
    surname = String(max_length=64, allow_blank=False)
    email = String(max_length=254, pattern=r'[^@]+@[^@]+\.[^@]+', allow_blank=False)
    birth_year = Integer()
    gender = String(max_length=1, pattern=r'^M$|^W$', allow_blank=False)
    info_channel = String(max_length=64, allow_blank=True)
    expected_burpees = Integer(minimum=0)

    @staticmethod
    async def validate_email_uniqueness(email: str) -> bool:
        participant = await Participants.objects.get_or_none(email=email)
        if participant is not None:
            return False

        return True
