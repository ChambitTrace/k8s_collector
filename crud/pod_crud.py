import uuid
import psycopg2
from db.database import get_db_connection, release_db_connection

def create_pod(p_name, p_nid, p_nsid, p_sid, p_created_at):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Convert all UUIDs to strings before using them in SQL parameters
        p_nid_str = str(p_nid)
        p_nsid_str = str(p_nsid)
        # p_created_at is already a Unix timestamp integer
        p_created_at_ts = p_created_at
        # Check foreign key existence for p_nid in t_node(n_id)
        cur.execute("SELECT 1 FROM t_node WHERE n_id = %s", (p_nid_str,))
        if cur.fetchone() is None:
            raise ValueError(f"Node ID {p_nid} does not exist in t_node.")
        # Check foreign key existence for p_nsid in t_namespace(ns_id)
        cur.execute("SELECT 1 FROM t_namespace WHERE ns_id = %s", (p_nsid_str,))
        if cur.fetchone() is None:
            raise ValueError(f"Namespace ID {p_nsid} does not exist in t_namespace.")

        # p_sid is optional; check if it exists in t_sbom, else set to None
        if p_sid is not None:
            p_sid_str = str(p_sid)
            cur.execute("SELECT 1 FROM t_sbom WHERE s_id = %s", (p_sid_str,))
            if cur.fetchone() is None:
                p_sid_str = None
        else:
            p_sid_str = None

        p_id = str(uuid.uuid4())
        cur.execute(
            "INSERT INTO t_pod (p_id, p_name, p_nid, p_nsid, p_sid, p_created_at) VALUES (%s, %s, %s, %s, %s, %s)",
            (p_id, p_name, p_nid_str, p_nsid_str, p_sid_str, p_created_at_ts)
        )
        conn.commit()
        cur.close()
        print(f"[+] Pod '{p_name}' inserted into DB.")
    except (Exception, psycopg2.DatabaseError) as error:
        if conn:
            conn.rollback()
        print(error)
    finally:
        if conn is not None:
            release_db_connection(conn)

def update_pod(p_name):
    # Note: This is a placeholder. A real implementation would need to decide
    # what fields of the pod to update.
    print(f"[~] Pod '{p_name}' update event received.")

def delete_pod(p_name, p_nsid):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM t_pod WHERE p_name = %s AND p_nsid = %s", (p_name, p_nsid))
        conn.commit()
        cur.close()
        print(f"[-] Pod '{p_name}' deleted from DB.")
    except (Exception, psycopg2.DatabaseError) as error:
        if conn:
            conn.rollback()
        print(error)
    finally:
        if conn is not None:
            release_db_connection(conn)
