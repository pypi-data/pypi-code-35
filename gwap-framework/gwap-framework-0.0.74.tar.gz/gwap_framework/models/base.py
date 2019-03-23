from datetime import datetime
from pytz import timezone

from sqlalchemy import Boolean, Column, DateTime

from sqlalchemy.ext.declarative import declarative_base


class Base(object):

    created_at = Column(DateTime, nullable=False, default=datetime.now(tz=timezone('America/Sao_Paulo')))
    updated_at = Column(DateTime, nullable=True)
    deleted = Column(Boolean, default=False, nullable=False)


BaseModel = declarative_base(cls=Base)
