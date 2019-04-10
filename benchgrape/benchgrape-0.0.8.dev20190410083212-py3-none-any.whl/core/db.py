import sqlite3


class Mapper(object):
    def __init__(self, db_conn, logger):
        self.db = db_conn
        self.logger = logger

    def init_db(self):
        raise NotImplemented('mappers must implement init_db.')


class RuntimeConfigMapper(Mapper):
    db = None
    tables = ['runtime_config']

    def init_db(self):
        c = self.db.cursor()
        # Create tables
        self.logger.info('init runtime config table...')
        c.execute(
            '''CREATE TABLE IF NOT EXISTS runtime_config (
                recycle_mode boolean
            )'''
        )

    def enable_user_recycliing(self):
        c = self.db.cursor()
        c.execute("UPDATE runtime_config SET recycle_mode='TRUE'")
        self.db.commit()
        self.logger.info('enabled user recycle mode.')

    def disable_user_recycling(self):
        c = self.db.cursor()
        c.execute("UPDATE runtime_config SET recycle_mode='FALSE'")
        self.db.commit()
        self.logger.info('disabled user recycle mode.')


class TestDataMapper(Mapper):
    db = None
    tables = ['organizations', 'users', 'groups', 'private_conversations']

    def drop_db(self):
        c = self.db.cursor()
        for tb in self.tables:
            self.logger.info('dropping table %s' % tb)
            c.execute("DROP TABLE %s" % tb)
        self.logger.info('committing...')
        self.db.commit()
        self.logger.info('all gone!')

    def init_db(self):
        c = self.db.cursor()
        # Create tables
        try:
            self.logger.info('init organizations table...')
            c.execute(
                '''CREATE TABLE IF NOT EXISTS organizations (
                id INTEGER PRIMARY KEY, url text, name text, subdomain text,
                CONSTRAINT unique_id UNIQUE (id))'''
            )
            self.logger.info('init user table...')
            c.execute(
                '''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY, username text, password text,
                token text, connected boolean,
                CONSTRAINT unique_id UNIQUE (id))'''
            )
            self.logger.info('init groups table...')
            c.execute('''CREATE TABLE IF NOT EXISTS groups (
                        id INTEGER PRIMARY KEY, name text,
                        CONSTRAINT unique_id UNIQUE (id)
                    )''')
            self.logger.info('init PM table...')
            c.execute('''CREATE TABLE IF NOT EXISTS private_conversations (
                        id INTEGER PRIMARY KEY, creator text,
                        CONSTRAINT unique_id UNIQUE (id)
                    )''')
            self.db.commit()
        except sqlite3.OperationalError as ex:
            self.logger.error(ex)
            self.db.rollback()

        self.logger.info('nice, so many tables!')

    def stats(self):
        cur = self.db.cursor()
        stats = {}
        for tb in self.tables:
            cur.execute("select count(*) from %s" % tb)
            stats[tb] = cur.fetchone()[0]

        return stats

    def sync_db(self, organization, users=None, groups=None, private_conversations=None):
        c = self.db.cursor()
        try:
            self.logger.info('creating %s organization...' % organization['name'])
            c.execute(
                "INSERT OR REPLACE INTO organizations (id, url, name, subdomain) "
                "VALUES (%i, '%s', '%s', '%s')" % (
                    int(organization['id']), organization['url'],
                    organization['name'],  organization['subdomain']
                ))

            self.logger.info('inserting %s users...' % len(users))
            for u in users or []:
                c.execute(
                    "INSERT OR REPLACE INTO users (id, username, password, token, connected) "
                    "VALUES (%i, '%s', '%s', '%s', 'FALSE')" % (
                        int(u['id']), u['username'], u['password'], u['token']
                    ))

            self.logger.info('inserting %s groups...' % len(groups))
            for g in groups or []:
                c.execute(
                    "INSERT OR REPLACE INTO groups (id, name) "
                    "VALUES (%i, '%s')" % (int(g['id']), g['name'])
                )

            self.logger.info('inserting %s private conversations...' % len(
                private_conversations))
            for pc in private_conversations or []:
                c.execute(
                    "INSERT OR REPLACE INTO private_conversations (id, creator) "
                    "VALUES (%i, '%s')" % (int(pc['id']), pc['creator'])
                )
            self.logger.info('benchmark data in sync with config file.')
            self.logger.info(
                'data heap now consists of %s' % (
                    ["%s: %s" % (k, v) for k, v in self.stats().items()]
                ))

            self.db.commit()
        except sqlite3.OperationalError as ex:
            self.logger.error(ex)
            self.db.rollback()
            self.logger.error('rolled back to initial state!')

    def _pick_unique_user(self):
        self.logger.info('picking a user')
        c = self.db.cursor()
        user = c.execute("SELECT id, username, password, token "
                         "FROM users "
                         "WHERE connected='FALSE' "
                         "ORDER BY RANDOM() "
                         "LIMIT 1 "
                         ).fetchone()

        if not user:
            self.db.rollback()
            raise RuntimeError('no users left to use.')
        upt = c.execute("UPDATE users SET connected='TRUE' WHERE id=%s" % user[0])
        assert upt.rowcount == 1
        self.db.commit()
        self.logger.info('picked user: %s' % user[1])
        return {
            'id': user[0], 'username': user[1],
            'password': user[2], 'token': user[3]
        }

    def _pick_user(self):
        self.logger.info('picking a user')
        c = self.db.cursor()
        user = c.execute("SELECT id, username, password, token "
                         "FROM users "
                         "ORDER BY RANDOM() "
                         "LIMIT 1 "
                         ).fetchone()

        if not user:
            self.db.rollback()
            raise RuntimeError('no users left to use.')

        self.logger.info('picked user: %s' % user[1])
        return {
            'id': user[0], 'username': user[1],
            'password': user[2], 'token': user[3]
        }

    def pick_user(self):
        c = self.db.cursor()
        unique_mode = c.execute(
            "SELECT recycle_mode FROM runtime_config  LIMIT 1 "
        ).fetchone()

        user = None
        if not unique_mode:
            return self._pick_user()

        while user is None:
            # try:
            user = self._pick_unique_user()
            # except Exception as ex:
            #     self.logger.error(ex)
            #     user = self.pick_user()
        return user

    def relieve_user(self, user_id):
        c = self.db.cursor()
        c.execute("UPDATE users SET connected='FALSE' WHERE id=%s" % user_id)
        self.db.commit()
        self.logger.info('user %s relieved' % user_id)

    def get_host(self):
        c = self.db.cursor()
        c.execute("SELECT url from organizations")
        return c.fetchone()[0]

    def get_organization(self):
        c = self.db.cursor()
        c.execute("SELECT * from organizations")
        org = c.fetchone()
        return {
            'id': org[0],
            'host': org[1],
            'name': org[2],
            'subdomain': org[3],
        }

    def sanitize(self):
        c = self.db.cursor()
        c.execute("UPDATE users SET connected='FALSE'")
        self.db.commit()
        self.logger.info('all users relieved')
