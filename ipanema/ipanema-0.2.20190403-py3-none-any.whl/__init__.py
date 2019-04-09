from ipanema.models import database_connection, Language


def query_language(s):
    with database_connection():
        return Language.query(s)
