import psycopg2
from db.database import get_db_connection, release_db_connection

def get_node_id_by_name(node_name):
    """Get node ID from the database by node name."""
    conn = None
    node_id = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT n_id FROM t_node WHERE n_name = %s", (node_name,))
        result = cur.fetchone()
        if result:
            node_id = result[0]
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        if conn:
            conn.rollback()
        print(f"Error getting node ID for {node_name}: {error}")
    finally:
        if conn is not None:
            release_db_connection(conn)
    return node_id

def get_namespace_id_by_name(namespace_name):
    """Get namespace ID from the database by namespace name."""
    conn = None
    namespace_id = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT ns_id FROM t_namespace WHERE ns_name = %s", (namespace_name,))
        result = cur.fetchone()
        if result:
            namespace_id = result[0]
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        if conn:
            conn.rollback()
        print(f"Error getting namespace ID for {namespace_name}: {error}")
    finally:
        if conn is not None:
            release_db_connection(conn)
    return namespace_id
