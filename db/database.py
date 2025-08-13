import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv

load_dotenv()

db_pool = None

def get_db_pool():
    global db_pool
    if db_pool is None:
        db_pool = psycopg2.pool.SimpleConnectionPool(
            1, 10,
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
    return db_pool

def get_db_connection():
    return get_db_pool().getconn()

def release_db_connection(conn):
    get_db_pool().putconn(conn)

def close_db_pool():
    global db_pool
    if db_pool is not None:
        db_pool.closeall()
        db_pool = None

def check_db_connection():
    """Check if the database connection is alive."""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT 1')
        cur.close()
        print("✅ 데이터베이스 연결 성공")
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"❌ 데이터베이스 연결 실패: {error}")
        return False
    finally:
        if conn is not None:
            release_db_connection(conn)
