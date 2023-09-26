import os
import psycopg2
import sys

from fastchat.utils import build_logger

logger = build_logger("db", "db.log")

PGSQL_HOST = os.environ["PGSQL_HOST"]
PQSQL_PORT = os.environ["PGSQL_PORT"]
PGSQL_USER = os.environ["PGSQL_USER"]
PGSQL_PASSWORD = os.environ["PGSQL_PASSWORD"]
PGSQL_DBNAME = os.environ["PGSQL_DBNAME"]

def write_qa_to_db(question, answer, model, user="default_user", pair_id="0", reaction="no reaction", table_name=PGSQL_DBNAME):
    
    try:
        conn = psycopg2.connect(host=PGSQL_HOST, port=PQSQL_PORT, database=PGSQL_DBNAME, user=PGSQL_USER, password=PGSQL_PASSWORD)
        logger.info(f"Successfully connected to the database: {PGSQL_DBNAME}")
    except (psycopg2.OperationalError, psycopg2.Error) as e:
        logger.info(f"Error connecting to the database: {PGSQL_DBNAME} ", str(e))
        return
    
    if is_table_exist(conn, table_name):
        logger.info(f"table {table_name} olready exists")
    else:
        success = create_table(conn, table_name)
        if not success:
            return
    insert_data(conn, table_name, question, answer, model, user, pair_id, reaction)

    conn.close()

def is_table_exist(conn, table_name):
    table_exist_sql = f"""
    SELECT tablename 
    FROM pg_catalog.pg_tables 
    WHERE schemaname='public' AND tablename='{table_name}'
    """

    with conn.cursor() as cursor:
        cursor.execute(table_exist_sql)
        table_exist = cursor.fetchone()
    return True if table_exist else False    

def create_table(conn, table_name):
    create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            questions TEXT NOT NULL,
            answers TEXT NOT NULL,
            model TEXT NOT NULL,
            user_name TEXT NOT NULL,
            pair_id TEXT NOT NULL,
            reaction TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(create_table_sql)
        conn.commit()
        logger.info(f"Table {table_name} created successfully!")
        return True
    except Exception as e:
         logger.info(f"Error creating table {table_name}: ", str(e))
         return False
        
def insert_data(conn, table_name, question, answer, model, user, pair_id, reaction):
    insert_sql = f"INSERT INTO {table_name} (questions, answers, model, user_name, pair_id, reaction) VALUES (%s, %s, %s, %s, %s, %s)"
    try:
        with conn.cursor() as cursor:
            cursor.execute(insert_sql, (question, answer, model, user, pair_id, reaction))

        conn.commit()
        logger.info("Data inserted successfully!")
    except Exception as e:
        logger.info("Error inserting data: ", str(e))
        
def init_db(database):
    try:
        conn = psycopg2.connect(host=PGSQL_HOST, port=PQSQL_PORT, database="postgres", user=PGSQL_USER, password=PGSQL_PASSWORD)
        logger.info("Successfully connected to the default database.")
    except (psycopg2.OperationalError, psycopg2.Error) as e:
        logger.info("Error connecting to the default database: ", str(e))
        return

    conn.autocommit = True 
    db_query = f"SELECT datname FROM pg_database WHERE datname = '{database}';"   
    create_db_query = f"CREATE DATABASE {database}"
    with conn.cursor() as cursor:
        cursor.execute(db_query)
        result = cursor.fetchone()
        if result:
            logger.info(f"Database '{database}' exists.")
        else:
            cursor.execute(create_db_query)
            logger.info(f"Database '{database}' created successfully!")

    conn.close()

if __name__ == "__main__":
    init_db(PGSQL_DBNAME)
    write_qa_to_db("What is your name?", "My name is OSS-Compass-Chat", "DB_TEST_NO_MODEL")
