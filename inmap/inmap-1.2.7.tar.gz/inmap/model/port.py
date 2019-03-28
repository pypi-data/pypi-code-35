from inmap.core.model import Model


class PortModel(Model):
    """
    Each class corresponds to a table in the database, the attributes are the fields
    """
    sql_table_port = """ CREATE TABLE IF NOT EXISTS port (
                        id integer PRIMARY KEY,
                        ip_address text,
                        port int,
                        proto text,
                        state text,
                        service text,
                        version text
                        
                        );
                    """

    sql_insert_line = ''' INSERT INTO port(ip_address, port, proto, state, service, version) VALUES
                         (:ip_address, :port, :proto, :state, :service, :version)'''
    sql_update_line = 'UPDATE port SET ip_address=:ip_address, port=:port, proto=:proto, state=:state, service=:service, version=:version WHERE id=:id'
    sql_delete_lines = 'DELETE FROM port'

    def __init__(self):
        """
        we create a port table, we use the protect method create_table
        :return:
        """
        self.table = 'port'
        self.arguments = ['ip_address', 'port', 'proto', 'state', 'service', 'version']
        super(PortModel, self).__init__()
        # if we don't create table before
        self._create_table(self.sql_table_port)

    def insert_line(self, **line):
        """
        insert a single line : port, proto, state, service, version
        :return:
        """
        # every single line can be found by port & proto
        row = self._get_id(ip_address=line['ip_address'], port=line['port'], proto=line['proto'])

        if len(row) > 0:
            line['id'] = row[0][0]
            self._update_line(line)
        else:
            self._insert_line(self.sql_insert_line, line)

    def insert_lines(self, lines, ip_address):
        """
        insert a lines : port, proto, state, service, version
        :return:
        """

        for line in lines:
            if not line:
                continue

            self.insert_line(
                ip_address = ip_address,
                port=line['port'],
                proto=line['proto'],
                state=line['state'],
                version=line['version'],
                service=line['service']
            )

    def select(self, **kwargs):

        return self._select(kwargs)

    #def clear(self):
    #    self._db_clear()