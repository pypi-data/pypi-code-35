import pymysql.cursors


class DB:
    """docstring for DB"""

    def __init__(self):
        pass

    def db_connection(self, **args):

        if "db" in args:
            conn = pymysql.connect(host=args['host'],
                                   user=args['user'],
                                   password=args['password'],
                                   db=args['db'],
                                   charset="utf8mb4",
                                   cursorclass=pymysql.cursors.DictCursor)
        else:
            conn = pymysql.connect(host=args['host'],
                                   user=args['user'],
                                   password=args['password'],
                                   charset="utf8mb4",
                                   cursorclass=pymysql.cursors.DictCursor)

        return conn

    def create_vivo_database(self, conn, dbname):
        try:

            # Create a cursor object
            cursorObject = conn.cursor()

            # Create database harvester
            createDBQuery = "CREATE Database " + dbname + ";"

            cursorObject.execute(createDBQuery)

        except Exception as e:

            print("Exeception occured:{}".format(e))

        finally:

            conn.close()

    def create_vivo_table(self, conn, tablename):
        try:

            if tablename == "users":

                createTableQuery = "CREATE TABLE `users`" \
                    "(" \
                    "`pid` varchar(20) NOT NULL," \
                    "`eid` varchar(20) NOT NULL," \
                    "`uid` varchar(20)," \
                    "`public` varchar(20)  NOT NULL DEFAULT 'N'," \
                    "`keyword` LONGTEXT," \
                    "`update_date` DATE DEFAULT NULL," \
                    "PRIMARY KEY ( pid )" \
                    ");"
            elif tablename == "publications":

                createTableQuery = "CREATE TABLE `publications` (" \
                    "`pid` varchar(20) NOT NULL," \
                    "`keyword` LONGTEXT," \
                    "`public` varchar(20) NOT NULL DEFAULT 'N'," \
                    "`update_date` DATE DEFAULT NULL," \
                    "PRIMARY KEY (`pid`)" \
                    ");"

            elif tablename == "relations":

                createTableQuery = "CREATE TABLE `relations` (" \
                    "`rid` varchar(20) NOT NULL," \
                    "`public` varchar(20) NOT NULL DEFAULT 'N'," \
                    "`update_date` DATE DEFAULT NULL," \
                    "PRIMARY KEY (`rid`)" \
                    ");"

            cursorObject = conn.cursor()
            cursorObject.execute(createTableQuery)

        except Exception as e:

            print("Exeception occured:{}".format(e))

    def execute_query(self, conn, querystring, querytype):
        try:

            cursorObject = conn.cursor()
            cursorObject.execute(querystring)

            if querytype == "select":

                rows = cursorObject.fetchall()
                return rows

            elif querytype == "update":

                conn.commit()

        except Exception as e:

            print("Exeception occured:{}".format(e))

    def check_exist(self, conn, tablename, keyname, value):

        isExist = False

        try:
            querystring = "SELECT * from " + tablename + \
                " where " + keyname + " = \"" + value + "\";"

            cursorObject = conn.cursor()
            cursorObject.execute(querystring)
            rows = cursorObject.fetchall()

            for row in rows:
                isExist = True

        except Exception as e:

            print("MySQL Exeception occured:{}".format(e))

        return isExist

    def select_records(self, conn, tablename, keyname, value):

        try:
            querystring = "SELECT * from " + tablename + \
                " where " + keyname + " = \"" + value + "\";"

            cursorObject = conn.cursor()
            cursorObject.execute(querystring)
            rows = cursorObject.fetchall()

            return rows

        except Exception as e:

            print("MySQL Exeception occured:{}".format(e))

        return None

    def delete_record(self, conn, tablename, keyname, value):

        resp = False

        try:
            querystring = "DELETE from %s where %s = %s" % (
                tablename, keyname, value,)
            print(querystring)

            cursorObject = conn.cursor()
            cursorObject.execute(querystring)
            conn.commit()

            resp = True

        except Exception as e:

            print("MySQL Exeception occured:{}".format(e))

        return resp

    def update_user_privacy(self, conn, tablename, privacy, keyname, value):

        resp = False

        try:
            querystring = "UPDATE %s set public = \"%s\" where %s = \"%s\";" % (
                tablename, privacy, keyname, value,)
            print(querystring)
            cursorObject = conn.cursor()
            cursorObject.execute(querystring)
            conn.commit()

            resp = True

        except Exception as e:

            print("MySQL Exeception occured:{}".format(e))

        return resp

    def insert_user(self, conn, username, elementid, uid, privacy):

        resp = False

        try:
            querystring = "INSERT INTO users (pid, eid, uid, public) VALUES (\"%s\", \"%s\", \"%s\", \"%s\");" % (
                username, elementid, uid, privacy,)

            cursorObject = conn.cursor()
            cursorObject.execute(querystring)
            conn.commit()

            resp = True

        except Exception as e:

            print("MySQL Exeception occured:{}".format(e))

        return resp

    def insert_publication(self, conn, pubid, privacy):

        resp = False

        try:

            querystring = "INSERT INTO publications (pid, public) VALUES (\"%s\", \"%s\");" % (
                pubid, privacy,)

            cursorObject = conn.cursor()
            cursorObject.execute(querystring)
            conn.commit()

            resp = True

        except Exception as e:

            print("MySQL Exeception occured:{}".format(e))

        return resp

    def insert_relation(self, conn, rid, privacy):

        resp = False

        try:

            querystring = "INSERT INTO relations (rid, public) VALUES (\"%s\", \"%s\");" % (
                rid, privacy,)

            cursorObject = conn.cursor()
            cursorObject.execute(querystring)
            conn.commit()

            resp = True

        except Exception as e:

            print("MySQL Exeception occured:{}".format(e))

        return resp
