import os
import psycopg
from psycopg import OperationalError, Connection


def connect_to_db():
    credentional_to_connect_db = {
        "host": os.getenv("DB_HOST"),
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASS"),
        "port": int(os.getenv("DB_PORT")),
    }

    try:
        connection = psycopg.connect(**credentional_to_connect_db)
        return connection
    except OperationalError as e:
        print(f"Error to connect database {e}")
        return None


def create_tables(connect: Connection):
    drop_tables = """
    DROP TABLE IF EXISTS users;
    DROP TABLE IF EXISTS tasks;
    """
    users_table = """
    CREATE TABLE users(
        user_id SERIAL PRIMARY KEY
    );
    
    """
    task_table = """
    CREATE TABLE tasks(
    task_id UUID PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    description VARCHAR(500),
    status VARCHAR(20) NOT NULL,
    creation_date TIMESTAMP WITH TIME ZONE NOT NULL,
    due_date TIMESTAMP WITH TIME ZONE,
    user_id INT NOT NULL,
    FOREIGN KEY(user_id)
    REFERENCES users(user_id)
    );
    """
    try:
        with connect.cursor() as cur:
            cur.execute(drop_tables)
            cur.execute(users_table)
            cur.execute(task_table)
        
        connect.commit()
    
    except Exception as e:
        print(f"Error during connection_table {e}")
        connect.rollback()
