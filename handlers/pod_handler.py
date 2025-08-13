import uuid
from crud.pod_crud import create_pod, delete_pod, update_pod
from crud.common_crud import get_node_id_by_name, get_namespace_id_by_name

# This is a temporary placeholder. You should have a mechanism to get the actual SBOM ID.
TEMP_SBOM_ID = str(uuid.uuid4())

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
            create_pod(pod_name, str(node_id), str(namespace_id), str(TEMP_SBOM_ID) if TEMP_SBOM_ID else None, created_at_unix)
        else:
            print(f"[!] Could not find node or namespace ID for pod {pod_name}. Node ID: {node_id}, Namespace ID: {namespace_id}")

    elif event_type == 'MODIFIED':
        update_pod(pod_name)

    elif event_type == 'DELETED':
        namespace_id = get_namespace_id_by_name(namespace)
        delete_pod(pod_name, str(namespace_id))