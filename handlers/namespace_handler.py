import uuid
from crud.namespace_crud import create_namespace, delete_namespace

# This is a temporary placeholder. You should have a mechanism to get the actual cluster ID.
TEMP_CLUSTER_ID = uuid.uuid4()

def handle_namespace_event(event_type, namespace_obj):
    namespace_name = namespace_obj.metadata.name
    created_at = namespace_obj.metadata.creation_timestamp

    if event_type == 'ADDED':
        # The cluster ID should be retrieved from a config or another source.
        create_namespace(TEMP_CLUSTER_ID, namespace_name, created_at)
    elif event_type == 'MODIFIED':
        print(f"[~] Namespace 변경: {namespace_name}")
        # Placeholder for update logic
    elif event_type == 'DELETED':
        delete_namespace(namespace_name)
