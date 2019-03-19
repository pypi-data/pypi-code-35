import pyodbc

import os

import sshtunnel
from sshtunnel import SSHTunnelForwarder

from pyzure.connection.azure_credentials import credential


def execute_query(instance, query, data=None, commit=True, cursor=None, cnxn=None, create_schema=False):
    if not cnxn and not cursor:
        connection_kwargs = credential(instance)

        # Create an SSH tunnel
        ssh_host = os.environ.get("SSH_%s_HOST" % instance)
        ssh_user = os.environ.get("SSH_%s_USER" % instance)
        ssh_path_private_key = os.environ.get("SSH_%s_PATH_PRIVATE_KEY" % instance)
        if ssh_host:
            tunnel = SSHTunnelForwarder(
                (ssh_host, 22),
                ssh_username=ssh_user,
                ssh_private_key=ssh_path_private_key,
                remote_bind_address=(
                    os.environ.get("AZURE_%s_HOST" % instance), int(os.environ.get("AZURE_%s_PORT" % instance))),
                local_bind_address=('localhost', 1433),  # could be any available port
            )
            # Start the tunnel
            try:
                tunnel.start()
                print("Tunnel opened!")
            except sshtunnel.HandlerSSHTunnelForwarderError:
                pass

            connection_kwargs["server"] = "127.0.0.1,1433"
            connection_kwargs["port"] = 1433
        cnxn = pyodbc.connect(**connection_kwargs)

        cursor = cnxn.cursor()

    if data:
        try:
            cursor.execute(query, data)
        except Exception as e:
            if ssh_host:
                tunnel.close()
            print("Error:" + str(e))
            raise
        if commit:
            cnxn.commit()
        result = None
    elif create_schema:
        try:
            cursor.execute(query)
        except Exception as e:
            if ssh_host:
                tunnel.close()
            print("Error:" + str(e))
            raise
        cnxn.commit()
        result = None
    else:
        try:
            cursor.execute(query)
        except Exception as e:
            if ssh_host:
                tunnel.close()
            print("Error:" + str(e))
            raise
        result = []
        try:
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                dict_ = dict()
                for i in range(len(columns)):
                    dict_[columns[i]] = row[i]
                result.append(dict_)
        except pyodbc.ProgrammingError:
            pass
        except TypeError:
            cnxn.commit()
            return []
        cnxn.commit()

    if commit:
        cursor.close()
        cnxn.close()
        if ssh_host:
            tunnel.close()
            print("Tunnel closed!")
        return result
    else:
        return result, cursor, cnxn
