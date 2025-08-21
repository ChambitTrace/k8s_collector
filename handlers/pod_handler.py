import uuid
from crud.pod_crud import create_pod, delete_pod, update_pod, list_all_pods
from crud.common_crud import get_node_id_by_name, get_namespace_id_by_name
from kubernetes import client, config


# Initial pod sync: fetch all existing pods and insert them
def init_pod_sync():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    pods = v1.list_pod_for_all_namespaces().items

    # 1) Build set of pods that currently exist in the cluster: {(p_name, nsid_str)}
    cluster_pods_keyset = set()
    for pod in pods:
        pod_name = pod.metadata.name
        namespace = pod.metadata.namespace
        ns_id = get_namespace_id_by_name(namespace)
        if ns_id:
            ns_id_str = str(ns_id)
            cluster_pods_keyset.add((pod_name, ns_id_str))

    # 2) Ensure existing cluster pods are present in DB (insert if missing)
    for pod in pods:
        pod_name = pod.metadata.name
        namespace = pod.metadata.namespace
        node_name = pod.spec.node_name
        created_at = pod.metadata.creation_timestamp

        node_id = get_node_id_by_name(node_name)
        namespace_id = get_namespace_id_by_name(namespace)

        if not node_id:
            node_id = get_node_id_by_name("ip-172-31-26-64")
        if not namespace_id:
            namespace_id = get_namespace_id_by_name("default")

        if created_at is not None:
            if isinstance(created_at, int):
                created_at_unix = created_at
            else:
                created_at_unix = int(created_at.timestamp())
        else:
            created_at_unix = None

        if node_id and namespace_id:
            create_pod(pod_name, str(node_id), str(namespace_id), None, created_at_unix)

    # 3) Delete pods from DB that are NOT in the current cluster set
    db_pods = list_all_pods()  # [(p_name, p_nsid), ...]
    print("[DEBUG] Pods in DB:")
    for p_name in db_pods:
        print(f" - {p_name}")
    for p_name, p_nsid in db_pods:
        key = (p_name, str(p_nsid))
        if key not in cluster_pods_keyset:
            # This pod no longer exists in the cluster -> delete from DB
            delete_pod(p_name, str(p_nsid))

def handle_pod_event(event_type, pod_obj):
    pod_name = pod_obj.metadata.name
    namespace = pod_obj.metadata.namespace
    node_name = pod_obj.spec.node_name
    created_at = pod_obj.metadata.creation_timestamp

    print(f"[DEBUG] Pod event received: pod_name={pod_name}, namespace={namespace}, node_name={node_name}")

    if event_type == 'ADDED':
        node_id = get_node_id_by_name(node_name)
        namespace_id = get_namespace_id_by_name(namespace)

        if not node_id:
            node_id = get_node_id_by_name("ip-172-31-26-64")
        if not namespace_id:
            namespace_id = get_namespace_id_by_name("default")

        print(f"[DEBUG] Resolved IDs: node_id={node_id}, namespace_id={namespace_id}")

        if node_id and namespace_id:
            # The SBOM ID should be retrieved based on the container image or other metadata.
            # Convert created_at to Unix timestamp (int) if not already int
            if created_at is not None:
                if isinstance(created_at, int):
                    created_at_unix = created_at
                else:
                    created_at_unix = int(created_at.timestamp())
            else:
                created_at_unix = None
            create_pod(pod_name, str(node_id), str(namespace_id), None, created_at_unix)
        else:
            print(f"[!] Could not find node or namespace ID for pod {pod_name}. Node ID: {node_id}, Namespace ID: {namespace_id}")

    elif event_type == 'MODIFIED':
        update_pod(pod_name)

    elif event_type == 'DELETED':
        namespace_id = get_namespace_id_by_name(namespace)
        delete_pod(pod_name, str(namespace_id))