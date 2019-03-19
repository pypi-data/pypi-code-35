# -*- coding: utf-8 -*-
import datetime

import pyodbc
import os
import sshtunnel
from sshtunnel import SSHTunnelForwarder
from pyzure.connection.azure_credentials import credential
from pyzure.create import existing_test
from pyzure import create
from pyzure.send.common import cleaning_function, commit_function, print_progress_bar
from pyzure.tools.print_colors import C


def send_to_azure(instance, data, replace=True, types=None, primary_key=(), sub_commit=True):
    """
    data = {
        "table_name" 	: 'name_of_the_azure_schema' + '.' + 'name_of_the_azure_table' #Must already exist,
        "columns_name" 	: [first_column_name,second_column_name,...,last_column_name],
        "rows"		: [[first_raw_value,second_raw_value,...,last_raw_value],...]
    }
    """

    # Time initialization
    start = datetime.datetime.now()

    # Extract info
    rows = data["rows"]
    if not rows:
        return 0
    table_name = data["table_name"]
    columns_name = data["columns_name"]
    total_len_data = len(rows)

    # Create table if needed
    if not existing_test(instance, table_name) or (types is not None) or (primary_key != ()):
        create.create_table(instance, data, primary_key, types)

    # Clean table if needed
    if replace:
        cleaning_function(instance, table_name)

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

        connection_kwargs["host"] = "localhost,1433"
        connection_kwargs["port"] = 1433

    cnxn = pyodbc.connect(**connection_kwargs)
    cursor = cnxn.cursor()

    small_batch_size = int(2099 / len(columns_name))

    print("Initiate send_to_azure...")

    # Initialize counters
    boolean = True
    question_mark_pattern = "(%s)" % ",".join(["?" for i in range(len(rows[0]))])
    counter = 0
    while boolean:
        temp_row = []
        question_mark_list = []
        for i in range(small_batch_size):
            if rows:
                temp_row.append(rows.pop())
                question_mark_list.append(question_mark_pattern)
            else:
                boolean = False
                continue
        counter = counter + len(temp_row)
        # percent = round(float(counter * 100) / total_len_data)
        if sub_commit:
            suffix = "%% rows sent"
            print_progress_bar(counter, total_len_data, suffix=suffix)
            # print("%s %% rows sent" % str(percent))
        else:
            suffix = "% rows prepared to be sent"
            print_progress_bar(counter, total_len_data, suffix=suffix)
            # print("%s %% rows prepared to be sent" % str(percent))
        data_values_str = ','.join(question_mark_list)
        columns_name_str = ", ".join(columns_name)
        inserting_request = '''INSERT INTO %s (%s) VALUES %s ;''' % (table_name, columns_name_str, data_values_str)

        final_data = [y for x in temp_row for y in x]
        if final_data:
            cursor.execute(inserting_request, final_data)

        if sub_commit:
            commit_function(cnxn)
    if not sub_commit:
        commit_function(cnxn)
    cursor.close()
    cnxn.close()

    if ssh_host:
        tunnel.close()
        print("Tunnel closed!")

    print("data sent to azure")
    print("Total rows: %s" % str(total_len_data))
    print(C.BOLD + "Total time in seconds : %s" % str((datetime.datetime.now() - start).seconds) + C.ENDC)
    return 0


def test_unique_thread():
    data = {
        "table_name": 'testaz.test2',
        "columns_name": ["nom", "prenom", "age", "date"],
        "rows": [["pif", "pif", 12, "2017-02-23"] for v in range(8000)]
    }
    send_to_azure(
        "MH_TEST",
        data,
        replace=True,
        sub_commit=False
    )
