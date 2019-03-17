def delta_write_safe(sp_df_to_write, SP_CONTEXT, DATABRICKS_TABLE_NAME):
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