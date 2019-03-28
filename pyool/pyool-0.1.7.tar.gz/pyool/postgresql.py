import psycopg2 
import pandas as pd 
import csv 
import os 
import time 
from .logger_setting import logger 


# Defining PostgreSQL Database specific Class to work with

class PostgreSQLConnector: 
    def connect(self, db_name, host, port, user, password, retry_time = 0, buffering = 5):
        attempt = 0
        
        while attempt == 0 or attempt < retry_time:
            try: 
                logger.info("Connecting...") 
                self.connection  = psycopg2.connect(dbname = db_name
                                                    , host = host
                                                    , port = port
                                                    , user = user
                                                    , password = password) 
                logger.info("Connection established.")
                return True 

            except Exception as e:
                attempt += 1
                issue = e 
                message = "Attempt {}. {}. Retrying .....".format(attempt, issue)
                logger.error(message)
                time.sleep(buffering) 
                continue  

            raise RuntimeError("Can not access to PostgreSQL due to: {}".format(issue)) 



    def read_sql(self, file_path):
        with open(file_path, "r", encoding = "utf-8") as file:
            query  = file.read()

        return query 
    


    def extract_header(self, csv_file_path): 
        with open(csv_file_path, "r", newline = "") as file:
            reader = csv.reader(file)
            header = ",".join(next(reader))

        return header 



    def run_query(self, query, return_data = False, retry_time = 0, buffering = 5): 
        attempt = 0

        while attempt == 0 or attempt < retry_time:
            try: 
                cur = self.connection.cursor()
                cur.execute(query) 

                if return_data == True: 
                    data = cur.fetchall()
                    column_names = [desc[0] for desc in cur.description]
                    df = pd.DataFrame(data, columns = column_names) 
                    cur.close() 
                    logger.info("Data is returned")
                    return df 

                else: 
                    cur.close()
                    self.connection.commit()
                    logger.info("Query is executed")  
                    return True 

            except Exception as e: 
                attempt += 1
                issue = e 
                message = "Attempt {}. {}. Retrying .....".format(attempt, issue)
                logger.error(message)  
                time.sleep(buffering) 
                continue 
        
        self.connection.rollback() 
        raise RuntimeError("Cannot query from PostgreSQL server due to: {}".format(issue))
        
        


    def truncate(self, table):
        cur = self.connection.cursor()
        cur.execute("TRUNCATE TABLE %s" % (table)) 



    def uploadCsv(self, filepath, table, fields, truncate = False, remove_file = False): 
        if truncate == True: 
            self.truncate(table)
            logger.info("Table truncated. Start uploading...")

        cur = self.connection.cursor()

        try: 
            with open(filepath, 'r', encoding='utf-8') as f:
                sql = "COPY %s(%s) FROM STDIN WITH ( DELIMITER ',', FORMAT CSV, HEADER, ENCODING 'UTF8', FORCE_NULL(%s))" % (table, fields, fields) 
                cur.copy_expert(sql, f) 
                self.connection.commit()
            if remove_file == True:
                os.remove(filepath) 
            return True

        except Exception as e:
            issue = e 
            raise RuntimeError("Cannot upload to PostgreSQL server due to: {}".format(issue))



    def disconnect(self):
        state = self.connection.close() 
        logger.info("Connection closed.")
        return state 