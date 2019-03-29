from orm import Model, Integer, String, Boolean
from . settings import DATABASE_PARTICIPANTS_TABLE
from . resources import DATABASE, DATABASE_METADATA

class Participants(Model):
    __tablename__ = DATABASE_PARTICIPANTS_TABLE
    __database__ = DATABASE
    __metadata__ = DATABASE_METADATA

    id = Integer(primary_key=True)
    name = String(max_length=64, allow_null=False)
    surname = String(max_length=64, allow_null=False)
    email = String(max_length=254, index=True, unique=True, allow_null=False)
    birth_year = Integer(default=0, allow_null=False)
    gender = String(max_length=1, allow_null=False)
    info_channel = String(max_length=64, allow_null=False)
    confirmed = Boolean(default=False, allow_null=False)
    confirmation_code = String(max_length=64, index=True, allow_null=True)
    attended = Boolean(default=False, allow_null=False)
    expected_burpees = Integer(default=0, allow_null=False)
    burpees_made = Integer(default=0, allow_null=False)
    start_number = Integer(default=None, unique=True, allow_null=True)
