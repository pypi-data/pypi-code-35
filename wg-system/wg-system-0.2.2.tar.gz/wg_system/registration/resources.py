from databases import Database
from sqlalchemy import MetaData, create_engine
from aiosmtplib import SMTP
#from orm import ModelRegistry
from . settings import TESTING, DATABASE_TEST_URL, DATABASE_URL, SMTP_HOST, SMTP_PORT

DATABASE = Database(url=DATABASE_TEST_URL if TESTING else DATABASE_URL)
DATABASE_METADATA = MetaData()
DATABASE_ENGINE = create_engine(str(DATABASE.url))
# MODELS = ModelRegistry(database=database)
SMTP_SERVER = SMTP(hostname=SMTP_HOST, port=SMTP_PORT)
