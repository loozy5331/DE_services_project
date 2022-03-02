import os

import psycopg2 as pg
from dotenv import load_dotenv

load_dotenv()
DB_HOST = os.environ.get("DB_HOST")
DB_USER_NAME = os.environ.get("DB_USER_NAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_PORT = os.environ.get("DB_PORT")

def get_connector():
    conn = pg.connect(host=DB_HOST, 
                        port=DB_PORT, 
                        user=DB_USER_NAME, 
                        password=DB_PASSWORD)
    conn.autocommit = True

    return conn