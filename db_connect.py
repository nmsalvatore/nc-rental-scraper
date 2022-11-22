import os
import psycopg2
import dotenv

dotenv.load_dotenv()

def connect():
    conn = psycopg2.connect(
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
<<<<<<< HEAD
    )
    return conn
=======
        password=os.environ['DB_PASSWORD'],
        host='localhost'
    )
    return conn
>>>>>>> update
