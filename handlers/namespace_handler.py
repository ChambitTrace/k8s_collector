from kubernetes import client, config
import uuid
import os
from crud.namespace_crud import create_namespace, update_namespace, delete_namespace

# Use fixed cluster ID from env when provided; otherwise generate a string UUID
TEMP_CLUSTER_ID = os.getenv("CHAMBIT_CLUSTER_ID") or "7306424b-8bcc-5c65-bf07-d4ff12ea6f84"


def init_namespace_sync():
    """Sync all existing namespaces into DB at startup.
    Tries in-cluster config first, falls back to local kubeconfig.
    """
    try:
        try:
            # Prefer in-cluster when running inside Kubernetes
            config.load_incluster_config()
            print("[BOOT] Loaded in-cluster kube config")
        except Exception:
            # Fallback for local/dev execution
            config.load_kube_config()
            print("[BOOT] Loaded local kubeconfig")

        v1 = client.CoreV1Api()
        ns_list = v1.list_namespace().items
        print(f"[BOOT] Found {len(ns_list)} namespaces in cluster. Syncing...")
        print(f"[BOOT] Cluster ID: {TEMP_CLUSTER_ID}, Found Namespaces:")
        for ns in ns_list:
            print(f" - {ns.metadata.name}")
        synced = 0
        for ns in ns_list:
            ns_name = ns.metadata.name
            created_at = ns.metadata.creation_timestamp
            if created_at is not None:
                if isinstance(created_at, int):
                    created_at_unix = created_at
                else:
                    created_at_unix = int(created_at.timestamp())
            else:
                created_at_unix = None
            create_namespace(TEMP_CLUSTER_ID, ns_name, created_at_unix)
            synced += 1
        print(f"[BOOT] Namespace sync complete. Processed={synced}")
    except Exception as e:
        print(f"[BOOT][ERROR] Namespace sync failed: {e}")


def handle_namespace_event(event_type, namespace_obj):
    namespace_name = namespace_obj.metadata.name
    _created_at = namespace_obj.metadata.creation_timestamp
    if _created_at is not None:
        if isinstance(_created_at, int):
            created_at_unix = _created_at
        else:
            created_at_unix = int(_created_at.timestamp())
    else:
        created_at_unix = None

    if event_type == 'ADDED':
        # The cluster ID should be retrieved from a config or another source.
        create_namespace(TEMP_CLUSTER_ID, namespace_name, created_at_unix)
    elif event_type == 'MODIFIED':
        print(f"[~] Namespace 변경 감지: {namespace_name}")
        update_namespace(TEMP_CLUSTER_ID, namespace_name, created_at_unix)
    elif event_type == 'DELETED':
        delete_namespace(namespace_name)
