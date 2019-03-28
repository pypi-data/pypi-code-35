from inmap.core import model


class HostModel(model.Model):
    """
    Each class corresponds to a table in the database, the attributes are the fields
    """
    sql_table_host = """ CREATE TABLE IF NOT EXISTS host (
                            id integer PRIMARY KEY,
                            ip_address  text,
                            mac_address text,
                            hostname    text,
                            os_family   text,
                            os_cpe      text, 
                            os_details  text, 
                            state       text,
                            device_type text,
                            info_host   text, 
                            info_cpe    text,
                            info_os     text,
                            network_distance    text
                            );
                            """

    sql_insert_line = ''' INSERT INTO host(ip_address, mac_address, hostname, os_family, os_cpe, os_details,
                                         state, device_type, info_host, info_cpe, info_os, network_distance) 
                                        VALUES(:ip_address, :mac_address, :hostname, :os_family, :os_cpe, :os_details, 
                                                :state, :device_type, :info_host, :info_cpe, :info_os, :network_distance) '''

    sql_update_line = '''UPDATE host SET ip_address=:ip_address, mac_address=:mac_address, hostname=:hostname, os_family=:os_family, 
                                       os_cpe=:os_cpe, os_details=:os_details, state=:state, device_type=:device_type, info_host=:info_host,
                                        info_cpe=:info_cpe, info_os=:info_os, network_distance=:network_distance WHERE id=:id'''

    sql_delete_lines = 'DELETE FROM host'

    def __init__(self):
        """
        we create a host table, we use the protect method create_table
        :return:
        """
        self.table = 'host'
        self.arguments = ['ip_address', 'mac_address', 'hostname', 'os_family', 'os_cpe', 'os_details',
                             'state', 'device_type', 'info_host', 'info_cpe', 'info_os', 'network_distance']
        super(HostModel, self).__init__()
        # if we don't create table before
        self._create_table(self.sql_table_host)

    def insert_line(self, **line):
        """
        insert a single line : port, proto, state, service, version
        :return:
        """
        # every single line can be found by ip_address
        # line[0] ip_address
        row = self._get_id(ip_address=line['ip_address'])

        if len(row) > 0:
            line['id'] = row[0][0]
            self._update_line(line)
        else:
            self._insert_line(self.sql_insert_line, line)

    def insert_lines(self, lines):
        """
        insert a lines : port, proto, state, service, version
        :return:
        """

        for line in lines:
            if not line:
                continue

            self.insert_line(
                ip_address=line['ip_address'],
                hostname=line['hostname'],
                mac_address=line['mac_address'],
                device_type=line['device_type'],
                os_family=line['os_family'],
                os_cpe=line['os_cpe'],
                os_details=line['os_details'],
                state=line['state'],
                info_host=str(line['service_info_host']),
                info_os=str(line['service_info_os']),
                info_cpe=str(line['service_info_cpe']),
                network_distance=line['network_distance'],
            )

    def select(self, **kwargs):

        return self._select(kwargs)

    def get_id(self, **kwargs):

        return self._get_id(**kwargs)

    #def clear(self):
    #    self._db_clear()