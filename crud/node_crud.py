import uuid
import psycopg2
from db.database import get_db_connection, release_db_connection

def create_node(n_cid, n_name, n_zone, n_created_at):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        n_id = uuid.uuid4()
        created_at_ts = int(n_created_at.timestamp())
        cur.execute(
            "INSERT INTO t_node (n_id, n_cid, n_name, n_zone, n_created_at) VALUES (%s, %s, %s, %s, %s)",
            (n_id, n_cid, n_name, n_zone, created_at_ts)
        )
        conn.commit()
        cur.close()
        print(f"[+] Node '{n_name}' inserted into DB.")
    except (Exception, psycopg2.DatabaseError) as error:
        if conn:
            conn.rollback()
        print(error)
    finally:
        if conn is not None:
            release_db_connection(conn)

def update_node(n_name, n_zone):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE t_node SET n_zone = %s WHERE n_name = %s",
            (n_zone, n_name)
        )
        conn.commit()
        cur.close()
        print(f"[~] Node '{n_name}' updated in DB.")
    except (Exception, psycopg2.DatabaseError) as error:
        if conn:
            conn.rollback()
        print(error)
    finally:
        if conn is not None:
            release_db_connection(conn)

def delete_node(n_name):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM t_node WHERE n_name = %s", (n_name,))
        conn.commit()
        cur.close()
        print(f"[-] Node '{n_name}' deleted from DB.")
    except (Exception, psycopg2.DatabaseError) as error:
        if conn:
            conn.rollback()
        print(error)
    finally:
        if conn is not None:
            release_db_connection(conn)
