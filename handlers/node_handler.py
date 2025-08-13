import uuid
from crud.node_crud import create_node, delete_node, update_node

# This is a temporary placeholder. You should have a mechanism to get the actual cluster ID.
TEMP_CLUSTER_ID = uuid.uuid4()

def handle_node_event(event_type, node_obj):
    node_name = node_obj.metadata.name
    created_at = node_obj.metadata.creation_timestamp

    zone = node_obj.metadata.labels.get("topology.kubernetes.io/zone")
    if zone is None:
        zone = node_obj.metadata.labels.get("failure-domain.beta.kubernetes.io/zone")
    if zone is None:
        zone = None

    if event_type == 'ADDED':
        # The cluster ID should be retrieved from a config or another source.
        create_node(TEMP_CLUSTER_ID, node_name, zone, int(created_at.timestamp()))
    elif event_type == 'MODIFIED':
        update_node(node_name, zone)
    elif event_type == 'DELETED':
        delete_node(node_name)
