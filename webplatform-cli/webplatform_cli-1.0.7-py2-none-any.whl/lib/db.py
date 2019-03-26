from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import binascii, os, json, hashlib

from .config import Settings
from .sessions import Session

class Manager(object):
   __instance = None

   mongo_client = None
   host = None
   config = None
   settings = None
   db_host = None
   db_port = None
   sessions = None

   __db = None

   def __new__(cls, *args, **kwargs):
      if Manager.__instance is None:
         Manager.__instance = object.__new__(cls)
         Manager.__instance.__set_class()

      return Manager.__instance

   def __init__(self, db=None, new_client=False):
      self.setup(db)


   def __set_class(self):
      Manager.settings = Settings()
      Manager.config = Manager.settings.get_config("mongodb")

      Manager.db_host = Manager.settings.get_config("mongodb")['host']
      Manager.db_port = Manager.settings.get_config("mongodb")['port']

      Manager.mongo_client = MongoClient(Manager.db_host, Manager.db_port, connect=False)
      Manager.ldap_server = Manager.ldap_server

      Manager.sessions = Session(Manager.mongo_client["cee-tools"])

   def setup(self, db):
      self.mongo_client = Manager.mongo_client
      self.host = Manager.host
      self.config = Manager.config
      self.settings = Manager.settings
      self.sessions = Manager.sessions

      if db != None:
         self.__db = Manager.mongo_client[db]
      else:
         self.__db = Manager.mongo_client["webplatform"]

   def db(self, db=None):
      if db == None:
         return self.__db
      else:
         return self.mongo_client[db]

   def new_connection(self):
      self.mongo_client = MongoClient(self.host, self.port)

   def drop_database(self, db):
      self.mongo_client.drop_database(db)

   def get_picture_url(self, email):
      email = email.encode('utf-8')
      return "https://secure.gravatar.com/avatar/" + hashlib.md5(email).hexdigest() + "?s=100&d=identicon"

   def set_hostname(self, hostname):
      self.host = hostname
      Manager.host = hostname
      return hostname

   def get_hostname(self):
      return self.host

   def get_http_port(self):
      return self.http_port

   def set_user_uid(self, uid):
      self.user_uid = uid

   def get_user_uid(self):
      return self.user_uid

   def set_permissions(self, permissions):
      self.permissions = permissions

   def get_permissions(self, app=None):
      if app == None:
         return self.permissions
      else:
         if app in self.permissions:
            return self.permissions[app]
         else:
            return []

   def get_session(self, **kwargs):
      return self.sessions.get_session(**kwargs)

   def get_all_sessions(self, uid):
      return self.sessions.get_session(uid=uid)

   def validate_session(self, *args):
      return self.sessions.validate(*args)

   def parse_cursor_object(self, cursor):
      if cursor == None or cursor == "":
         return

      if "_id" in cursor.keys():
         _id = cursor['_id']
         del cursor['_id']
         cursor['id'] = _id

      return cursor

   @staticmethod
   def get_current_time():
      return datetime.utcnow()

   @staticmethod
   def get_formatted_time():
      return Manager.get_current_time().isoformat()

   @staticmethod
   def timestamp_to_datetime(ts):
      return datetime.utcfromtimestamp(ts)

   @staticmethod
   def local_to_utc(date, local_tz):
      from datetime import datetime
      from pytz import timezone
      import pytz
      tz = timezone(local_tz)
      aware = tz.localize(date)
      return pytz.utc.normalize(aware)

   @staticmethod
   def local_timestamp_to_datetime(ts):
      from datetime import datetime
      date = datetime.fromtimestamp(ts)

      return Manager.local_to_utc(date, 'US/Eastern')

   def utc_to_local(date, tz):
      import pytz
      local_tz = pytz.timezone(tz)
      local_date = date.replace(tzinfo=pytz.utc).astimezone(local_tz)
      return local_tz.normalize(local_date)
