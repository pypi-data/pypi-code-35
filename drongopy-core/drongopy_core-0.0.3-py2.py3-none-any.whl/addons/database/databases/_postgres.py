from collections import namedtuple

from peewee import PostgresqlDatabase
from playhouse.migrate import PostgresqlMigrator, migrate
from playhouse.reflection import Introspector

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 5432


ValidationResult = namedtuple('ValidationResult', (
    'valid', 'table_exists', 'add_fields', 'remove_fields', 'change_fields'))


class PostgresDatabase(object):
    def __init__(self, app, config):
        host = config.get('host', DEFAULT_HOST)
        port = config.get('port', DEFAULT_PORT)
        user = config.get('user')
        password = config.get('password')
        name = config.get('name')

        self.connection = PostgresqlDatabase(
            host=host,
            port=port,
            user=user,
            password=password,
            database=name,
            autorollback=True
        )
        self.connection.connect()

    def get(self):
        return self.connection

    def validate_schema(self, model):
        db = self.connection
        table = model._meta.table_name
        if not db.table_exists(table):
            return ValidationResult(False, False, None, None, None)

        introspector = Introspector.from_database(db)
        db_model = introspector.generate_models(table_names=[table])[table]

        columns = set(model._meta.columns)
        db_columns = set(db_model._meta.columns)

        to_remove = [db_model._meta.columns[c] for c in db_columns - columns]
        to_add = [model._meta.columns[c] for c in columns - db_columns]
        to_change = []
        # Take intersection and remove matches.
        intersect = columns & db_columns
        for column in intersect:
            field = model._meta.columns[column]
            db_field = db_model._meta.columns[column]
            if field.field_type != db_field.field_type:
                to_change.append((db_field, field))

        is_valid = not any((to_remove, to_add, to_change))
        return ValidationResult(is_valid, True, to_add, to_remove, to_change)

    def auto_migrate(self, model):
        result = self.validate_schema(model)
        if not result.table_exists:
            self.connection.create_tables([model])
            return

        migrator = PostgresqlMigrator(self.connection)

        if not result.valid:
            migrations = []
            for fld in result.add_fields:
                migrations.append(migrator.add_column(
                    model._meta.table_name, fld.column_name, fld))
            migrate(*migrations)
