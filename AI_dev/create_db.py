import os
import psycopg2


def create_db():
    '''
    db_config = {
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
    }
    '''

    db_config = {
        "dbname": "resume",
        "user": "postgresadm",
        "password": "3fnosUd8krVC",
        "host": "ep-autumn-recipe-a1i2wgsj.ap-southeast-1.pg.koyeb.app",
        "port": 5432
    }

    conn = psycopg2.connect(**db_config)
    conn.autocommit = True  # Enable autocommit for creating the database

    cursor = conn.cursor()
    cursor.execute(
        f"SELECT 1 FROM pg_database WHERE datname = '{os.getenv('DB_NAME')}';"
    )
    database_exists = cursor.fetchone()
    cursor.close()


    conn.close()

    db_config["dbname"] = "resume"
    conn = psycopg2.connect(**db_config)
    conn.autocommit = True

    cursor = conn.cursor()
    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    cursor.close()

    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS trans.embeddings (id serial PRIMARY KEY, doc_fragment text, embeddings vector(4096));"
    )
    cursor.close()

    print("Database setup completed.")

create_db()