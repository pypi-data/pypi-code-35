def list_available_mysql_tables(spark=SP_CONTEXT, url=MYSQL_URL, driver=MYSQL_DRIVER, user=MYSQL_USER, password=MYSQL_PASSWORD,
                                ssl_ca=MYSQL_SSL_CA_PATH, queryTimeout=MYSQL_QUERY_TIMEOUT):
    """
    Method allows to list all the tables that available to a particular user.
    Returnws Spark DataFrame as a result
    """
    table_name = "(SELECT table_name FROM information_schema.tables WHERE table_type = 'base table') AS t"
    return read_mysql(table_name, spark=spark, url=MYSQL_URL, driver=MYSQL_DRIVER, user=MYSQL_USER, password=MYSQL_PASSWORD,
                      ssl_ca=MYSQL_SSL_CA_PATH, queryTimeout=MYSQL_QUERY_TIMEOUT)


def read_mysql(table_name, spark=SP_CONTEXT, url=MYSQL_URL, driver=MYSQL_DRIVER, user=MYSQL_USER, password=MYSQL_PASSWORD,
               ssl_ca=MYSQL_SSL_CA_PATH, queryTimeout=MYSQL_QUERY_TIMEOUT):
    """
    Method allows fetch the table, or a query as a Spark DataFrame.
    Returnws Spark DataFrame as a result.

    # Example usage:
      read_mysql(table_name=customers)
      read_mysql(table_name=h2.customers)
      read_mysql(table_name=h2.customers, url=MYSQL_URL, driver=MYSQL_DRIVER, user=MYSQL_USER, password=MYSQL_PASSWORD, ssl_ca=MYSQL_SSL_CA_PATH, queryTimeout=MYSQL_QUERY_TIMEOUT)
    """
    return spark.read.format('jdbc').options(
        url=url,
        driver=driver,
        dbtable=table_name,
        user=user,
        password=password,
        ssl_ca=ssl_ca,
        queryTimeout=queryTimeout
    ).load()


def remove_columns(p_spark_dataframe, p_columns_to_remove_csv="", delimiter=";"):
    """
    remove_columns() method removes columns from a specified dataframe.
    It will silently return a result even if user specifies column that doesn't exist.
    Usage example: destination_df = remove_columns(source_df, "SequenceNumber;Body;Non-existng-column")
    """
    for column in p_columns_to_remove_csv.split(delimiter):
        p_spark_dataframe = p_spark_dataframe.drop(column)

    return p_spark_dataframe


def write_data_mysql(p_spark_dataframe, p_mysql_dbtable, spark=SP_CONTEXT, p_num_partitions=-1, url=MYSQL_URL, driver=MYSQL_DRIVER,
                     user=MYSQL_USER, password=MYSQL_PASSWORD, ssl_ca=MYSQL_SSL_CA_PATH,
                     queryTimeout=MYSQL_QUERY_TIMEOUT):
    """
    Method writes data into MySQL and takes care of repartitioning in case if it's necessary.

    Dependencies:
      1. MySQL connector Java 8_0_13
      dbfs:/FileStore/jars/7b863f06_67cf_4a51_8f3b_67d414d808b3-Barnymysql_connector_java_8_0_13_4ac45-2f7c7.jar

      http://dev.mysql.com/doc/connector-j/en/
      https://mvnrepository.com/artifact/mysql/mysql-connector-java

    By default, it relies on constant variables outside of method that define MySQL credentials, that can be also specified as a parameters:
        * MYSQL_URL
        * MYSQL_DRIVER
        * MYSQL_USER
        * MYSQL_PASSWORD
        * MYSQL_SSL_CA_PATH
        * MYSQL_QUERY_TIMEOUT

    Method Parameters:
       * p_spark_dataframe - dataframe to write
       * p_mysql_db_name - name of database to write to
       * p_mysql_table_name - name of table to write to
       * p_num_partitions - amount of partitions, if -1, runs with default amount of partitions defined in spark environment or specific delta

   Method default parameters:
        p_num_partitions=-1
        url=MYSQL_URL,
        driver=MYSQL_DRIVER,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        ssl_ca=MYSQL_SSL_CA_PATH,
        queryTimeout=MYSQL_QUERY_TIMEOUT

   Usage example:
      #MySQL settings defined outside of a method below:
      MYSQL_DRIVER = "com.mysql.jdbc.Driver"
      MYSQL_URL = "jdbc:mysql://hostname:port/database?useUnicode=true&characterEncoding=utf-8&useJDBCCompliantTimezoneShift=true&useLegacyDatetimeCode=false"
      MYSQL_QUERY_TIMEOUT = 0

      MYSQL_USER = "user@namespace"
      MYSQL_PASSWORD = "example_password"
      MYSQL_SSL_CA_PATH = "/mnt/alex-experiments-blob/certs/cert.txt"

      #Method execution itself
      write_data_mysql(p_spark_dataframe=target_data, p_mysql_dbtable=destination_db_name_column_name_construct)

    """

    # Casting amount of partitions
    p_num_partitions = int(p_num_partitions)

    # Repartition if necessary
    if p_num_partitions > 0:
        p_spark_dataframe = p_spark_dataframe.repartition(p_num_partitions)
    # Writing data to MySQL
    p_spark_dataframe.write.format('jdbc').options(
        url=MYSQL_URL,
        driver=MYSQL_DRIVER,
        dbtable=p_mysql_dbtable,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        ssl_ca=MYSQL_SSL_CA_PATH,
        queryTimeout=MYSQL_QUERY_TIMEOUT
    ).mode('append').save()

    return True


def delta_write_safe(sp_df_to_write, SP_CONTEXT, DATABRICKS_TABLE_NAME):
    """
    :param sp_df_to_write:
    :param SP_CONTEXT:
    :param DATABRICKS_TABLE_NAME:
    :return:

    Sample usage:
        #!/usr/bin/env python

        from sparksafedelta import sparksafedelta
        sparksafedelta.delta_write_safe(sp_df_to_write, SP_CONTEXT, DATABRICKS_TABLE_NAME)
    """
    missing_columns = __get_missing_columns(sp_df_to_write, SP_CONTEXT, DATABRICKS_TABLE_NAME)
    if missing_columns:
        __implement_missing_columns(missing_columns, SP_CONTEXT, DATABRICKS_TABLE_NAME)
    sp_df_to_write.write.insertInto(DATABRICKS_TABLE_NAME)
    return True
    
def __get_missing_columns(sp_df_to_insert, SP_CONTEXT, DATABRICKS_TABLE_NAME):
    existing_table = SP_CONTEXT.sql("SELECT * FROM " + DATABRICKS_TABLE_NAME)
    existing_columns = set(existing_table.columns)
    new_columns = set(sp_df_to_insert.columns)
    returnable = list(set.difference(new_columns, existing_columns))

    if len(returnable) == 0:
        return False
    else:
        return returnable
      
def __implement_missing_columns(missing_column_list, SP_CONTEXT, DATABRICKS_TABLE_NAME):
    for column in missing_column_list:
        SP_CONTEXT.sql("ALTER TABLE " + DATABRICKS_TABLE_NAME + " ADD COLUMNS (" + column + " STRING)")