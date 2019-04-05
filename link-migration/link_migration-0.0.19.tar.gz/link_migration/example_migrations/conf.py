# -*- coding: utf-8 -*-
import requests
import json
from glom import glom

from datetime import datetime
from pathlib import Path
from uuid import uuid4

ROOT_DIR = 'link_migration.example_migrations'
MIGRATIONS_ABS_PATH = Path(__file__).resolve().parent
MIGRATIONS_DIR = 'link_migration.example_migrations'

DRIVER = 'neo4j'
DRIVER_KWARGS = {'host': 'bolt://localhost:7687', 'auth': ('neo4j', 'password')}


def get_current_version(self):
    with self.driver.session() as session:
        response_data = self.driver.read(session, "MATCH (m:Migration) RETURN m")

        versions = []
        for response in response_data:
            versions.append(response['m']['version'])

        versions = sorted(versions, reverse=True)

        # Check for duplicate version numbers, fail if found
        check_versions = set()
        if any(s in check_versions or check_versions.add(s) for s in versions):
            check_versions = set()
            raise Exception(
                'Duplicate version numbers %s' % (
                    list(set(
                        s for s in versions if s in check_versions or check_versions.add(s)
                    ))
                )
            )

    return versions[0] if versions else 0


def set_current_version(self, migration):
    try:
        print(migration.migration_file.change_file)
    except:
        pass
    with self.driver.session() as session:
        response_data = self.driver.write(session, (
            f'CREATE (m:Migration {{'
            f'id: "{uuid4()}",'
            f'version: {migration.version},'
            f'changelog_file: "test",'
            f'started_datetime: "{datetime.now()}",'
            f'ended_datetime: "{datetime.now()}",'
            f'checksum: "test",'
            f'previous: "test"'
            f'}}) RETURN m'
        ))

        for response in response_data:
            print(response['m'])

        if migration.previous:
            response_data = self.driver.write(session, (
                f"MATCH(a:Migration), (b:Migration)"
                f"WHERE a.version = {migration.version} AND b.version = {migration.previous.version} "
                f"CREATE (a)-[:PREVIOUS]->(b)"
                f"RETURN a, b"
            ))

            for response in response_data:
                print(response['a'])
                print(response['b'])

    return migration.version
