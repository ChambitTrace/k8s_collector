import uuid
import psycopg2
from db.database import get_db_connection, release_db_connection

def create_namespace(ns_cid, ns_name, ns_created_at):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Check if namespace already exists for the cluster
        ns_cid_str = str(ns_cid)
        cur.execute(
            "SELECT ns_id, ns_created_at FROM t_namespace WHERE ns_name = %s AND ns_cid = %s",
            (ns_name, ns_cid_str)
        )
        row = cur.fetchone()
        if row is not None:
            # Already exists -> no insert
            print(f"[=] Namespace '{ns_name}' already exists for cluster {ns_cid}. Skipping insert.")
            cur.close()
            return
        # Insert if missing
        ns_id = uuid.uuid4()
        ns_id_str = str(ns_id)
        cur.execute(
            "INSERT INTO t_namespace (ns_id, ns_cid, ns_name, ns_created_at) VALUES (%s, %s, %s, %s)",
            (ns_id_str, ns_cid_str, ns_name, ns_created_at)
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

def update_namespace(ns_cid, ns_name, ns_created_at=None):
    """Update mutable fields of a namespace. Currently supports updating ns_created_at if provided.
    """
    if ns_created_at is None:
        print(f"[~] No updatable fields provided for namespace '{ns_name}'. Skipping update.")
        return
    ns_cid_str = str(ns_cid)
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE t_namespace SET ns_created_at = %s WHERE ns_name = %s AND ns_cid = %s",
            (ns_created_at, ns_name, ns_cid_str)
        )
        if cur.rowcount == 0:
            print(f"[!] Namespace '{ns_name}' for cluster {ns_cid} not found. No rows updated.")
        else:
            conn.commit()
            print(f"[~] Namespace '{ns_name}' updated.")
        cur.close()
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
