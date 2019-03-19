# -*- coding: utf-8 -*-
import datetime

from pyzure.connection.connection import connect
from pyzure.create import existing_test
from pyzure import create
from pyzure.execute import execute_query
import concurrent.futures

from pyzure.send.common import cleaning_function, commit_function, get_table_info, create_table_from_info, \
    print_progress_bar_multi_threads
from pyzure.tools.print_colors import C
from pyzure.tools.read_and_write import write_in_file, read_file


def send_to_azure_from_one_thread(x):
    d = datetime.datetime.now()
    send_to_azure(x["instance"], x["data"], x["thread_number"], x["sub_commit"], x["table_info"], x["nb_threads"])
    return (datetime.datetime.now() - d).seconds


def create_a_batch(rows, batch_size, i):
    return rows[batch_size * i:batch_size * (i + 1)]


def send_to_azure_multi_threads(instance, data, nb_threads=4, replace=True, types=None, primary_key=(),
                                sub_commit=False):
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
    table_name = data["table_name"]
    columns_name = data["columns_name"]
    rows = data["rows"]
    total_len_data = len(rows)

    # Create table if needed
    if not existing_test(instance, table_name) or (types is not None) or (primary_key != ()):
        create.create_table(instance, data, primary_key, types)

    # Clean table if needed
    if replace:
        cleaning_function(instance, table_name)

    # Define batch size
    batch_size = int(total_len_data / nb_threads) + 1
    if total_len_data < nb_threads:
        batch_size = 1

    # Get table info
    table_info = get_table_info(instance, table_name)

    # Split data in batches of batch_size length
    split_data = []

    # global threads_state
    # threads_state = {}

    for i in range(nb_threads):
        batch = create_a_batch(rows, batch_size, i)
        split_data.append(
            {
                "data":
                    {
                        "table_name": table_name,
                        "columns_name": columns_name,
                        "rows": batch
                    },
                "instance": instance,
                "thread_number": i,
                "nb_threads": nb_threads,
                "sub_commit": sub_commit,
                "table_info": table_info,
            }
        )
        write_in_file("threads_state_%s" % str(i), str({
            "iteration": 0,
            "total": len(batch)
        }))

    with concurrent.futures.ProcessPoolExecutor() as executor:
        r = list(executor.map(send_to_azure_from_one_thread, split_data))

    print()
    for num_thread in range(nb_threads):
        insert_query = "INSERT INTO %s SELECT * FROM %s" % (table_name, table_name + "_" + str(num_thread))
        print(insert_query)
        execute_query(instance, insert_query)

    for num_thread in range(nb_threads):
        sub_table = table_name + "_" + str(num_thread)
        print(C.HEADER + "DROP TABLE %s..." % sub_table + C.ENDC)
        execute_query(instance, "DROP TABLE %s" % sub_table)
        print(C.HEADER + "DROP TABLE %s...OK" % sub_table + C.ENDC)

    total_length_data = 0
    for element in split_data:
        total_length_data = total_length_data + len(element["data"]["rows"])

    for i in range(len(r)):
        print("Thread %s : %s seconds" % (str(i), str(r[i])))

    print("Total rows: %s" % str(total_length_data))
    print(C.BOLD + "Total time in seconds : %s" % str((datetime.datetime.now() - start).seconds) + C.ENDC)
    return 0


def send_to_azure(instance, data, thread_number, sub_commit, table_info, nb_threads):
    """
    data = {
        "table_name" 	: 'name_of_the_azure_schema' + '.' + 'name_of_the_azure_table' #Must already exist,
        "columns_name" 	: [first_column_name,second_column_name,...,last_column_name],
        "rows"		: [[first_raw_value,second_raw_value,...,last_raw_value],...]
    }
    """

    rows = data["rows"]
    if not rows:
        return 0
    columns_name = data["columns_name"]
    table_name = data["table_name"] + "_" + str(thread_number)

    print(C.HEADER + "Create table %s..." % table_name + C.ENDC)
    create_table_from_info(instance, table_info, table_name)
    print(C.OKGREEN + "Create table %s...OK" % table_name + C.ENDC)
    small_batch_size = int(2099 / len(columns_name))

    cnxn = connect(instance)
    cursor = cnxn.cursor()

    # Initialize counters
    boolean = True
    total_rows = len(rows)
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
        # percent = round(float(counter * 100) / total_rows)
        threads_state = eval(read_file("threads_state_%s" % str(thread_number)))
        threads_state["iteration"] = counter
        write_in_file("threads_state_%s" % str(thread_number), str(threads_state))

        # print(threads_state)
        if sub_commit:
            suffix = "rows sent"
            # print("Thread %s : %s %% rows sent" % (str(thread_number), str(percent)))
        else:
            suffix = "rows prepared to be sent"
        print_progress_bar_multi_threads(nb_threads, suffix=suffix)
        # print("Thread %s : %s %% rows prepared to be sent" % (str(thread_number), str(percent)))
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
    return 0


def test_multi_threads():
    data = {
        "table_name": 'testaz.test2',
        "columns_name": ["nom", "prenom", "age", "date"],
        "rows": [["pif", "pif", 12, "2017-02-23"] for v in range(100000)]
    }
    send_to_azure_multi_threads(
        "MH_TEST",
        data,
        replace=True,
        nb_threads=4,
        sub_commit=False
    )
