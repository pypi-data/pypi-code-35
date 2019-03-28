import sqlite3
from sqlite3 import Error


class Model:

    conn:    object
    cursor:     object
    table:    str
    db_name   =   "db_inmap"

    def __init__(self):
        """
        alwase we have just one connection to create
        and if we have already we get it, so:
        in try block we try to get a connection if we have, if not we create it
        """
        try:
            # if we have already a connection
            self.cursor = Model.conn.cursor()
        except AttributeError:
            # else we create a connection
            self.__db_connect()


    def _create_table(self, table_query):
        """
        We create the table ports, and the hosts tables
        :return:
        """
        try:
            self.cursor.execute(table_query)

        except Error as e:
            print(e)

    def _select(self, kwargs):

        query = 'SELECT * FROM ' + self.table
        results = self.__query_select(query, **kwargs)
        results = self.__filter_resutls(results)

        if len(results) == 1:
            return results[0]

        return results

    def _get_id(self, **kwargs):

        query = "SELECT id FROM " + self.table
        result = self.__query_select(query, **kwargs)

        return result

    def _insert_line(self, query, line):
        """
        insert a single line : port, proto, state, service, version
        but if we execute the scan_ports the line is like : port, proto, state, service

        :return:
        """
        # check if we have this line
        self.cursor.execute(query, line)
        Model.conn.commit()

        return self.cursor.lastrowid

    def _insert_lines(self, query, lines):

        for line in lines:
            self.cursor.execute(query, line)

        Model.conn.commit()

        return self.cursor.lastrowid

    def _update_line(self, line):

        self.cursor.execute(self.sql_update_line, line)
        Model.conn.commit()

    def _delete_lines(self):

        self.cursor.execute(self.sql_delete_lines)
        Model.conn.commit()

    def _db_close(self):
        Model.conn.close()

    #def _db_clear(self):
    #    query = 'DELETE FROM ' + self.table
    #    self.__query_select(query)
    #
    #    query = 'VACUUM'
    #    self.__query_select(query)



    # Private method
    def __query_select(self, query, **kwargs):

        # if we have condition for where
        if len(kwargs) > 0:
            query += ' WHERE '
            for key, value in kwargs.items():
                query += key + '=' + '"' + str(value) + '"' + ' AND '

            index = query.index('AND', len(query) - 4)  # 4 == len('AND') + 1
            query = query[0:index]

        try:
            results = self.cursor.execute(query).fetchall()
        except sqlite3.OperationalError as e:
            print(str(e).replace('column', 'argument'))
            print("The parameters are:")
            print(self.arguments)
            return 0

        return results

    def __filter_resutls(self, results):
        """
        the resutls output is a tuple that contain the id, for removing the id column we copy all results int a new list
        :param results:
        :return:
        """
        l_results = []

        i = 0
        for result in results:
            l_results.append({})

            j = 0
            for field in result:
                if j == 0:
                    j += 1
                    continue

                l_results[i][self.arguments[j-1]] = field
                j += 1

            i += 1

        return l_results

    def __db_connect(self):
        """
        Connect or Create a new database
        :return:
        """
        try:
            Model.conn = sqlite3.connect(self.db_name)
            self.cursor = Model.conn.cursor()
        except Error as e:
            print(e)
