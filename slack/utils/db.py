import os

import psycopg2 as pg
from dotenv import load_dotenv

load_dotenv()
LOCAL_HOST = os.environ.get("LOCAL_HOST")

USER_NAME = os.environ.get("DB_USER_NAME")
PASSWORD = os.environ.get("DB_PASSWORD")
PORT = os.environ.get("DB_PORT")

def get_connector():
    conn = pg.connect(host=LOCAL_HOST, 
                        port=PORT, 
                        user=USER_NAME, password=PASSWORD)
    conn.autocommit = True

    return conn