import psycopg2
import traceback

################################################################################

DDL_DB_USER_NAME="dcworker_db_user"
DDL_DB_NAME="dcworker_db"
DDL_DB_HOST="localhost"

################################################################################

WORKER_REGISTRATION_TABLE_NAME = "worker_registration"
WORKER_REGISTRATION_TABLE_COMMAND = """
CREATE TABLE IF NOT EXISTS {} (
    workder_uuid VARCHAR(255) PRIMARY KEY,
    passcode VARCHAR(255) NOT NULL,
    workdir TEXT NOT NULL,
    port INTEGER NOT NULL,
    gpu_uuid VARCHAR(255) NOT NULL
)
""".format(WORKER_REGISTRATION_TABLE_NAME)

WORKER_REGISTER_COMMAND = """
INSERT INTO {}(workder_uuid, passcode, workdir, port, gpu_uuid)
VALUES(%s, %s, %s, %s, %s);
""".format(WORKER_REGISTRATION_TABLE_NAME)

WORKER_QUERY_REGIDTRATION_COMMAND = """
SELECT workder_uuid, passcode, workdir, port, gpu_uuid FROM {};
""".format(WORKER_REGISTRATION_TABLE_NAME)

DATASET_TABLE_NAME = "datasets"
DATASET_TABLE_COMMAND = """
CREATE TABLE IF NOT EXISTS {} (
    dataset_name VARCHAR(255) PRIMARY KEY,
    local_path TEXT NOT NULL,
    dataset_persist INTEGER NOT NULL,
    dataset_ready INTEGER NOT NULL,
    refcount INTEGER NOT NULL
)
""".format(DATASET_TABLE_NAME)

DATASET_QUERY_ALL_COMMAND = """
SELECT dataset_name, local_path, dataset_persist, dataset_ready, refcount
FROM {};
""".format(DATASET_TABLE_NAME)

DATASET_QUERY_BY_DATASET_NAME_COMMAND = """
SELECT dataset_name, local_path, dataset_persist, dataset_ready, refcount
FROM {}
WHERE dataset_name = %s;
""".format(DATASET_TABLE_NAME)

DATASET_INSERT_COMMAND = """
INSERT INTO {}(dataset_name, local_path, dataset_persist, dataset_ready, refcount)
VALUES(%s, %s, %s, %s, %s);
""".format(DATASET_TABLE_NAME)

DATASET_TAKE_REFERENCE_COUNT_LOCK_COMMAND = """
SELECT refcount FROM {} WHERE dataset_name = %s FOR UPDATE;
""".format(DATASET_TABLE_NAME)

DATASET_GET_REFERENCE_AND_PERSIST_LOCK_COMMAND = """
SELECT refcount, dataset_persist FROM {} WHERE dataset_name = %s FOR UPDATE;
""".format(DATASET_TABLE_NAME)

DATASET_TAKE_REFERENCE_COUNT_COMMAND = """
UPDATE {} SET refcount = refcount + 1 WHERE dataset_name = %s;
""".format(DATASET_TABLE_NAME)

DATASET_DROP_REFERENCE_COUNT_COMMAND = """
UPDATE {} SET refcount = refcount - 1 WHERE dataset_name = %s;
""".format(DATASET_TABLE_NAME)

DATASET_SET_READY_LOCK_COMMAND = """
SELECT dataset_ready FROM {} WHERE dataset_name = %s FOR UPDATE;
""".format(DATASET_TABLE_NAME)

DATASET_SET_READY_COMMAND = """
UPDATE {} SET dataset_ready = 1 WHERE dataset_name = %s;
""".format(DATASET_TABLE_NAME)

DATASET_DELETE_COMMAND = """
DELETE FROM {} WHERE dataset_name = %s
""".format(DATASET_TABLE_NAME)

################################################################################

def connection():
    try:
        conn = psycopg2.connect(dbname=DDL_DB_NAME,
                                user=DDL_DB_USER_NAME,
                                password=DDL_DB_USER_NAME,
                                host=DDL_DB_HOST)

        return conn
    except psycopg2.Error as db_err:
        print("[DB::connection] [ERROR] {}".format(db_err))
        print(db_err.pgerror)
        return None

def disconnect(conn):
    conn.close()

def db_operation(operation):
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = connection()
            kwargs['conn'] = conn
            return operation(*args, **kwargs)
        except psycopg2.DatabaseError as db_err:
            print("[DB] [ERROR] DB Error: {}".format(db_err))
            return False, None

        except Exception as err:
            print("[DB] [ERROR] Unexpected Exception: {}".format(err))
            traceback.print_exc()
            return False, None
        finally:
            if conn is not None:
                disconnect(conn)
    return wrapper

################################################################################

@db_operation
def create_table(create_table_command, conn=None):
    assert(conn is not None)
    cur = conn.cursor()
    cur.execute(create_table_command)
    cur.close()
    conn.commit()
    return True, None

@db_operation
def table_exists(table_name, conn=None):
    assert(conn is not None)
    table_exists_command = "SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name='{}')".format(
                            table_name)

    cur = conn.cursor()
    cur.execute(table_exists_command)
    exists = cur.fetchone()[0]
    cur.close()
    return True, exists

@db_operation
def insert_table(insert_table_command, values=None, conn=None):
    assert(conn is not None)
    cur = conn.cursor()
    if values is not None:
        cur.execute(insert_table_command, values)
    else:
        cur.execute(insert_table_command)
    conn.commit()
    cur.close()
    return True, None

@db_operation
def update_table_sync(select_for_update_command, update_command, values, conn=None):
    assert(conn is not None)
    cur = conn.cursor()
    cur.execute(select_for_update_command, values)
    cur.execute(update_command, values)
    conn.commit()
    cur.close()
    return True, None

@db_operation
def query_from_table(query_command, conditions=None, conn=None):
    assert(conn is not None)
    data = []
    cur = conn.cursor()
    if conditions is not None:
        cur.execute(query_command, conditions)
    else:
        cur.execute(query_command)
    rows = cur.fetchall()
    for row in rows:
        data += [row]
    cur.close()
    return True, data

@db_operation
def delete_from_table(delete_command, values=None, conn=None):
    assert(conn is not None)
    cur = conn.cursor()
    if values is not None:
        cur.execute(delete_command, values)
    else:
        cur.execute(delete_command)
    rows_deleted_count = cur.rowcount
    conn.commit()
    cur.close()
    return True, rows_deleted_count

@db_operation
def drop_table(table_name, conn=None):
    assert(conn is not None)
    drop_table_command = "DROP TABLE \"{}\";".format(table_name)
    cur = conn.cursor()
    cur.execute(drop_table_command)
    conn.commit()
    cur.close()
    return True, None

@db_operation
def delete_dataset_sync(dataset_name, conn=None):
    assert(conn is not None)
    delete = False
    cur = conn.cursor()
    cur.execute(DATASET_GET_REFERENCE_AND_PERSIST_LOCK_COMMAND, (dataset_name,))
    first = cur.fetchone()
    if first is not None:
        current_refcount = int(first[0])
        persist = int(first[1])
        # if the ref here is 1 and not persist, then just the entry and
        # also delete the dataset.
        if current_refcount <= 1 and persist == 0:
            delete = True
            cur.execute(DATASET_DELETE_COMMAND, (dataset_name,))
        elif current_refcount > 1:
            # If there are more refcounts, just unref and exit.
            cur.execute(DATASET_DROP_REFERENCE_COUNT_COMMAND, (dataset_name,))
    else:
        # Something went wrong that we cannot find the dataset with the given
        # dataset_name. Bail out.
        pass

    conn.commit()
    cur.close()
    return True, delete