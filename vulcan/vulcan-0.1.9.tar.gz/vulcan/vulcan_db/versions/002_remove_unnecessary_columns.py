from sqlalchemy import *
from migrate import *
from migrate.changeset import *

meta = MetaData()

def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    cards = Table('cards', meta, autoload=True)
    cards.c.last_answered.drop()
    cards.c.closing.drop()
    cards.c.times_asked.drop()
    cards.c.num_successes.drop()

def downgrade(migrate_engine):
    raise NotImplementedError
