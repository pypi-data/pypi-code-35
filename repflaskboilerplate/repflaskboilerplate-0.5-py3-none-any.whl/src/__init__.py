import db
from app_global import app
sys.modules["rep-db"] = (db,app)
