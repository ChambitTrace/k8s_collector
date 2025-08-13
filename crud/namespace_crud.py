import uuid
import psycopg2
from db.database import get_db_connection, release_db_connection

def create_namespace(ns_cid, ns_name, ns_created_at):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        ns_id = uuid.uuid4()
        cur.execute(
            "INSERT INTO t_namespace (ns_id, ns_cid, ns_name, ns_created_at) VALUES (%s, %s, %s, %s)",
            (ns_id, ns_cid, ns_name, ns_created_at)
        )
        conn.commit()
        cur.close()
        print(f"[+] Namespace '{ns_name}' inserted into DB.")
    except (Exception, psycopg2.DatabaseError) as error:
        if conn:
            conn.rollback()
        print(error)
    finally:
        if conn is not None:
            release_db_connection(conn)

def delete_namespace(ns_name):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM t_namespace WHERE ns_name = %s", (ns_name,))
        conn.commit()
        cur.close()
        print(f"[-] Namespace '{ns_name}' deleted from DB.")
    except (Exception, psycopg2.DatabaseError) as error:
        if conn:
            conn.rollback()
        print(error)
    finally:
        if conn is not None:
            release_db_connection(conn)
